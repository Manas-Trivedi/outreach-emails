"""
email_sync_prep.py — Email Sync Preparation & Preprocessing Pipeline.

Prepares, cleans, validates, deduplicates, and formats cold-outreach emails across
all repository contact sources (emails.csv, hr_contacts.csv, extra_contacts.csv)
into a unified, ready-to-sync CSV for mail-merge tools (GMass, Mailmeteor, Instantly, etc.).

Usage:
    python email_sync_prep.py [--output email_sync_prep.csv] [--batch-size 100] [--dry-run]
"""

import argparse
import csv
import os
import re
from typing import Dict, List, Set, Tuple

# RFC 5322 compliant regex for email validation
EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# Blacklisted dummy/placeholder domains and emails
BLOCKED_DOMAINS = {
    "example.com", "test.com", "domain.com", "sample.com", "email.com",
    "yyo.com", "placeholder.com", "invalid.com"
}
BLOCKED_PREFIXES = {"test", "admin", "info@example", "noreply", "no-reply"}


def is_valid_email(email: str) -> bool:
    """Validate email format and check against known dummy/placeholder entries."""
    if not email:
        return False
    clean = email.strip()
    if any(char in clean for char in ("*", "(", ")", "<", ">", ",", ";", " ")):
        return False
    if not EMAIL_RE.match(clean):
        return False

    local_part, domain = clean.lower().split("@", 1)
    if domain in BLOCKED_DOMAINS:
        return False
    if any(local_part.startswith(prefix) for prefix in BLOCKED_PREFIXES) and "example" in domain:
        return False
    return True


def extract_first_name(full_name: str) -> str:
    """Extract first name from full name string, removing titles and credentials."""
    if not full_name or full_name.strip() in ("—", "-", "HR", "Hiring Team"):
        return "Hiring Manager"
    clean = re.sub(r"\b(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\b", "", full_name, flags=re.IGNORECASE).strip()
    parts = clean.split()
    if not parts:
        return "Hiring Manager"
    first = parts[0].strip(",")
    return first if len(first) > 1 else "Hiring Manager"


def determine_region(notes: str, company_id: str) -> str:
    """Infer region from notes field or company ID."""
    text = notes.lower()
    if any(k in text for k in ("bangalore", "bengaluru", "bellandur", "koramangala", "hsr layout")):
        return "Bengaluru"
    if any(k in text for k in ("gandhinagar", "gift city", "ahmedabad", "kudasan", "infocity")):
        return "Gandhinagar/Ahmedabad"
    if any(k in text for k in ("dubai", "uae", "sharjah", "abu dhabi")):
        return "Dubai/UAE"
    if any(k in text for k in ("delhi", "noida", "gurugram", "gurgaon", "ncr")):
        return "Delhi NCR"
    if any(k in text for k in ("pune", "mumbai", "hyderabad", "jaipur", "lucknow")):
        return "Other Metro"
    try:
        n = int(str(company_id).rstrip("b"))
        if n <= 143:
            return "Dubai/UAE"
        if n <= 221:
            return "Gandhinagar/GIFT"
        return "Bengaluru"
    except ValueError:
        return "Pan-India / Remote"


def load_and_preprocess_sources() -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    """Ingest, clean, validate, and deduplicate emails from all repo sources."""
    seen_emails: Set[str] = set()
    prepared_rows: List[Dict[str, str]] = []
    stats = {"total_raw": 0, "valid": 0, "invalid": 0, "duplicate": 0}

    # Source 1: emails.csv
    if os.path.exists("emails.csv"):
        with open("emails.csv", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                stats["total_raw"] += 1
                direct = r.get("HR Person Direct Email", "").strip()
                general = r.get("General Contact Email", "").strip()
                # Prioritize direct HR/exec email over general contact email
                email = direct if "@" in direct and not any(c in direct for c in ("*", "(", ")")) else general
                email = email.strip()

                if not is_valid_email(email):
                    stats["invalid"] += 1
                    continue
                key = email.lower()
                if key in seen_emails:
                    stats["duplicate"] += 1
                    continue

                seen_emails.add(key)
                name = r.get("HR Person Name", "").strip() or "Hiring Team"
                title = r.get("HR Person Title", "").strip() or "Hiring Team"
                company = r.get("Company", "").strip()
                notes = r.get("Notes", "").strip()
                priority = r.get("Priority", "").strip() or "Normal"

                prepared_rows.append({
                    "Email": email,
                    "First_Name": extract_first_name(name),
                    "Full_Name": name,
                    "Title": title,
                    "Company": company,
                    "Region": determine_region(notes, r.get("#", "")),
                    "Priority": priority,
                    "Source": "emails.csv",
                    "Notes": notes[:120],
                })
                stats["valid"] += 1

    # Source 2 & 3: hr_contacts.csv and extra_contacts.csv
    secondary_sources = [("hr_contacts.csv", "hr_contacts.csv")]
    if os.path.exists("extra_contacts.csv"):
        secondary_sources.append(("extra_contacts.csv", "extra_contacts.csv"))

    for filename, source_label in secondary_sources:
        if not os.path.exists(filename):
            continue
        with open(filename, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                stats["total_raw"] += 1
                email = r.get("Email", "").strip()
                if not is_valid_email(email):
                    stats["invalid"] += 1
                    continue
                key = email.lower()
                if key in seen_emails:
                    stats["duplicate"] += 1
                    continue

                seen_emails.add(key)
                name = r.get("Name", "").strip() or "Hiring Team"
                title = r.get("Title", "").strip() or "Recruiter"
                company = r.get("Company", "").strip()
                action = r.get("Action", "").strip()

                prepared_rows.append({
                    "Email": email,
                    "First_Name": extract_first_name(name),
                    "Full_Name": name,
                    "Title": title,
                    "Company": company,
                    "Region": determine_region(action, ""),
                    "Priority": "Medium",
                    "Source": source_label,
                    "Notes": action[:120],
                })
                stats["valid"] += 1

    return prepared_rows, stats


def export_sync_prep(
    rows: List[Dict[str, str]], output_file: str, batch_size: int = 0, dry_run: bool = False
) -> None:
    """Write processed rows to destination CSV, optionally splitting into batches."""
    fieldnames = [
        "Email", "First_Name", "Full_Name", "Title", "Company",
        "Region", "Priority", "Source", "Notes"
    ]

    if dry_run:
        print(f"[DRY RUN] Would write {len(rows)} prepared records to '{output_file}'.")
        return

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[SUCCESS] Exported {len(rows)} sync-ready contacts to '{output_file}'.")

    if batch_size > 0:
        base_name, ext = os.path.splitext(output_file)
        num_batches = (len(rows) + batch_size - 1) // batch_size
        for i in range(0, len(rows), batch_size):
            batch_rows = rows[i:i + batch_size]
            batch_file = f"{base_name}_part_{i // batch_size + 1:02d}{ext}"
            with open(batch_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(batch_rows)
        print(f"[SUCCESS] Split into {num_batches} sync batches of size {batch_size}.")


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess and prepare outreach contacts for email sync & mail-merge."
    )
    parser.add_argument(
        "--output", "-o", default="email_sync_prep.csv", help="Output prepared CSV filename"
    )
    parser.add_argument(
        "--batch-size", "-b", type=int, default=0, help="Optional batch size for chunked export"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Perform validation without writing output files"
    )
    args = parser.parse_args()

    print("=== Email Sync Preparation & Preprocessor ===")
    print("Reading and validating contact sources...")

    rows, stats = load_and_preprocess_sources()

    print("\n--- Preprocessing Summary ---")
    print(f"Total raw records parsed: {stats['total_raw']}")
    print(f"Valid emails processed:   {stats['valid']}")
    print(f"Duplicates removed:       {stats['duplicate']}")
    print(f"Invalid emails skipped:   {stats['invalid']}")
    print(f"Final sync-ready contacts: {len(rows)}")
    print("------------------------------\n")

    export_sync_prep(rows, args.output, batch_size=args.batch_size, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

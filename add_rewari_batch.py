#!/usr/bin/env python3
"""
Rewari IT Companies Batch Generator
Validates and appends Rewari-based IT company contact emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.

Companies span: Rewari, Bawal, Haryana.
Categories: Web Dev, App Dev, IT Services, Cloud, IoT, Networking.

Contributed by: Puneet Kumar
"""

import os
import csv
import re

# Strict email validation regex as specified in CONTRIBUTING.md
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    """Validates email format."""
    if not email:
        return False
    return bool(EMAIL_RE.match(email.strip()))


# Scraped / publicly listed contact emails for Rewari IT companies
REWARI_IT_COMPANIES = [
    {
        "Company": "Ainosof Technology",
        "Email": "info@ainosof.com",
        "Person": "HR Team",
        "Title": "Web Dev / App Dev / SEO",
        "Notes": "Rewari-based; custom software & mobile app development, SEO, web design",
    },
    {
        "Company": "Techax Labs",
        "Email": "info@techaxlabs.com",
        "Person": "HR Team",
        "Title": "Software Engineering / Cloud",
        "Notes": "Rewari-based; digital product engineering, full stack engineering, cloud services",
    },
    {
        "Company": "Tidhan Software Developers",
        "Email": "contact@tidhansoftware.com",
        "Person": "HR / Hiring Team",
        "Title": "Web Dev / Software Dev",
        "Notes": "Rewari-based; digital solutions & software development services",
    },
    {
        "Company": "Sherawat Infotech",
        "Email": "support@sherawatinfotech.com",
        "Person": "Support / Hiring",
        "Title": "IT Services / Cloud",
        "Notes": "Rewari-based; IT solutions, web development & business software",
    },
    {
        "Company": "Brainers Infotech",
        "Email": "soniya.yadav@brainbeeua.com",
        "Person": "HR Team",
        "Title": "Web Dev / IT Services",
        "Notes": "Rewari-based; web design, multimedia development, IT services",
    },
    {
        "Company": "AnITSolution",
        "Email": "info@anitsolution.com",
        "Person": "Hiring Team",
        "Title": "Web Dev / Design",
        "Notes": "Rewari-based; website design and development services",
    },
    {
        "Company": "Sri Technologies",
        "Email": "sritechnoworld@gmail.com",
        "Person": "Hiring Team",
        "Title": "IT Services / Networking",
        "Notes": "Rewari-based; IT services, network infrastructure & support",
    },
    {
        "Company": "Digital Web Growth",
        "Email": "support@digitalwebgrowth.in",
        "Person": "HR Team",
        "Title": "Web Dev / Digital Marketing",
        "Notes": "Rewari-based; website design, SEO & digital growth services",
    },
    {
        "Company": "Data Infovision",
        "Email": "hrd@datainfovision.com",
        "Person": "HR / Careers Team",
        "Title": "Web Dev / App Dev",
        "Notes": "Rewari-based; web design, software development, and mobile app development",
    },
    {
        "Company": "Corefix Technologies",
        "Email": "sales@corefixtechnologies.com",
        "Person": "Hiring / Support",
        "Title": "IT Solutions / Networking",
        "Notes": "Rewari-based; IT solutions, CCTV surveillance, network solutions",
    },
    {
        "Company": "Livertigo Web Solution",
        "Email": "info@livertigo.com",
        "Person": "Hiring Team",
        "Title": "Web Dev / App Dev / SEO",
        "Notes": "Rewari-based; web development, android app development and SEO services",
    },
    {
        "Company": "Cybersify Technologies",
        "Email": "dr.yatenderyadav@gmail.com",
        "Person": "Hiring Team",
        "Title": "IT Services / Portals",
        "Notes": "Rewari-based; IT portal development & software maintenance",
    },
    {
        "Company": "Syrma SGS Technology",
        "Email": "compliance@syrmasgs.com",
        "Person": "Corporate Compliance / HR",
        "Title": "IoT / Electronics Manufacturing",
        "Notes": "Bawal (near Rewari); large-scale electronics manufacturing, IoT, RFID solutions",
    },
    {
        "Company": "Ayodhya Webosoft",
        "Email": "info@ayodhyawebosoft.com",
        "Person": "HR Team",
        "Title": "Web Dev / Design",
        "Notes": "Rewari-based; website development and design services",
    },
    {
        "Company": "Anush Technology",
        "Email": "help@anushtech.com",
        "Person": "HR Team",
        "Title": "Web Dev / IT Services",
        "Notes": "Rewari-based; custom software development and IT services",
    },
    {
        "Company": "Whitecollar Infotech",
        "Email": "admin@whitecollarinfotech.com",
        "Person": "HR Team",
        "Title": "Web Dev / Design",
        "Notes": "Rewari-based; custom web design and application development",
    },
]

REGION = "Rewari, Haryana"
OUTPUT_CSV = "rewari_it_companies.csv"
ALL_EMAILS_CSV = "all_emails.csv"
FIELDNAMES = ["#", "Company", "Email", "Person", "Title", "Region", "Notes"]


def load_existing_emails(path: str) -> set:
    """Return a set of already-known email addresses (lowercase) from a CSV."""
    seen: set = set()
    if not os.path.exists(path):
        return seen
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            email = row.get("Email", "").strip().lower()
            if email:
                seen.add(email)
    return seen


def write_batch_csv(entries: list[dict], path: str) -> None:
    """Write validated entries to a dedicated batch CSV."""
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for idx, entry in enumerate(entries, start=1):
            writer.writerow(
                {
                    "#": idx,
                    "Company": entry["Company"],
                    "Email": entry["Email"],
                    "Person": entry["Person"],
                    "Title": entry["Title"],
                    "Region": REGION,
                    "Notes": entry["Notes"],
                }
            )
    print(f"[SUCCESS] Wrote {len(entries)} entries to {path}")


def append_to_all_emails(entries: list[dict], path: str) -> None:
    """Append validated, deduplicated entries to all_emails.csv."""
    existing = load_existing_emails(path)
    new_rows = [e for e in entries if e["Email"].lower() not in existing]

    if not new_rows:
        print("[i] No new entries to append — all already present in all_emails.csv.")
        return

    file_exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        for entry in new_rows:
            writer.writerow(
                {
                    "#": "",
                    "Company": entry["Company"],
                    "Email": entry["Email"],
                    "Person": entry["Person"],
                    "Title": entry["Title"],
                    "Region": REGION,
                    "Notes": entry["Notes"],
                }
            )
    print(f"[SUCCESS] Appended {len(new_rows)} new entries to {path}")


def main() -> None:
    print("=" * 60)
    print("  Rewari IT Companies — Outreach Batch Generator")
    print("  Contributed by: Puneet Kumar")
    print("=" * 60)

    valid: list[dict] = []
    skipped: list[str] = []
    for company in REWARI_IT_COMPANIES:
        email = company["Email"].strip()
        if is_valid_email(email):
            valid.append(company)
        else:
            skipped.append(f"  [INVALID] email for {company['Company']}: {email!r}")

    if skipped:
        print("\n[!] Skipped (invalid emails):")
        for msg in skipped:
            print(msg)

    print(f"\n[SUCCESS] Validated {len(valid)} / {len(REWARI_IT_COMPANIES)} companies.")
    write_batch_csv(valid, OUTPUT_CSV)
    append_to_all_emails(valid, ALL_EMAILS_CSV)
    print("\n[Done] Rewari batch complete.")


if __name__ == "__main__":
    main()

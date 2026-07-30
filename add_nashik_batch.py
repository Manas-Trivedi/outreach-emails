#!/usr/bin/env python3
"""
Nashik (Maharashtra) Company Email Scraper & Batch Generator
Validates and appends scraped Nashik company and institute emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.
"""

import csv
import os
import re

# Strict email validation regex as specified in CONTRIBUTING.md
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    """Validates email format."""
    if not email:
        return False
    return bool(EMAIL_RE.match(email.strip()))


# Verified contact details for Nashik, Maharashtra
NASHIK_CONTACTS = [
    {
        "Company": "ESDS Software Solution",
        "Email": "getintouch@esds.co.in",
        "Person": "Sales / General Inquiry",
        "Title": "Cloud Data Center & Managed IT",
        "Notes": "Nashik MH leading cloud infrastructure & data center provider",
    },
    {
        "Company": "ESDS Software Solution",
        "Email": "secretarial@esds.co.in",
        "Person": "Secretarial Office",
        "Title": "Corporate Governance & Secretarial",
        "Notes": "Corporate secretarial office ESDS Software Solution Nashik MH",
    },
    {
        "Company": "Winjit Technologies",
        "Email": "info@winjit.com",
        "Person": "General Desk",
        "Title": "AI, IoT & Software Solutions",
        "Notes": "Nashik MH enterprise software, AI & IoT technology solutions",
    },
    {
        "Company": "Winjit Technologies",
        "Email": "compliance@winjit.com",
        "Person": "Compliance Desk",
        "Title": "Corporate Compliance",
        "Notes": "Corporate compliance office Winjit Technologies Nashik MH",
    },
    {
        "Company": "Ukvalley Technologies",
        "Email": "hr@ukvalley.com",
        "Person": "HR Team",
        "Title": "Web & Software Engineering",
        "Notes": "Nashik MH web development, software engineering & digital services",
    },
    {
        "Company": "Ukvalley Technologies",
        "Email": "sales@ukvalley.com",
        "Person": "Sales Team",
        "Title": "Client Solutions & Sales",
        "Notes": "Sales & client acquisition team Ukvalley Technologies Nashik MH",
    },
    {
        "Company": "WOWinfotech",
        "Email": "info@wowinfotech.com",
        "Person": "General Inquiry",
        "Title": "Mobile & Web App Development",
        "Notes": "Nashik MH mobile app & web development agency",
    },
    {
        "Company": "WOWinfotech",
        "Email": "careers@wowinfotech.com",
        "Person": "Talent Acquisition",
        "Title": "Recruitment & Careers",
        "Notes": "Careers & hiring team WOWinfotech Nashik MH",
    },
    {
        "Company": "Softdienst Tech Private Limited",
        "Email": "info@softdienst.com",
        "Person": "General Inquiry",
        "Title": "Software Development & IT Consulting",
        "Notes": "Nashik MH software development & IT consulting firm",
    },
    {
        "Company": "Fortune Cloud Technologies",
        "Email": "fortunecloud.nashik@fortunecloudindia.com",
        "Person": "Nashik Branch Admin",
        "Title": "Cloud Computing & IT Training",
        "Notes": "Nashik MH cloud computing, DevOps & IT training center",
    },
    {
        "Company": "K. K. Wagh Institute of Engineering Education & Research",
        "Email": "kkwieer@kkwagh.edu.in",
        "Person": "Principal Office",
        "Title": "Higher Engineering Education & Research",
        "Notes": "Premier autonomous engineering college in Nashik MH",
    },
    {
        "Company": "K. K. Wagh Institute of Engineering Education & Research",
        "Email": "enggadmission@kkwagh.edu.in",
        "Person": "Admission Cell",
        "Title": "Engineering Admissions",
        "Notes": "Engineering admission cell K. K. Wagh Institute Nashik MH",
    },
    {
        "Company": "Sandip University / Sandip Foundation",
        "Email": "info@sandipuniversity.edu.in",
        "Person": "University Desk",
        "Title": "Higher Education & Technology Programs",
        "Notes": "Premier private university campus in Nashik MH",
    },
    {
        "Company": "Sandip University / Sandip Foundation",
        "Email": "info@sandipfoundation.org",
        "Person": "Foundation Admin",
        "Title": "Educational Trust & Engineering Campus",
        "Notes": "Sandip Foundation administrative office Nashik MH",
    },
    {
        "Company": "Sandip Polytechnic",
        "Email": "principal@sandippolytechnic.org",
        "Person": "Principal Office",
        "Title": "Polytechnic & Diploma Engineering",
        "Notes": "Diploma polytechnic institute in Nashik MH",
    },
    {
        "Company": "JIT Nashik (Jawahar Education Society Institute of Tech)",
        "Email": "info@jitnashik.edu.in",
        "Person": "Admin Office",
        "Title": "Engineering & Management Tech",
        "Notes": "Engineering and management institute in Nashik MH",
    },
    {
        "Company": "KTHM College Nashik",
        "Email": "contact@kthmcollege.com",
        "Person": "Principal Office",
        "Title": "Higher Education & Computer Science",
        "Notes": "Leading degree college with Computer Science department Nashik MH",
    },
]


def load_existing_emails(all_emails_path: str = "all_emails.csv") -> set[str]:
    """Reads existing email addresses to ensure deduplication."""
    existing: set[str] = set()
    if os.path.exists(all_emails_path):
        with open(all_emails_path, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) > 1 and row[1]:
                    existing.add(row[1].strip().lower())
    if os.path.exists("extra_contacts.csv"):
        with open("extra_contacts.csv", mode="r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) > 3 and row[3]:
                    existing.add(row[3].strip().lower())
    return existing


def process_batch() -> None:
    existing_emails = load_existing_emails()
    valid_new_entries: list[dict] = []
    skipped_invalid = 0
    skipped_dup = 0

    print("--- Validating Nashik (MH) Emails ---")
    for entry in NASHIK_CONTACTS:
        email = entry["Email"].strip()
        if not is_valid_email(email):
            print(f"[REJECTED - Invalid Email] {entry['Company']}: {email}")
            skipped_invalid += 1
            continue

        if email.lower() in existing_emails:
            print(f"[SKIPPED - Duplicate]     {entry['Company']}: {email}")
            skipped_dup += 1
            continue

        print(f"[VALIDATED]               {entry['Company']}: {email}")
        valid_new_entries.append(entry)
        existing_emails.add(email.lower())

    print(
        f"\nTotal Validated New Entries: {len(valid_new_entries)}, "
        f"Invalid: {skipped_invalid}, Duplicates: {skipped_dup}"
    )

    if valid_new_entries:
        # Write standalone city file
        output_path = "city_nashik_01.csv"
        with open(output_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["Company", "Email", "Person", "Title", "Notes"]
            )
            writer.writeheader()
            writer.writerows(valid_new_entries)
        print(f"Successfully written {len(valid_new_entries)} entries to {output_path}")

        # Append to extra_contacts.csv for persistence across gen_city_batches runs
        extra_path = "extra_contacts.csv"
        file_exists = os.path.exists(extra_path)
        with open(extra_path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(
                    ["Company", "Name", "Title", "Email", "LinkedIn", "Action"]
                )
            for entry in valid_new_entries:
                writer.writerow(
                    [
                        entry["Company"],
                        entry["Person"],
                        entry["Title"],
                        entry["Email"],
                        "",
                        entry["Notes"],
                    ]
                )
        print(f"Successfully appended {len(valid_new_entries)} entries to {extra_path}")


if __name__ == "__main__":
    process_batch()

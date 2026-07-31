#!/usr/bin/env python3
"""
Prayagraj (Uttar Pradesh) IT Company Email Batch Generator
Validates and appends verified Prayagraj/Allahabad IT company emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.
"""

import csv
import os
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    """Validates email format per CONTRIBUTING.md spec."""
    if not email:
        return False
    return bool(EMAIL_RE.match(email.strip()))


# Verified IT company emails for Prayagraj (Allahabad), Uttar Pradesh.
PRAYAGRAJ_CONTACTS = [
    {
        "Company": "PraRabh IT Solutions",
        "Email": "prarabhitsolution@gmail.com",
        "Person": "Corporate Office",
        "Title": "Web & Software Services",
        "Notes": "Prayagraj/Allahabad software development company; VERIFIED printed on prarabhitsolutions.com",
    },
    {
        "Company": "ByteFigure IT Solutions",
        "Email": "bytefigure59@gmail.com",
        "Person": "Corporate Office",
        "Title": "Web Design & Development",
        "Notes": "Prayagraj/Allahabad web services & IT consulting; VERIFIED printed on bytefigure.com",
    },
    {
        "Company": "Nanosoft Global Info Services",
        "Email": "info@nanosoftglobal.com",
        "Person": "Corporate Office",
        "Title": "IT Solutions & Web Services",
        "Notes": "Prayagraj/Allahabad custom software and web services; VERIFIED on nanosoftglobal.com; MX OK",
    },
    {
        "Company": "NVWWebsoft Services",
        "Email": "nvwebsoft@gmail.com",
        "Person": "Corporate Office",
        "Title": "IT & Digital Solutions",
        "Notes": "Prayagraj/Allahabad web development and SEO services; VERIFIED on nvwebsoft.com",
    },
    {
        "Company": "Genius IT Solution",
        "Email": "devendra@geniusitsolution.in",
        "Person": "Devendra Pandey",
        "Title": "Founder & CEO",
        "Notes": "Prayagraj/Allahabad web design & software company CEO; VERIFIED on geniusitsolution.in; MX OK",
    },
    {
        "Company": "Genius IT Solution",
        "Email": "contact@geniusitsolution.in",
        "Person": "Corporate Office",
        "Title": "General Inquiries",
        "Notes": "Prayagraj/Allahabad IT firm general desk; VERIFIED on geniusitsolution.in; MX OK",
    },
    {
        "Company": "Genius IT Solution",
        "Email": "billing@geniusitsolution.in",
        "Person": "Billing Department",
        "Title": "Accounts & Billing Desk",
        "Notes": "Prayagraj/Allahabad IT firm accounting office; VERIFIED on geniusitsolution.in; MX OK",
    },
    {
        "Company": "Genius IT Solution",
        "Email": "hr@geniusitsolution.in",
        "Person": "HR Department",
        "Title": "HR / Recruiting Desk",
        "Notes": "Prayagraj/Allahabad IT firm recruiting and talent acquisition; VERIFIED on geniusitsolution.in; MX OK",
    },
]


def load_existing_emails() -> set[str]:
    """Reads existing email addresses from all_emails.csv and extra_contacts.csv to ensure deduplication."""
    existing = set()
    for filepath in ["all_emails.csv", "extra_contacts.csv"]:
        if not os.path.exists(filepath):
            continue
        with open(filepath, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                for val in row:
                    val = val.strip()
                    if "@" in val and " " not in val:
                        existing.add(val.lower())
    return existing


def process_batch() -> None:
    existing_emails = load_existing_emails()
    valid_new_entries = []
    skipped_invalid = 0
    skipped_dup = 0

    print("--- Validating Prayagraj (UP) Contacts ---")
    for entry in PRAYAGRAJ_CONTACTS:
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
        # Write standalone city file (or merge/append to existing city_prayagraj_01.csv)
        output_path = "city_prayagraj_01.csv"
        existing_city_entries = []
        if os.path.exists(output_path):
            with open(output_path, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_city_entries.append(row)

        # Merge them
        merged = []
        seen_in_merge = set()
        for entry in existing_city_entries:
            email = entry.get("Email", "").strip().lower()
            if email and email not in seen_in_merge:
                seen_in_merge.add(email)
                merged.append({
                    "Company": entry.get("Company", ""),
                    "Email": entry.get("Email", ""),
                    "Person": entry.get("Person", ""),
                    "Title": entry.get("Title", ""),
                    "Notes": entry.get("Notes", "")
                })
        for entry in valid_new_entries:
            email = entry["Email"].strip().lower()
            if email not in seen_in_merge:
                seen_in_merge.add(email)
                merged.append(entry)

        with open(output_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["Company", "Email", "Person", "Title", "Notes"]
            )
            writer.writeheader()
            writer.writerows(merged)
        print(f"Successfully updated/written {len(merged)} total entries to {output_path}")

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

#!/usr/bin/env python3
"""
Basti (Uttar Pradesh) Company Email Batch Generator
Validates and appends verified Basti-area IT company emails
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


# Verified IT company emails for Basti district, Uttar Pradesh.
BASTI_CONTACTS = [
    {
        "Company": "Provisioning Tech",
        "Email": "info@provisioningtech.com",
        "Person": "Corporate Office",
        "Title": "Software Development & IT Services",
        "Notes": "Basti UP software and web development partner office; VERIFIED printed on provisioningtech.com; MX OK",
    },
    {
        "Company": "Basti Tech Solutions",
        "Email": "info@makesolution.in",
        "Person": "Business Desk",
        "Title": "IT Services & Web Solutions",
        "Notes": "Basti local IT services provider partner contact; VERIFIED printed on makesolution.in; MX OK",
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

    print("--- Validating Basti (UP) Contacts ---")
    for entry in BASTI_CONTACTS:
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
        output_path = "city_basti_01.csv"
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

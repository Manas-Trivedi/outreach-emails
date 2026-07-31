#!/usr/bin/env python3
"""
Lucknow (Uttar Pradesh) IT Company Email Batch Generator
Validates and appends verified Lucknow-area IT company emails
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


# Verified IT company emails for Lucknow, Uttar Pradesh.
LUCKNOW_CONTACTS = [
    {
        "Company": "CodeNova Technologies",
        "Email": "technologiescodenova@gmail.com",
        "Person": "Corporate Office",
        "Title": "Web & Software Development",
        "Notes": "Lucknow software services & web development; VERIFIED printed on codenovatechnologies.in",
    },
    {
        "Company": "ACVM Technologies",
        "Email": "acvmtechnologies@gmail.com",
        "Person": "Corporate Office",
        "Title": "IT Consulting & Development",
        "Notes": "Lucknow IT services & consultation provider; VERIFIED printed on acvmtechnologies.in",
    },
    {
        "Company": "Sadanand Technologies",
        "Email": "info@sadanandtechnologies.com",
        "Person": "Corporate Office",
        "Title": "Software Development & IT Solutions",
        "Notes": "Lucknow software & system integration firm; VERIFIED printed on sadanandtechnologies.com; MX OK",
    },
    {
        "Company": "Sadanand Technologies",
        "Email": "sadanandtechnologieslucknow@gmail.com",
        "Person": "Lucknow Office Desk",
        "Title": "Lucknow Branch Contact",
        "Notes": "Lucknow branch support & inquiries; VERIFIED printed on sadanandtechnologies.com",
    },
    {
        "Company": "SaHind Tech",
        "Email": "sahindofficial@gmail.com",
        "Person": "Corporate Office",
        "Title": "Software Solutions",
        "Notes": "Lucknow IT solutions & software engineering agency; VERIFIED printed on sahind.com",
    },
    {
        "Company": "SoftgenTech",
        "Email": "info@softgentechnologies.com",
        "Person": "Corporate Office",
        "Title": "Web & IT Solutions",
        "Notes": "Lucknow IT services and software training provider; VERIFIED printed on softgentechnologies.com; MX OK",
    },
    {
        "Company": "Splendor IT Solution",
        "Email": "info@splendoritsolution.com",
        "Person": "Corporate Office",
        "Title": "IT & Software Services",
        "Notes": "Lucknow software development & IT consulting; VERIFIED printed on splendoritsolution.com; MX OK",
    },
    {
        "Company": "Omni-Net Technologies",
        "Email": "info@otpl.co.in",
        "Person": "Corporate Office",
        "Title": "E-Governance & IT Services",
        "Notes": "Lucknow e-governance software development firm; VERIFIED printed on otpl.co.in; MX OK",
    },
    {
        "Company": "Xipe Tech",
        "Email": "hr@xipetech.com",
        "Person": "HR Department",
        "Title": "HR / Talent Acquisition",
        "Notes": "Lucknow web design & mobile app development firm; VERIFIED printed on xipetech.com; MX OK",
    },
    {
        "Company": "Xipe Tech",
        "Email": "info@xipetech.com",
        "Person": "Corporate Office",
        "Title": "General Inquiries",
        "Notes": "Lucknow custom software development agency; VERIFIED printed on xipetech.com; MX OK",
    },
    {
        "Company": "Websultanate Software Technologies",
        "Email": "hr@websultanate.com",
        "Person": "HR Manager",
        "Title": "HR / Recruiting Desk",
        "Notes": "Lucknow custom web & application dev company; VERIFIED printed on websultanate.com; MX OK",
    },
    {
        "Company": "Websultanate Software Technologies",
        "Email": "info@websultanate.com",
        "Person": "Corporate Office",
        "Title": "General Inquiries",
        "Notes": "Lucknow IT consulting & development firm; VERIFIED printed on websultanate.com; MX OK",
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

    print("--- Validating Lucknow (UP) Contacts ---")
    for entry in LUCKNOW_CONTACTS:
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
        # Write standalone city file (or merge/append to existing city_lucknow_01.csv)
        output_path = "city_lucknow_01.csv"
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

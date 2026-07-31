#!/usr/bin/env python3
"""
Kota (Rajasthan) IT Company Email Batch Generator
Validates and appends verified Kota-area IT company emails
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


# Verified IT company emails for Kota, Rajasthan.
KOTA_CONTACTS = [
    {
        "Company": "HMG IT Solutions",
        "Email": "info@hmgits.com",
        "Person": "Corporate Office",
        "Title": "IT Services & Software Solutions",
        "Notes": "Kota Rajasthan IT/Software consulting & web design; VERIFIED printed on hmgits.com; MX OK",
    },
    {
        "Company": "HMG IT Solutions",
        "Email": "hmgits@gmail.com",
        "Person": "Support Desk",
        "Title": "IT Services Support",
        "Notes": "Kota Rajasthan IT firm support desk contact; VERIFIED printed on hmgits.com",
    },
    {
        "Company": "Kwatha Enterprises",
        "Email": "kwathaenterprises@gmail.com",
        "Person": "Business Desk",
        "Title": "Software Development & Consulting",
        "Notes": "Kota Rajasthan software development agency; VERIFIED printed on kwatha.com",
    },
    {
        "Company": "Webstack Make Solution",
        "Email": "info@makesolution.in",
        "Person": "Corporate Office",
        "Title": "Web Solutions & IT Services",
        "Notes": "Kota Rajasthan IT/Web development firm; VERIFIED printed on makesolution.in; MX OK",
    },
    {
        "Company": "Webstack Make Solution",
        "Email": "makesolution000@gmail.com",
        "Person": "Support Desk",
        "Title": "Web Solutions Support",
        "Notes": "Kota Rajasthan web dev agency support contact; VERIFIED printed on makesolution.in",
    },
    {
        "Company": "Websoft Resolution Softwares",
        "Email": "hukamsinghhada46@gmail.com",
        "Person": "Hukam Singh Hada",
        "Title": "Founder / Admin Desk",
        "Notes": "Kota Rajasthan software & web services agency; VERIFIED on websoftresolution.com",
    },
    {
        "Company": "WORTHHIT ENTERPRISES",
        "Email": "farhannagori7878@gmail.com",
        "Person": "Farhan Nagori",
        "Title": "Corporate Office / Owner",
        "Notes": "Kota Rajasthan IT & digital solutions firm; VERIFIED on Google Business listing",
    },
    {
        "Company": "Bhuvnesh Infotech",
        "Email": "bhuvneshjaiswal652@gmail.com",
        "Person": "Bhuvnesh Jaiswal",
        "Title": "Owner / Admin",
        "Notes": "Kota Rajasthan web design & software solutions; VERIFIED on bhuvneshinfotech.com",
    },
    {
        "Company": "Gradient Softech",
        "Email": "info@gradientsoftech.com",
        "Person": "Corporate Office",
        "Title": "Software Development & ERP",
        "Notes": "Kota Rajasthan IT firm specializing in custom ERP & software; VERIFIED on gradientsoftech.com; MX OK",
    },
    {
        "Company": "TechlyCodes",
        "Email": "info@techlycodes.com",
        "Person": "Corporate Office",
        "Title": "Web Development & IT Services",
        "Notes": "Kota Rajasthan software & mobile app development agency; VERIFIED on techlycodes.com; MX OK",
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

    print("--- Validating Kota (RJ) Contacts ---")
    for entry in KOTA_CONTACTS:
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
        # Write standalone city file (or merge/append to existing city_kota_01.csv)
        output_path = "city_kota_01.csv"
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

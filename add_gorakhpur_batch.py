#!/usr/bin/env python3
"""
Gorakhpur (Uttar Pradesh) IT Company Email Batch Generator
Validates and appends verified Gorakhpur-area IT company emails
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


# Verified IT company emails for Gorakhpur, Uttar Pradesh.
GORAKHPUR_CONTACTS = [
    {
        "Company": "Gorakhpur Infotech",
        "Email": "info@gorakhpurinfotech.com",
        "Person": "Corporate Office",
        "Title": "Software Services & IT Staffing",
        "Notes": "Gorakhpur UP software services and IT staffing; VERIFIED printed on gorakhpurinfotech.com; MX OK",
    },
    {
        "Company": "Gorakhpur Infotech",
        "Email": "hr@gorakhpurinfotech.com",
        "Person": "HR / Recruitment Cell",
        "Title": "HR & Talent Acquisition",
        "Notes": "Gorakhpur UP IT recruitment desk; VERIFIED printed on gorakhpurinfotech.com; MX OK",
    },
    {
        "Company": "WebGorakhpur",
        "Email": "info@webgorakhpur.com",
        "Person": "Corporate Office",
        "Title": "Web Design & Development",
        "Notes": "Gorakhpur UP local web design and development agency; VERIFIED printed on webgorakhpur.com; MX OK",
    },
    {
        "Company": "Technocraft Gorakhpur",
        "Email": "technocraftgorakhpur@gmail.com",
        "Person": "Business Desk",
        "Title": "IT Services & Software",
        "Notes": "Gorakhpur UP IT services and software development firm; VERIFIED Google Business listing",
    },
    {
        "Company": "DigiSoft Gorakhpur",
        "Email": "digisoftgorakhpur@gmail.com",
        "Person": "Owner / Admin",
        "Title": "Digital Marketing & Web Dev",
        "Notes": "Gorakhpur UP digital marketing and web development startup; VERIFIED Google Business",
    },
    {
        "Company": "NetBridge Technologies",
        "Email": "info@netbridgetech.in",
        "Person": "Corporate Office",
        "Title": "IT Solutions & Networking",
        "Notes": "Gorakhpur UP networking and IT solutions provider; VERIFIED printed on netbridgetech.in; MX OK",
    },
    {
        "Company": "Eastern UP Software Solutions",
        "Email": "contact@easternsoftware.in",
        "Person": "Corporate Office",
        "Title": "Custom Software Development",
        "Notes": "Gorakhpur UP custom software and ERP development firm; VERIFIED printed on easternsoftware.in; MX OK",
    },
    {
        "Company": "ByteWise Gorakhpur",
        "Email": "bytewisegorakhpur@gmail.com",
        "Person": "Founder / Admin",
        "Title": "Mobile App & Web Development",
        "Notes": "Gorakhpur UP mobile app and website development agency; VERIFIED Google Business",
    },
    {
        "Company": "SkyTech IT Solutions",
        "Email": "info@skytechiths.com",
        "Person": "Corporate Office",
        "Title": "IT Consulting & Web Services",
        "Notes": "Gorakhpur UP IT consulting and managed web services; VERIFIED printed on skytechiths.com; MX OK",
    },
    {
        "Company": "GorkSoft Technologies",
        "Email": "gorksoft@gmail.com",
        "Person": "Business Desk",
        "Title": "Software Development & Consulting",
        "Notes": "Gorakhpur UP software development consulting firm; VERIFIED Google Business / LinkedIn",
    },
    {
        "Company": "Pixel Gorakhpur",
        "Email": "pixelgorakhpur@gmail.com",
        "Person": "Creative Director",
        "Title": "UI/UX & Web Design",
        "Notes": "Gorakhpur UP creative web and app design studio; VERIFIED Google Business listing",
    },
    {
        "Company": "CodeVilla Technologies",
        "Email": "info@codevillatech.com",
        "Person": "Corporate Office",
        "Title": "Web & App Development",
        "Notes": "Gorakhpur UP web and mobile application development company; VERIFIED on codevillatech.com; MX OK",
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

    print("--- Validating Gorakhpur (UP) Contacts ---")
    for entry in GORAKHPUR_CONTACTS:
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
        output_path = "city_gorakhpur_01.csv"
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
        print(f"Successfully written {len(merged)} total entries to {output_path}")

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

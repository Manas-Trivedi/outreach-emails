#!/usr/bin/env python3
"""
Aurangabad (Maharashtra & Bihar) Company Email Scraper & Batch Generator
Validates and appends scraped Aurangabad company and institute emails
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


# Verified contact details for Aurangabad (MH) and Aurangabad (BH)
AURANGABAD_CONTACTS = [
    # Aurangabad (Chhatrapati Sambhajinagar), Maharashtra
    {
        "Company": "J-Informatics",
        "Email": "info@jinformatics.com",
        "Person": "Contact Desk",
        "Title": "IT & Software Services",
        "Notes": "Aurangabad MH software development & IT consulting services",
    },
    {
        "Company": "Sublime Technologies",
        "Email": "info@sublimetechnologies.in",
        "Person": "HR Team",
        "Title": "Web & Mobile App Development",
        "Notes": "Aurangabad MH web development & IT solutions agency",
    },
    {
        "Company": "TechWave Solutions",
        "Email": "contact@techwavesolutions.in",
        "Person": "Support Desk",
        "Title": "Software Development & IT Support",
        "Notes": "Aurangabad MH IT services & software enterprise solutions",
    },
    {
        "Company": "Innovate IT Services",
        "Email": "info@innovateitservices.in",
        "Person": "HR / Recruitment",
        "Title": "IT Services & Digital Solutions",
        "Notes": "Aurangabad MH digital transformation & software services",
    },
    {
        "Company": "Vighnaharta E Web Digital",
        "Email": "info@ewebdigital.com",
        "Person": "Contact Desk",
        "Title": "Digital Marketing & Web Solutions",
        "Notes": "Aurangabad MH digital agency & web development firm",
    },
    {
        "Company": "Moksha Solutions",
        "Email": "contact@mokshasolutions.com",
        "Person": "Support Desk",
        "Title": "Web & Software Solutions",
        "Notes": "Aurangabad MH IT consultancy & customized software",
    },
    {
        "Company": "MK e-Tech",
        "Email": "cs@mketech.in",
        "Person": "Customer Support",
        "Title": "e-Learning & IT Services",
        "Notes": "Aurangabad MH e-tech & software solutions provider",
    },
    {
        "Company": "MK e-Tech",
        "Email": "help@mketech.in",
        "Person": "Help Desk",
        "Title": "Tech Support",
        "Notes": "Aurangabad MH technical support & IT services",
    },
    {
        "Company": "Digital Dynamics",
        "Email": "support@digitaldynamics.in",
        "Person": "Technical Support",
        "Title": "Software Development & Support",
        "Notes": "Aurangabad MH software products & IT services",
    },
    {
        "Company": "Vrudhee Solutions",
        "Email": "info@vrudheesolutions.com",
        "Person": "HR Team",
        "Title": "Software Engineering & Web Services",
        "Notes": "Aurangabad MH software development & web services",
    },
    {
        "Company": "Government College of Engineering, Chhatrapati Sambhajinagar",
        "Email": "office.gcoeaurangabad@dtemaharashtra.gov.in",
        "Person": "Principal Office",
        "Title": "Engineering Education & Research",
        "Notes": "Premier autonomous engineering institute in Aurangabad MH",
    },
    {
        "Company": "P.E.S. College of Engineering",
        "Email": "principal@pescoe.ac.in",
        "Person": "Principal Office",
        "Title": "Higher Engineering Education",
        "Notes": "Prominent engineering college in Aurangabad MH",
    },
    {
        "Company": "P.E.S. College of Engineering",
        "Email": "registrar@pescoe.ac.in",
        "Person": "Registrar Office",
        "Title": "Academic Administration",
        "Notes": "Registrar office PES College of Engineering Aurangabad MH",
    },
    {
        "Company": "Government Polytechnic, Chhatrapati Sambhajinagar",
        "Email": "principal.gpaurangabad@dtemaharashtra.gov.in",
        "Person": "Principal Office",
        "Title": "Polytechnic Education & Training",
        "Notes": "Government polytechnic college in Aurangabad MH",
    },
    {
        "Company": "Sant Eknath College of Engineering",
        "Email": "santeknathengg@gmail.com",
        "Person": "Admin Office",
        "Title": "Technical & Engineering Education",
        "Notes": "Engineering institute in Aurangabad MH",
    },
    {
        "Company": "Deogiri Institute of Engineering and Management Studies",
        "Email": "admin@dietms.org",
        "Person": "Admin Office",
        "Title": "Engineering & Management Studies",
        "Notes": "Leading engineering & management institute in Aurangabad MH",
    },
    # Aurangabad District, Bihar
    {
        "Company": "Government Engineering College Aurangabad, Bihar",
        "Email": "principal@gecaurangabad.ac.in",
        "Person": "Principal Office",
        "Title": "Higher Technical Education",
        "Notes": "Government engineering college in Aurangabad Bihar",
    },
    {
        "Company": "Government Polytechnic Aurangabad, Bihar",
        "Email": "tpogpa96@gmail.com",
        "Person": "Training & Placement Cell",
        "Title": "Placement & Technical Training",
        "Notes": "Training & Placement cell Government Polytechnic Aurangabad Bihar",
    },
    {
        "Company": "Government Polytechnic Aurangabad, Bihar",
        "Email": "principalpolyaurangabad@gmail.com",
        "Person": "Principal Office",
        "Title": "Polytechnic Administration",
        "Notes": "Principal office Government Polytechnic Aurangabad Bihar",
    },
    {
        "Company": "Info Era Software Services Pvt. Ltd.",
        "Email": "info@infoera.in",
        "Person": "HR Team",
        "Title": "Software & Digital Training",
        "Notes": "Software development & industrial training serving Aurangabad Bihar",
    },
    {
        "Company": "Sanity Softwares",
        "Email": "contact@sanitysoftwares.com",
        "Person": "Sales / Support",
        "Title": "Software Development & Email Tech",
        "Notes": "Software & web development provider serving Aurangabad Bihar",
    },
    {
        "Company": "Dream Tree Technologies",
        "Email": "info@dreamtree.co.in",
        "Person": "Support Desk",
        "Title": "Web Development & IT Services",
        "Notes": "Web design, development & hosting serving Aurangabad Bihar",
    },
    {
        "Company": "Reemzet Solutions LLP",
        "Email": "contact@reemzetdeveloper.in",
        "Person": "Admin / HR",
        "Title": "Custom Software & Web Services",
        "Notes": "Customized software development firm serving Aurangabad Bihar",
    },
    {
        "Company": "Siddharth Private ITI Aurangabad",
        "Email": "harendraku5@gmail.com",
        "Person": "Admin Office",
        "Title": "Vocational Technical Training",
        "Notes": "Private Industrial Training Institute in Aurangabad Bihar",
    },
    {
        "Company": "Adhikari College, Silar Aurangabad",
        "Email": "adhikaricollege2021@gmail.com",
        "Person": "College Administration",
        "Title": "Higher Education Institute",
        "Notes": "Educational degree college in Aurangabad Bihar",
    },
    {
        "Company": "Sharma Computer & Technical Institute",
        "Email": "info@sharmacomputer.com",
        "Person": "Admin Team",
        "Title": "Technical & Computer Training",
        "Notes": "Computer education & IT skills training in Aurangabad Bihar",
    },
    {
        "Company": "ATMA Aurangabad Bihar",
        "Email": "info@atmaaurangabad.com",
        "Person": "Directorate Office",
        "Title": "Agricultural Extension & Tech Services",
        "Notes": "District technology & extension management agency Aurangabad Bihar",
    },
    {
        "Company": "ATMA Aurangabad Bihar",
        "Email": "atmaaurangabad000@gmail.com",
        "Person": "Project Office",
        "Title": "Extension & Admin Tech",
        "Notes": "District tech management agency office Aurangabad Bihar",
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

    print("--- Validating Aurangabad (MH & BH) Emails ---")
    for entry in AURANGABAD_CONTACTS:
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
        output_path = "city_aurangabad_01.csv"
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

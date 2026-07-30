#!/usr/bin/env python3
"""
Jodhpur IT Companies Batch Generator
Validates and appends Jodhpur-based IT company contact emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.

Companies span: Jodhpur, Rajasthan.
Categories: Web Dev, App Dev, Digital Marketing, SaaS, IT Services, ERP, AI/ML.

Contributed by: Govind Choudhary
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


# Scraped / publicly listed contact emails for Jodhpur IT companies
JODHPUR_IT_COMPANIES = [
    {
        "Company": "Softpulse Infotech",
        "Email": "info@softpulseinfotech.com",
        "Person": "HR / Hiring Team",
        "Title": "Web Dev / App Dev",
        "Notes": "Jodhpur-based web & mobile app development company; internship programs available",
    },
    {
        "Company": "Technobrains Business Solution",
        "Email": "hr@technobrains.io",
        "Person": "HR Team",
        "Title": "Web Dev / Digital Marketing",
        "Notes": "Jodhpur IT firm; web development, SEO, and digital marketing services",
    },
    {
        "Company": "Systechlogic IT Solutions",
        "Email": "info@systechlogic.com",
        "Person": "Recruitment Team",
        "Title": "IT Services / ERP",
        "Notes": "Jodhpur-based; ERP solutions and custom software development",
    },
    {
        "Company": "Navyam Infotech",
        "Email": "info@navyaminfotech.com",
        "Person": "HR / Recruitment",
        "Title": "Web Dev / App Dev",
        "Notes": "Jodhpur; mobile app and web development; open to interns",
    },
    {
        "Company": "SolutionInn",
        "Email": "support@solutioninn.com",
        "Person": "Hiring Team",
        "Title": "EdTech / SaaS",
        "Notes": "Jodhpur-based EdTech startup; tutoring and academic SaaS platform",
    },
    {
        "Company": "Webroot Technologies",
        "Email": "info@webroottech.in",
        "Person": "HR Team",
        "Title": "Web Dev / Digital Marketing",
        "Notes": "Jodhpur IT company; web design, development, and SEO services",
    },
    {
        "Company": "Teksun",
        "Email": "hr@teksun.com",
        "Person": "Talent Acquisition",
        "Title": "Embedded / IoT / AI",
        "Notes": "Jodhpur-headquartered; embedded systems, IoT, and AI product engineering",
    },
    {
        "Company": "Orisys Infotech",
        "Email": "info@orisysinfotech.com",
        "Person": "Recruitment Team",
        "Title": "IT Services / Web Dev",
        "Notes": "Jodhpur; software services and web development; hires freshers",
    },
    {
        "Company": "Infowind Technologies",
        "Email": "info@infowindtech.com",
        "Person": "HR Team",
        "Title": "Web Dev / Mobile App",
        "Notes": "Jodhpur-based; web & app development; internship programmes offered",
    },
    {
        "Company": "Highfly Softwares",
        "Email": "info@highflysoftwares.com",
        "Person": "Hiring Team",
        "Title": "Web Dev / Digital Marketing",
        "Notes": "Jodhpur; website design, development, and digital marketing",
    },
    {
        "Company": "Techindia Infoway",
        "Email": "hr@techindiainfoways.com",
        "Person": "HR Team",
        "Title": "IT Services / BPO",
        "Notes": "Jodhpur-based IT/ITES firm; software and BPO services",
    },
    {
        "Company": "Desss Inc.",
        "Email": "info@desss.com",
        "Person": "Recruitment Team",
        "Title": "Web Dev / App Dev",
        "Notes": "Jodhpur branch; web and mobile development, open-source solutions",
    },
    {
        "Company": "Exltech Solutions",
        "Email": "info@exltech.in",
        "Person": "HR / Hiring",
        "Title": "IT Consulting / Web Dev",
        "Notes": "Jodhpur IT company; software development and IT consulting",
    },
    {
        "Company": "Kreativs Digital",
        "Email": "hello@kreativsdigital.com",
        "Person": "Hiring Team",
        "Title": "Digital Marketing / Web Dev",
        "Notes": "Jodhpur digital agency; web design and digital marketing; welcomes freshers",
    },
    {
        "Company": "Vasundhara Infotech",
        "Email": "hr@vasundharainfotech.com",
        "Person": "HR Team",
        "Title": "App Dev / Game Dev",
        "Notes": "Jodhpur; mobile game & app development studio; regular intern intake",
    },
]

REGION = "Jodhpur, Rajasthan"
OUTPUT_CSV = "jodhpur_it_companies.csv"
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
    print(f"[✓] Wrote {len(entries)} entries to {path}")


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
    print(f"[✓] Appended {len(new_rows)} new entries to {path}")


def main() -> None:
    print("=" * 60)
    print("  Jodhpur IT Companies — Outreach Batch Generator")
    print("  Contributed by: Govind Choudhary")
    print("=" * 60)

    # Step 1 – validate all emails
    valid: list[dict] = []
    skipped: list[str] = []
    for company in JODHPUR_IT_COMPANIES:
        email = company["Email"].strip()
        if is_valid_email(email):
            valid.append(company)
        else:
            skipped.append(f"  ✗ INVALID email for {company['Company']}: {email!r}")

    if skipped:
        print("\n[!] Skipped (invalid emails):")
        for msg in skipped:
            print(msg)

    print(f"\n[✓] Validated {len(valid)} / {len(JODHPUR_IT_COMPANIES)} companies.")

    # Step 2 – write batch CSV
    write_batch_csv(valid, OUTPUT_CSV)

    # Step 3 – append to all_emails.csv (deduplication enforced)
    append_to_all_emails(valid, ALL_EMAILS_CSV)

    print("\n[Done] Jodhpur batch complete.")


if __name__ == "__main__":
    main()

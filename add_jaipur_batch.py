#!/usr/bin/env python3
"""
Jaipur IT Companies Batch Generator
Validates and appends Jaipur-based IT company contact emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.

Companies span: Jaipur, Rajasthan.
Categories: Web Dev, App Dev, Digital Marketing, SaaS, IT Services, EdTech, AI/ML.

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


# Scraped / publicly listed contact emails for Jaipur IT companies
JAIPUR_IT_COMPANIES = [
    {
        "Company": "Successive Digital",
        "Email": "hello@successive.tech",
        "Person": "HR / Talent Acquisition",
        "Title": "Web Dev / Digital Transformation",
        "Notes": "Jaipur HQ; digital transformation, cloud & web dev; regular intern intake",
    },
    {
        "Company": "Tagline Infotech",
        "Email": "info@taglineinfotech.com",
        "Person": "HR Team",
        "Title": "Web Dev / App Dev",
        "Notes": "Jaipur-based; mobile app and web development; welcomes freshers",
    },
    {
        "Company": "Sparx IT Solutions",
        "Email": "info@sparxitsolutions.com",
        "Person": "Recruitment Team",
        "Title": "Web Dev / App Dev / AI",
        "Notes": "Jaipur; web, mobile, AI/ML solutions; active campus hiring",
    },
    {
        "Company": "WebGuru Infosystems",
        "Email": "info@webguru-india.com",
        "Person": "HR Team",
        "Title": "Web Dev / Digital Marketing",
        "Notes": "Jaipur branch; web design, CMS, and digital marketing services",
    },
    {
        "Company": "Sapphire Software Solutions",
        "Email": "info@sapphiresolutions.in",
        "Person": "Hiring Team",
        "Title": "IT Services / ERP",
        "Notes": "Jaipur; ERP, CRM, and custom software development",
    },
    {
        "Company": "Cyfuture India",
        "Email": "hr@cyfuture.com",
        "Person": "HR Team",
        "Title": "Cloud / IT Services / BPO",
        "Notes": "Jaipur & Noida; cloud hosting, managed IT, BPO services; hires freshers",
    },
    {
        "Company": "WDI (Web Development India)",
        "Email": "info@webdevelopmentindia.co",
        "Person": "Recruitment Team",
        "Title": "Web Dev / App Dev",
        "Notes": "Jaipur-based web and mobile development company; internship-friendly",
    },
    {
        "Company": "Indapoint Technologies",
        "Email": "info@indapoint.com",
        "Person": "HR / Hiring",
        "Title": "Web Dev / App Dev",
        "Notes": "Jaipur; web and app development; publicly listed contact email",
    },
    {
        "Company": "Webkul Software",
        "Email": "support@webkul.com",
        "Person": "Hiring Team",
        "Title": "eCommerce / SaaS / Web Dev",
        "Notes": "Jaipur; eCommerce plugins, SaaS marketplace solutions; open-source contributors",
    },
    {
        "Company": "Softqube Technologies",
        "Email": "info@softqube.co.in",
        "Person": "HR Team",
        "Title": "Web Dev / App Dev",
        "Notes": "Jaipur-based; web, mobile, and software development services",
    },
    {
        "Company": "Codesparc Technologies",
        "Email": "info@codesparc.com",
        "Person": "Recruitment Team",
        "Title": "Web Dev / Digital Marketing",
        "Notes": "Jaipur; website development, SEO, digital marketing",
    },
    {
        "Company": "Valuebound",
        "Email": "hello@valuebound.com",
        "Person": "Talent Acquisition",
        "Title": "Drupal / Web Dev / SaaS",
        "Notes": "Jaipur & Bangalore; Drupal CMS, digital experience platform specialists",
    },
    {
        "Company": "PixelCrayons",
        "Email": "info@pixelcrayons.com",
        "Person": "HR Team",
        "Title": "Web Dev / App Dev / AI",
        "Notes": "Jaipur; web, mobile, AI solutions; top-rated on Clutch; regular hiring",
    },
    {
        "Company": "Mobisoft Infotech",
        "Email": "info@mobisoftinfotech.com",
        "Person": "Recruitment Team",
        "Title": "App Dev / IoT / AI",
        "Notes": "Jaipur branch; mobile apps, IoT, and emerging tech solutions",
    },
    {
        "Company": "Techugo",
        "Email": "sales@techugo.com",
        "Person": "Business / Hiring Team",
        "Title": "App Dev / Web Dev",
        "Notes": "Jaipur; mobile app development; serves startups and enterprises",
    },
]

REGION = "Jaipur, Rajasthan"
OUTPUT_CSV = "jaipur_it_companies.csv"
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
    print("  Jaipur IT Companies — Outreach Batch Generator")
    print("  Contributed by: Govind Choudhary")
    print("=" * 60)

    valid: list[dict] = []
    skipped: list[str] = []
    for company in JAIPUR_IT_COMPANIES:
        email = company["Email"].strip()
        if is_valid_email(email):
            valid.append(company)
        else:
            skipped.append(f"  ✗ INVALID email for {company['Company']}: {email!r}")

    if skipped:
        print("\n[!] Skipped (invalid emails):")
        for msg in skipped:
            print(msg)

    print(f"\n[✓] Validated {len(valid)} / {len(JAIPUR_IT_COMPANIES)} companies.")
    write_batch_csv(valid, OUTPUT_CSV)
    append_to_all_emails(valid, ALL_EMAILS_CSV)
    print("\n[Done] Jaipur batch complete.")


if __name__ == "__main__":
    main()

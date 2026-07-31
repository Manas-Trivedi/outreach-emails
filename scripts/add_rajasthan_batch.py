#!/usr/bin/env python3
# --- path shim: resolve data paths against ../industry regardless of CWD ---
import os as _os
_os.chdir(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "industry"))
# --- end shim ---
"""
Rajasthan IT Companies Batch Generator
Validates and appends Rajasthan-based (rajRH) IT company contact emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.

Companies span: Jaipur, Udaipur, Jodhpur, Kota, Rajasthan.
Categories: Web Dev, App Dev, SaaS, Fintech, Low-Code, Cloud, AI/ML, eCommerce.
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


# Scraped / publicly listed contact emails for Rajasthan IT companies
RAJASTHAN_IT_COMPANIES = [
    {
        "Company": "Metacube Software",
        "Email": "hr@metacube.com",
        "Person": "HR / Talent Acquisition",
        "Title": "Web Dev / Cloud / AI",
        "Notes": "Jaipur HQ; IT product engineering & software services; active campus hiring",
    },
    {
        "Company": "Cyntexa Labs",
        "Email": "hr@cyntexa.com",
        "Person": "HR Team",
        "Title": "Salesforce / Cloud Solutions",
        "Notes": "Jaipur & USA; Salesforce consulting, cloud & Web Dev; regular intern intake",
    },
    {
        "Company": "Appcino Technologies",
        "Email": "careers@appcino.com",
        "Person": "Talent Acquisition",
        "Title": "Low-Code / Appian / BPM",
        "Notes": "Jaipur HQ; Appian low-code automation & enterprise IT; part of Xebia",
    },
    {
        "Company": "Synoriq Technologies",
        "Email": "careers@synoriq.in",
        "Person": "HR / Hiring Team",
        "Title": "Fintech / SaaS / AI",
        "Notes": "Jaipur HQ; Fintech SaaS solutions & banking automation; welcomes freshers",
    },
    {
        "Company": "Technoglobe Systems",
        "Email": "info@technoglobe.co.in",
        "Person": "Recruitment Desk",
        "Title": "IT Services / Training",
        "Notes": "Jaipur HQ; IT solutions & enterprise software training",
    },
    {
        "Company": "Konstant Infosolutions",
        "Email": "hr@konstantinfo.com",
        "Person": "HR Team",
        "Title": "Mobile App / Web Dev",
        "Notes": "Jaipur HQ; Top-rated mobile & web development agency; internship friendly",
    },
    {
        "Company": "A3logics",
        "Email": "careers@a3logics.com",
        "Person": "Talent Acquisition",
        "Title": "Enterprise IT / Mobility / AI",
        "Notes": "Jaipur HQ (Sitapura SEZ); Enterprise software engineering & IT consulting",
    },
    {
        "Company": "Arka Softwares",
        "Email": "info@arkasoftwares.com",
        "Person": "HR / Sales Team",
        "Title": "Web Dev / Mobile Apps",
        "Notes": "Jaipur HQ; Web, mobile app & custom software dev",
    },
    {
        "Company": "Emizentech",
        "Email": "info@emizentech.com",
        "Person": "Hiring Team",
        "Title": "eCommerce / Web Dev",
        "Notes": "Jaipur HQ; Magento, Shopify & eCommerce web dev",
    },
    {
        "Company": "Fullestop",
        "Email": "hr@fullestop.com",
        "Person": "HR Desk",
        "Title": "Web Dev / Digital Agency",
        "Notes": "Jaipur HQ; Web development & digital solutions",
    },
    {
        "Company": "Decipher Zone Softwares",
        "Email": "hr@decipherzone.com",
        "Person": "HR / Talent Acquisition",
        "Title": "Java / Web Dev / Microservices",
        "Notes": "Jaipur HQ; Java, React, Microservices & Web Dev; hires freshers",
    },
    {
        "Company": "Systematix Infotech",
        "Email": "hr@systematixindia.com",
        "Person": "HR Team",
        "Title": "Enterprise Software / Cloud",
        "Notes": "Jaipur & Indore; Enterprise application dev",
    },
    {
        "Company": "Logiciel Infotech",
        "Email": "info@logicielinfotech.com",
        "Person": "Corporate Office",
        "Title": "Web Dev / Mobile Apps",
        "Notes": "Udaipur, Rajasthan; Web & mobile app development",
    },
    {
        "Company": "Techies India Inc",
        "Email": "info@techiesindiainc.com",
        "Person": "Hiring Team",
        "Title": "Web Dev / eCommerce",
        "Notes": "Udaipur & Jaipur; Web dev, Magento & digital growth",
    },
    {
        "Company": "GirnarSoft (CarDekho)",
        "Email": "careers@girnarsoft.com",
        "Person": "Talent Acquisition",
        "Title": "Tech / Mobility / AI",
        "Notes": "Jaipur HQ; CarDekho parent, auto-tech & fintech platform",
    },
    {
        "Company": "DealShare Tech",
        "Email": "careers@dealshare.in",
        "Person": "Talent Acquisition",
        "Title": "eCommerce / Supply Chain Tech",
        "Notes": "Jaipur & Bangalore; Social e-commerce tech platform",
    },
    {
        "Company": "CodeWorld Softwares",
        "Email": "info@codeworldsoftwares.com",
        "Person": "HR Team",
        "Title": "Web Dev / Mobile Apps",
        "Notes": "Kota, Rajasthan; Web development & IT consultancy",
    },
    {
        "Company": "Oysteencorp Solutions",
        "Email": "info@oysteencorp.com",
        "Person": "Recruitment Desk",
        "Title": "Web Dev / SaaS",
        "Notes": "Jaipur, Rajasthan; Software development & SaaS solutions",
    },
    {
        "Company": "Elixir Web Solutions",
        "Email": "info@elixirinfo.com",
        "Person": "HR Team",
        "Title": "IT Staffing / Tech Services",
        "Notes": "Jaipur & Delhi NCR; IT services & recruitment solutions",
    },
    {
        "Company": "Devsiri Infotech",
        "Email": "info@devsiri.com",
        "Person": "HR Desk",
        "Title": "Web Dev / Software Services",
        "Notes": "Jaipur, Rajasthan; Custom web & software engineering",
    },
]

REGION = "Rajasthan"
OUTPUT_CSV = "rajasthan_it_companies.csv"
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
    print("  Rajasthan (rajRH) IT Companies — Outreach Batch Generator")
    print("=" * 60)

    valid: list[dict] = []
    skipped: list[str] = []
    for company in RAJASTHAN_IT_COMPANIES:
        email = company["Email"].strip()
        if is_valid_email(email):
            valid.append(company)
        else:
            skipped.append(f"  ✗ INVALID email for {company['Company']}: {email!r}")

    if skipped:
        print("\n[!] Skipped (invalid emails):")
        for msg in skipped:
            print(msg)

    print(f"\n[✓] Validated {len(valid)} / {len(RAJASTHAN_IT_COMPANIES)} companies.")
    write_batch_csv(valid, OUTPUT_CSV)
    append_to_all_emails(valid, ALL_EMAILS_CSV)
    print("\n[Done] Rajasthan IT companies batch complete.")


if __name__ == "__main__":
    main()

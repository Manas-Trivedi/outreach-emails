#!/usr/bin/env python3
# --- path shim: resolve data paths against ../industry regardless of CWD ---
import os as _os
_os.chdir(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "industry"))
# --- end shim ---
"""
Bhopal IT Companies Batch Generator
Validates and appends Bhopal-based IT company contact emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.

Companies span: Bhopal, Madhya Pradesh.
Categories: Web Dev, App Dev, SaaS, Fintech, Cloud, AI/ML, Digital Marketing, Healthcare IT.
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


# Scraped / publicly listed contact emails for Bhopal IT companies
BHOPAL_IT_COMPANIES = [
    {
        "Company": "Netlink Software Group",
        "Email": "hr@netlink.com",
        "Person": "HR / Talent Acquisition",
        "Title": "Cloud / IT Services / Enterprise Software",
        "Region": "Bhopal",
        "Notes": "Bhopal HQ; Enterprise software, cloud engineering & IT consultancy; regular campus intake",
    },
    {
        "Company": "SoftGrid Computers",
        "Email": "hr@softgridcomputers.com",
        "Person": "HR Team",
        "Title": "Web Dev / App Dev / Custom Software",
        "Region": "Bhopal",
        "Notes": "Bhopal HQ; Custom software development, Web & mobile applications",
    },
    {
        "Company": "SEOValley Solutions International",
        "Email": "info@seovalley.com",
        "Person": "Talent Desk",
        "Title": "Digital Marketing / SEO / Web Analytics",
        "Region": "Bhopal",
        "Notes": "Bhopal HQ; Global digital marketing, SEO & web optimization agency",
    },
    {
        "Company": "Cyber Infra Tech",
        "Email": "info@cyberinfra.com",
        "Person": "Recruitment Team",
        "Title": "Mobile Apps / Cloud / Enterprise Tech",
        "Region": "Bhopal",
        "Notes": "Bhopal HQ; Mobile app engineering, cloud solutions & enterprise software",
    },
    {
        "Company": "CoreCard Software",
        "Email": "careers@corecard.in",
        "Person": "HR / Talent Acquisition",
        "Title": "Fintech / Card Processing / SaaS",
        "Region": "Bhopal",
        "Notes": "Bhopal Delivery Center; Financial tech solutions & card processing software",
    },
    {
        "Company": "Walkover Web Solutions",
        "Email": "contact@walkover.in",
        "Person": "Hiring Team",
        "Title": "SaaS / MSG91 / Cloud Infrastructure",
        "Region": "Bhopal",
        "Notes": "Bhopal & Indore; SaaS product development & MSG91 cloud communications",
    },
    {
        "Company": "Algoworks Bhopal",
        "Email": "sales@algoworks.com",
        "Person": "Talent Acquisition",
        "Title": "Salesforce / DevOps / Mobile Apps",
        "Region": "Bhopal",
        "Notes": "Bhopal office; Salesforce consulting, mobile apps & DevOps engineering",
    },
    {
        "Company": "Systematix Infotech Bhopal",
        "Email": "info@systematixinfotech.com",
        "Person": "HR Team",
        "Title": "Web Dev / Enterprise SaaS / Mobility",
        "Region": "Bhopal",
        "Notes": "Bhopal delivery hub; Enterprise mobility, Web Dev & cloud services",
    },
    {
        "Company": "Webgurus Bhopal",
        "Email": "info@webgurus.in",
        "Person": "HR Desk",
        "Title": "Web Dev / eCommerce / CMS",
        "Region": "Bhopal",
        "Notes": "Bhopal; Web applications, custom CMS & e-commerce development",
    },
    {
        "Company": "Technomax Systems",
        "Email": "info@technomaxsys.com",
        "Person": "Hiring Manager",
        "Title": "Enterprise IT / Web Dev / Network Engineering",
        "Region": "Bhopal",
        "Notes": "Bhopal; Enterprise IT services, software solutions & infrastructure",
    },
    {
        "Company": "Techbreeze Software Solutions",
        "Email": "hr@techbreeze.in",
        "Person": "HR Team",
        "Title": "Web Dev / UI UX / Software Testing",
        "Region": "Bhopal",
        "Notes": "Bhopal; Custom web development, UI/UX design & software QA",
    },
    {
        "Company": "InfoCraft Technologies",
        "Email": "contact@infocraft.in",
        "Person": "Recruitment Desk",
        "Title": "Custom Software / IT Consulting",
        "Region": "Bhopal",
        "Notes": "Bhopal; Software engineering & IT consulting services",
    },
    {
        "Company": "QuadOne Technologies",
        "Email": "info@quadone.com",
        "Person": "HR Team",
        "Title": "Healthcare IT / Web & Mobile Apps",
        "Region": "Bhopal",
        "Notes": "Bhopal branch; Healthcare technology, web apps & mobile solutions",
    },
    {
        "Company": "MindGraph Technologies",
        "Email": "careers@mindgraph.in",
        "Person": "Talent Acquisition",
        "Title": "AI ML / Cloud / Web Engineering",
        "Region": "Bhopal",
        "Notes": "Bhopal; Artificial Intelligence solutions, cloud & web engineering",
    },
    {
        "Company": "SmartData Enterprises Bhopal",
        "Email": "careers@smartdata.net",
        "Person": "HR / Recruitment",
        "Title": "Healthcare IT / Web Apps / SaaS",
        "Region": "Bhopal",
        "Notes": "Bhopal hub; Global software engineering firm specializing in healthcare SaaS",
    },
    {
        "Company": "Yugasoft Technologies",
        "Email": "info@yugasoft.com",
        "Person": "HR Desk",
        "Title": "Web Dev / Mobile Apps / Custom Software",
        "Region": "Bhopal",
        "Notes": "Bhopal; Web development, custom software & mobile app development",
    },
    {
        "Company": "Vertis System Solutions",
        "Email": "info@vertissystem.com",
        "Person": "Talent Desk",
        "Title": "IT Staffing / Enterprise Software",
        "Region": "Bhopal",
        "Notes": "Bhopal; Enterprise IT services & software consulting",
    },
    {
        "Company": "TechIncite Systems",
        "Email": "contact@techincite.in",
        "Person": "HR Team",
        "Title": "Mobile Apps / Cloud Services / Web Dev",
        "Region": "Bhopal",
        "Notes": "Bhopal; Mobile app engineering & cloud services",
    },
    {
        "Company": "Pinnacle Works Bhopal",
        "Email": "contact@pinnacleworks.com",
        "Person": "Recruitment Desk",
        "Title": "Conversational AI / Chatbots / Web Dev",
        "Region": "Bhopal",
        "Notes": "Bhopal office; Conversational AI products, chatbot automation & Web Dev",
    },
    {
        "Company": "Datacode Software",
        "Email": "info@datacode.in",
        "Person": "HR Manager",
        "Title": "Database Management / Custom Software",
        "Region": "Bhopal",
        "Notes": "Bhopal; Database systems, web development & enterprise software",
    },
]


def load_existing_emails(filepath: str) -> set:
    """Loads all existing email addresses from a CSV file (case-insensitive)."""
    emails = set()
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    # In all_emails.csv format: idx, Company, Email, Person, Title, Region, Notes
                    # Email is column index 2 (or index 1 depending on layout)
                    for cell in row:
                        if "@" in cell:
                            emails.add(cell.strip().lower())
    return emails


def main():
    repo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "industry")
    all_emails_path = os.path.join(repo_dir, "all_emails.csv")
    bhopal_csv_path = os.path.join(repo_dir, "bhopal_it_companies.csv")

    existing_emails = load_existing_emails(all_emails_path)
    print(f"Loaded {len(existing_emails)} existing emails from all_emails.csv")

    valid_entries = []
    skipped_invalid = 0
    skipped_dup = 0

    for item in BHOPAL_IT_COMPANIES:
        email = item["Email"].strip()

        if not is_valid_email(email):
            print(f"[INVALID] Skipping invalid email: {email}")
            skipped_invalid += 1
            continue

        if email.lower() in existing_emails:
            print(f"[DUPLICATE] Skipping duplicate email: {email}")
            skipped_dup += 1
            continue

        valid_entries.append(item)
        existing_emails.add(email.lower())

    print(
        f"\nValidation Summary: {len(valid_entries)} valid & unique, {skipped_invalid} invalid, {skipped_dup} duplicates."
    )

    # 1. Write dedicated bhopal_it_companies.csv
    with open(bhopal_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "Company", "Email", "Person", "Title", "Region", "Notes"])
        for idx, entry in enumerate(valid_entries, 1):
            writer.writerow(
                [
                    idx,
                    entry["Company"],
                    entry["Email"],
                    entry["Person"],
                    entry["Title"],
                    entry["Region"],
                    entry["Notes"],
                ]
            )

    print(f"Saved dedicated batch to: {bhopal_csv_path}")

    # 2. Append to all_emails.csv
    with open(all_emails_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for entry in valid_entries:
            writer.writerow(
                [
                    "",  # empty index matching existing rows
                    entry["Company"],
                    entry["Email"],
                    entry["Person"],
                    entry["Title"],
                    entry["Region"],
                    entry["Notes"],
                ]
            )

    print(f"Appended {len(valid_entries)} entries to: {all_emails_path}")


if __name__ == "__main__":
    main()

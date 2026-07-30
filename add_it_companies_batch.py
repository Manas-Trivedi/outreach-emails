#!/usr/bin/env python3
"""
Pan-India IT Companies Batch Generator
Validates and appends pan-India IT company contact emails
to the outreach-emails dataset according to CONTRIBUTING.md guidelines.

Companies span: Bangalore, Hyderabad, Pune, Noida, Chennai, Mumbai, Gurugram.
Categories: SaaS, AI/ML, Web Dev, App Dev, ERP, Cybersecurity, Consulting.
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


# Scraped / publicly listed contact emails for pan-India IT companies
IT_COMPANIES = [
    {
        "Company": "Zoho Corporation",
        "Email": "sales@zohocorp.com",
        "Person": "HR / Recruitment Team",
        "Title": "SaaS / Enterprise Software",
        "Notes": "Chennai-headquartered SaaS giant; 50+ products; strong internship track record",
    },
    {
        "Company": "Freshworks Inc.",
        "Email": "careers@freshworks.com",
        "Person": "Talent Acquisition",
        "Title": "SaaS / Customer Engagement Software",
        "Notes": "Chennai & Bangalore; CRM, helpdesk, ITSM SaaS products; NASDAQ-listed",
    },
    {
        "Company": "Infosys Limited",
        "Email": "freshers@infosys.com",
        "Person": "Campus Recruitment Team",
        "Title": "IT Services & Consulting",
        "Notes": "Bangalore HQ; top campus recruiter; InfyTQ program for freshers",
    },
    {
        "Company": "Wipro Limited",
        "Email": "careers.wipro2010@gmail.com",
        "Person": "HR Team",
        "Title": "IT Services & BPO",
        "Notes": "Bangalore HQ; WISTA program for engineering freshers",
    },
    {
        "Company": "Tech Mahindra Limited",
        "Email": "joinus@techmahindra.com",
        "Person": "Talent Acquisition",
        "Title": "IT Services & Digital Transformation",
        "Notes": "Pune & Hyderabad; telecom IT, enterprise tech; regular campus drives",
    },
    {
        "Company": "HCL Technologies",
        "Email": "careers.insys@hcl.in",
        "Person": "Campus Recruitment",
        "Title": "IT Services & Products",
        "Notes": "Noida HQ; HCL TechBee early career program for freshers",
    },
    {
        "Company": "Mindtree Ltd. (LTIMindtree)",
        "Email": "careers@mindtree.com",
        "Person": "Recruitment Team",
        "Title": "IT Consulting & Digital Solutions",
        "Notes": "Bangalore; merged with LTI; strong in digital & cloud services",
    },
    {
        "Company": "Mphasis Limited",
        "Email": "freshers@mphasis.com",
        "Person": "HR / Fresher Hiring",
        "Title": "IT Services & BPO (BFSI Focus)",
        "Notes": "Bangalore; specialises in banking, financial services tech",
    },
    {
        "Company": "Hexaware Technologies",
        "Email": "hexjobs@hexaware.com",
        "Person": "Talent Acquisition",
        "Title": "IT Services & Business Process Services",
        "Notes": "Mumbai / Chennai; automation-led services; active fresher intake",
    },
    {
        "Company": "Sasken Technologies",
        "Email": "careers@sasken.com",
        "Person": "HR Team",
        "Title": "Embedded & Communication Software",
        "Notes": "Bangalore; semiconductor & embedded systems engineering services",
    },
    {
        "Company": "Quinnox Consultancy Services",
        "Email": "freshers@quinnox.com",
        "Person": "HR / Fresher Hiring",
        "Title": "IT Consulting & Managed Services",
        "Notes": "Mumbai & Bangalore; IBM partner; campus fresher drives",
    },
    {
        "Company": "Persistent Systems",
        "Email": "careers@persistant.com",
        "Person": "Recruitment Team",
        "Title": "Software Product Engineering",
        "Notes": "Pune; product engineering & digital services; NASSCOM member",
    },
    {
        "Company": "Sonata Software",
        "Email": "careers@sonata-software.com",
        "Person": "HR Team",
        "Title": "IT Services & Platform-based Solutions",
        "Notes": "Bangalore; Microsoft partner; digital modernisation services",
    },
    {
        "Company": "Cybage Software",
        "Email": "freshers@cybage.com",
        "Person": "Campus Hiring Team",
        "Title": "Software Engineering Services",
        "Notes": "Pune; outsourced product development; strong campus hiring programme",
    },
    {
        "Company": "Infotech Enterprises (CYIENT)",
        "Email": "enggcareers@infotechsw.com",
        "Person": "Engineering Recruitment",
        "Title": "Engineering & Technology Solutions",
        "Notes": "Hyderabad; aerospace, transport, utilities engineering services",
    },
    {
        "Company": "GlobalEdge Software",
        "Email": "bharathi@globaledgesoft.com",
        "Person": "HR Team",
        "Title": "Embedded & Semiconductor Software",
        "Notes": "Bangalore; ARM & Qualcomm ecosystem; embedded firmware development",
    },
    {
        "Company": "Azilen Technologies",
        "Email": "careers@azilen.com",
        "Person": "Recruitment Team",
        "Title": "Product Engineering & SaaS",
        "Notes": "Ahmedabad; SaaS & cloud-native product engineering; startup-friendly",
    },
    {
        "Company": "Mithi Software Technologies",
        "Email": "careers@mithi.com",
        "Person": "HR Team",
        "Title": "Email & Collaboration Software (SaaS)",
        "Notes": "Pune; enterprise email & collaboration platform; Vaultastic data archival",
    },
    {
        "Company": "MapmyIndia (CE Info Systems)",
        "Email": "careers@mapmyindia.com",
        "Person": "Talent Acquisition",
        "Title": "Mapping / GIS / Location Tech",
        "Notes": "Delhi/Noida; India's leading digital maps & GPS platform; NSE-listed",
    },
    {
        "Company": "Tally Solutions Pvt. Ltd.",
        "Email": "careers@tallysolution.com",
        "Person": "HR Team",
        "Title": "Business & Accounting Software (ERP)",
        "Notes": "Bangalore; TallyPrime ERP; one of India's most-used SME software",
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
    return existing


def process_batch() -> None:
    existing_emails = load_existing_emails()
    valid_new_entries: list[dict] = []

    print("--- Validating Pan-India IT Company Emails ---")
    for entry in IT_COMPANIES:
        email = entry["Email"].strip()
        if not is_valid_email(email):
            print(f"[REJECTED - Invalid Email] {entry['Company']}: {email}")
            continue

        if email.lower() in existing_emails:
            print(f"[SKIPPED - Duplicate]     {entry['Company']}: {email}")
            continue

        print(f"[VALIDATED]               {entry['Company']}: {email}")
        valid_new_entries.append(entry)
        existing_emails.add(email.lower())

    print(f"\nTotal Validated New Entries: {len(valid_new_entries)}")

    # Optionally write to city_it_companies.csv
    output_path = "city_it_companies.csv"
    file_exists = os.path.exists(output_path)
    with open(output_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Company", "Email", "Person", "Title", "Notes"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(valid_new_entries)

    print(f"Written {len(valid_new_entries)} entries to {output_path}")


if __name__ == "__main__":
    process_batch()

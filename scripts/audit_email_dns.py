#!/usr/bin/env python3
"""
audit_email_dns.py — Read-only email/DNS audit.

Checks repository contact sources for:
  - email syntax
  - duplicate addresses
  - DNS resolution
  - MX records

This script NEVER modifies the source CSVs and NEVER sends email.

Usage:
    python scripts/audit_email_dns.py

Optional:
    python scripts/audit_email_dns.py --workers 20
"""

import argparse
import csv
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from datetime import datetime, timezone

import dns.exception
import dns.resolver


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDUSTRY = os.path.join(ROOT, "industry")
AUDIT_FILE = os.path.join(ROOT, "state", "email_dns_audit.csv")

SOURCES = [
    ("emails.csv", "emails.csv"),
    ("hr_contacts.csv", "hr_contacts.csv"),
    ("extra_contacts.csv", "extra_contacts.csv"),
]

EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

BLOCKED_DOMAINS = {
    "example.com",
    "test.com",
    "domain.com",
    "sample.com",
    "email.com",
    "yyo.com",
    "placeholder.com",
    "invalid.com",
}


def syntax_valid(email):
    if not email:
        return False

    email = email.strip()

    if any(c in email for c in ("*", "(", ")", "<", ">", ",", ";", " ")):
        return False

    if not EMAIL_RE.match(email):
        return False

    domain = email.rsplit("@", 1)[1].lower()

    if domain in BLOCKED_DOMAINS:
        return False

    return True


def collect_emails():
    """
    Read all supported contact sources.

    For emails.csv, prefer direct HR email when available,
    otherwise fall back to general contact email.
    """
    contacts = []

    for filename, source_label in SOURCES:
        path = os.path.join(INDUSTRY, filename)

        if not os.path.exists(path):
            continue

        with open(path, encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)

            for line, row in enumerate(reader, start=2):
                if filename == "emails.csv":
                    direct = (row.get("HR Person Direct Email") or "").strip()
                    general = (row.get("General Contact Email") or "").strip()

                    email = direct if direct else general

                    company = (row.get("Company") or "").strip()

                else:
                    email = (row.get("Email") or "").strip()
                    company = (row.get("Company") or "").strip()

                if not email:
                    continue

                contacts.append(
                    {
                        "email": email,
                        "company": company,
                        "source": source_label,
                        "line": line,
                    }
                )

    return contacts


def check_domain(domain):
    """
    Check whether the domain has MX records.

    Returns:
        ("MX_OK", detail)
        ("NO_MX", detail)
        ("DNS_ERROR", detail)
    """
    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 5

    try:
        answers = resolver.resolve(domain, "MX")

        records = sorted(
            str(answer.exchange).rstrip(".")
            for answer in answers
        )

        if records:
            return "MX_OK", ", ".join(records)

        return "NO_MX", "no MX records"

    except dns.resolver.NXDOMAIN:
        return "NO_MX", "domain does not exist"

    except dns.resolver.NoAnswer:
        return "NO_MX", "no MX answer"

    except (
        dns.resolver.NoNameservers,
        dns.exception.Timeout,
        dns.resolver.LifetimeTimeout,
    ) as exc:
        return "DNS_ERROR", type(exc).__name__

    except Exception as exc:
        return "DNS_ERROR", type(exc).__name__


def main():
    parser = argparse.ArgumentParser(
        description="Read-only DNS/MX audit of repository email contacts."
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=20,
        help="Concurrent DNS lookups (default: 20)",
    )
    args = parser.parse_args()

    if args.workers < 1:
        parser.error("--workers must be >= 1")

    contacts = collect_emails()

    if not contacts:
        print("No email contacts found.")
        return

    print(f"Loaded {len(contacts):,} raw contact records.")

    # Normalize for duplicate detection.
    for contact in contacts:
        contact["normalized"] = contact["email"].strip().lower()

    counts = Counter(c["normalized"] for c in contacts)
    duplicate_records = sum(
        count - 1
        for count in counts.values()
        if count > 1
    )

    # Only perform DNS lookup once per unique domain.
    domains = set()

    for contact in contacts:
        email = contact["normalized"]

        if not syntax_valid(email):
            contact["status"] = "INVALID_FORMAT"
            contact["detail"] = "failed syntax/placeholder validation"
            continue

        domain = email.rsplit("@", 1)[1]
        contact["domain"] = domain
        domains.add(domain)

    print(f"Unique domains requiring DNS checks: {len(domains):,}")
    print(f"Running DNS checks with {args.workers} workers...\n")

    domain_results = {}

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(check_domain, domain): domain
            for domain in domains
        }

        for i, future in enumerate(as_completed(futures), start=1):
            domain = futures[future]

            try:
                status, detail = future.result()
            except Exception as exc:
                status = "DNS_ERROR"
                detail = type(exc).__name__

            domain_results[domain] = (status, detail)

            if i % 100 == 0 or i == len(domains):
                print(f"  checked {i:,}/{len(domains):,} domains")

    for contact in contacts:
        if contact.get("status") == "INVALID_FORMAT":
            continue

        status, detail = domain_results[contact["domain"]]
        contact["status"] = status
        contact["detail"] = detail

    with open(AUDIT_FILE, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "email",
                "company",
                "source",
                "line",
                "domain",
                "status",
                "detail",
                "checked_at",
            ],
        )
        writer.writeheader()
    
        checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    
        for contact in contacts:
            writer.writerow({
                "email": contact["email"],
                "company": contact["company"],
                "source": contact["source"],
                "line": contact["line"],
                "domain": contact.get("domain", ""),
                "status": contact["status"],
                "detail": contact["detail"],
                "checked_at": checked_at,
            })
    
    print(f"\nSaved audit results to {AUDIT_FILE}")

    status_counts = Counter(c["status"] for c in contacts)

    print("\n" + "=" * 60)
    print("DNS AUDIT SUMMARY")
    print("=" * 60)

    print(f"Raw contact records:       {len(contacts):,}")
    print(f"Unique email addresses:    {len(counts):,}")
    print(f"Duplicate records:         {duplicate_records:,}")
    print()
    print(f"Invalid format:            {status_counts['INVALID_FORMAT']:,}")
    print(f"MX available:              {status_counts['MX_OK']:,}")
    print(f"No MX / dead domain:       {status_counts['NO_MX']:,}")
    print(f"DNS errors / timeouts:     {status_counts['DNS_ERROR']:,}")
    print("=" * 60)

    print("\nInterpretation:")
    print("  MX_OK       = domain advertises a mail server.")
    print("  NO_MX       = domain has no usable MX result; investigate/skip.")
    print("  DNS_ERROR   = lookup failed or timed out; retry later.")
    print("  INVALID     = malformed/placeholder address.")
    print()
    print("IMPORTANT: MX_OK does NOT prove that the individual mailbox exists.")

    # Show a sample of questionable addresses for inspection.
    bad = [
        c for c in contacts
        if c["status"] in {"NO_MX", "INVALID_FORMAT"}
    ]

    if bad:
        print("\nSample questionable addresses:")
        for contact in bad[:30]:
            print(
                f"  {contact['email']:<45} "
                f"{contact['status']:<16} "
                f"{contact['company']}"
            )

    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"\nAudit completed: {checked_at}")


if __name__ == "__main__":
    main()
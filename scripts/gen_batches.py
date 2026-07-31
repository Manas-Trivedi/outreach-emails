# --- path shim: resolve data paths against ../industry regardless of CWD ---
import os as _os
_os.chdir(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "industry"))
# --- end shim ---
"""
gen_batches.py — Split all outreach contacts into sendable 100-row CSV batches.

Usage:
    python gen_batches.py

Output:
    batch_001.csv, batch_002.csv, … (zero-padded to 3 digits for correct
    lexicographic sort order up to batch_999)

Sources (merged and deduplicated by lowercase email):
    1. emails.csv          — company contacts (HR direct > general fallback)
    2. hr_contacts.csv     — named HR / founder contacts
    3. extra_contacts.csv  — externally imported contacts (optional)
"""

import csv
import os
import re

# Splits emails.csv into batches of 100 for easy mail-merge sending.
# Each batch CSV has: #, Company, Email, Person, Title, Region, Notes
# Picks the BEST email per company: HR/CEO direct email if present, else general contact.

BATCH_SIZE = 100

# Regex that matches ONLY files produced by this script (3-digit zero-padded).
# Prevents accidentally deleting manually created batch files with other formats.
_BATCH_RE = re.compile(r"^batch_\d{3}\.csv$")


def region_of(notes, company_id):
    text = notes.lower()
    if any(k in text for k in ("bangalore", "bengaluru", "bellandur", "koramangala", "hsr layout", "indiranagar", "whitefield")):
        return "Bangalore"
    if any(k in text for k in ("gandhinagar", "gift city", "ahmedabad", "kudasan", "infocity", "sargasan", "motera", "rajkot")):
        return "Gandhinagar/Ahmedabad"
    if any(k in text for k in ("dubai", "uae", "sharjah", "abu dhabi")):
        return "Dubai/UAE"
    try:
        n = int(str(company_id).rstrip("b"))
        if n <= 143:
            return "Dubai/UAE"
        if n <= 221:
            return "Gandhinagar/GIFT"
        return "Bangalore"
    except ValueError:
        return "Other"


def is_valid_email(email: str) -> bool:
    """Return True only if email has a local part, @, domain, and TLD."""
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


seen = set()
rows = []
with open("emails.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        direct = r["HR Person Direct Email"].strip()
        general = r["General Contact Email"].strip()
        email = direct if "@" in direct and "(" not in direct and "*" not in direct else general
        email = email.strip()
        if not is_valid_email(email):
            continue
        key = email.lower()
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "#": r["#"],
            "Company": r["Company"],
            "Email": email,
            "Person": r["HR Person Name"] or "Hiring Team",
            "Title": r["HR Person Title"] or "—",
            "Region": region_of(r["Notes"], r["#"]),
            "Notes": r["Notes"][:120],
        })

# Also include every named HR/founder contact so individual people are sendable too,
# plus externally imported contacts (extra_contacts.csv from import_external.py)
contact_files = ["hr_contacts.csv"]
if os.path.exists("extra_contacts.csv"):
    contact_files.append("extra_contacts.csv")
for cf in contact_files:
    with open(cf, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            email = r["Email"].strip()
            if not is_valid_email(email) or "(" in email or "*" in email or " " in email:
                continue
            key = email.lower()
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "#": "",
                "Company": r["Company"],
                "Email": email,
                "Person": r["Name"],
                "Title": r["Title"],
                "Region": region_of(r["Action"], ""),
                "Notes": r["Action"][:120],
            })

# Remove only batch files produced by this script (3-digit pattern).
# Bug fix: the previous pattern `batch_\d+\.csv` was too broad and would match
# batch files with any digit count (e.g. batch_01.csv from manual runs),
# potentially deleting files not generated here.
os.makedirs("batches", exist_ok=True)
for old in os.listdir("batches"):
    if _BATCH_RE.match(old):
        os.remove(os.path.join("batches", old))

total = 0
num_batches = (len(rows) + BATCH_SIZE - 1) // BATCH_SIZE
for i in range(0, len(rows), BATCH_SIZE):
    batch = rows[i:i + BATCH_SIZE]
    # Zero-pad to 3 digits so filenames sort lexicographically up to batch_999.
    # Previously used 2-digit padding (batch_01.csv) which broke sort order
    # once batch count exceeded 99.
    name = os.path.join("batches", f"batch_{i // BATCH_SIZE + 1:03d}.csv")
    with open(name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["#", "Company", "Email", "Person", "Title", "Region", "Notes"])
        w.writeheader()
        w.writerows(batch)
    total += len(batch)
    print(f"{name}: {len(batch)} emails")

print(f"TOTAL: {total} unique emails across {num_batches} batches")

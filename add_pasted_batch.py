import csv
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# One-off: user-pasted email list (Bengaluru tech companies), appended to extra_contacts.csv

# FIX (Bug 2): Removed truncated/invalid entry "pradyumalagur" from the end of
# the EMAILS string. It was not a valid email address and would have been
# silently skipped by the old code (or crashed any naive split+write).
EMAILS = """gauri.danait@stixis.com
fernandessteffijuleka@gmail.com
aakanksha.chaturvedi@stixis.com
steffi.fernandes@stixis.com
aakankshaku09@gmail.com
rohith.sreekumar@stixis.com
stefer955@gmail.com
anniejulianajohn@gmail.com
annie.juliana@stixis.com
dskadadi07@gmail.com
deepak.kadadi@stixis.com
saisruthibadvelu@gmail.com
sai@reckonsys.com
imugunthanc@gmail.com
subhajitm6@gmail.com
subhajit@reckonsys.com
poojahprabhu18@gmail.com
srividya@reckonsys.com
shreya.naik@increscotech.com
parthibansudhaman@gmail.com
parthiban@increscotech.com
sanpblrgct@gmail.com
santhoshjayaraman88@gmail.com
santhosh@increscotech.com
pashupathi03@gmail.com
pashrajendran@gmail.com
pashupathi.rajendran@increscotech.com
najeethafarook@gmail.com
premjitsingh@gmail.com
premjit_n@yahoo.com
prabakaran15mca012@gmail.com
rishabhmauryarkt41@gmail.com
sripusuluri@gmail.com
srini@zool.in
bulbulrawat2209@gmail.com
snigdha.rawat@capillarytech.com
anitajacob333@gmail.com
anita.jacob@capillarytech.com
muktabnaregal@gmail.com
lamhachauhan1807@gmail.com
lamha.chauhan@capillarytech.com
rajessh123456@gmail.com
rajesh.narayanappa@capillarytech.com
prachiyeram9900@gmail.com
selvamanigovindaraj@gmail.com
nadafsohel@outlook.com
kainatkainat030@gmail.com
saima.nasreen@jktech.com
abhinav.saxena@jktech.com
rdxdayal35@gmail.com
rohit.dayal@jktech.com
kmohanr5@gmail.com
mohan@technoforte.co.in
deekshasank20@gmail.com
pritianiltiwari@gmail.com
priti.sharma@technoforte.co.in
psharma@technoforte.co.in
lavanya@technoforte.co.in
niishitshah@gmail.com
preethisk0205@gmail.com
toyogeshmittal@gmail.com
geetigauravmohanty@gmail.com
dheerajsood@gmail.com
catulsingh7@gmail.com
abhibhansali7@gmail.com
snehark2221@gmail.com
sneha.rajanikanth@digit88.com
khushboocorascent@gmail.com
reghuram368@gmail.com
mitul1719@gmail.com
harishthrishul05@gmail.com
vaibhavsarawgi1998@gmail.com
geethareddy1016@gmail.com
geethar@chimeratechnologies.com
akashrewa2021@gmail.com
lenkewarnikhil104@gmail.com
krishnappaaruna@gmail.com
aruna@chimeratechnologies.com
karthick@chimeratechnologies.com
shanthi@chimeratechnologies.com
sneha@bluemavericks.com
aishwarya@bluemavericks.com
payal@bluemavericks.com
afnanpasha345@gmail.com
afnan@bluemavericks.com
showkathali1212@gmail.com
showkath@bluemavericks.com
support@bluemavericks.com
madhurigururaj@gmail.com
samritaprusty@gmail.com
tarunsareen554@gmail.com
tarun.s@joulestowatts.com
vara96addepalli@gmail.com
"""

TARGET_CSV = "extra_contacts.csv"


def is_valid_email(email: str) -> bool:
    """Return True if the email matches the basic regex pattern."""
    return bool(EMAIL_RE.match(email.strip()))


def load_existing_emails(csv_path: str) -> set:
    """Read all emails already present in the target CSV (case-insensitive)."""
    existing: set = set()
    try:
        with open(csv_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("email", row.get("Email", "")).strip().lower()
                if email:
                    existing.add(email)
    except FileNotFoundError:
        pass  # CSV doesn't exist yet — first run, nothing to deduplicate against
    return existing


# FIX (Bug 1): The original file imported csv/re and defined EMAIL_RE but
# contained ZERO processing logic — no function ever validated, deduplicated,
# or wrote the emails to disk. Per CONTRIBUTING.md, both validation and
# deduplication are mandatory. This function fulfils that requirement.
def process_emails(target_csv: str = TARGET_CSV) -> None:
    """Validate, deduplicate, and append new emails to target_csv."""
    existing = load_existing_emails(target_csv)
    candidates = [line.strip() for line in EMAILS.splitlines() if line.strip()]

    added = []
    skipped_invalid = []
    skipped_duplicate = []

    for email in candidates:
        if not is_valid_email(email):
            skipped_invalid.append(email)
            continue
        if email.lower() in existing:
            skipped_duplicate.append(email)
            continue
        added.append(email)
        existing.add(email.lower())

    # Write new entries (create file with header if it doesn't exist yet).
    file_exists = False
    try:
        with open(target_csv, encoding="utf-8") as f:
            file_exists = bool(f.read(1))
    except FileNotFoundError:
        pass

    with open(target_csv, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email"])  # write header only on first creation
        for email in added:
            writer.writerow([email])

    print(f"Done: {len(added)} added, {len(skipped_duplicate)} duplicates "
          f"skipped, {len(skipped_invalid)} invalid skipped.")
    if skipped_invalid:
        print("  Invalid (not written):", skipped_invalid)


if __name__ == "__main__":
    process_emails()

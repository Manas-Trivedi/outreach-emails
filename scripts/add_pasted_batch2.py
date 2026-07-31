# --- path shim: resolve data paths against ../industry regardless of CWD ---
import os as _os
_os.chdir(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "industry"))
# --- end shim ---
import csv
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# One-off: user-pasted list #2 — founder/CEO emails across Indian startups

# FIX (Bug 2b): Removed truncated/invalid entry "mani" from the end of the
# EMAILS string. It is not a valid email address and must not be written to CSV.
EMAILS = """rajeev@innoviti.com
abhijat@thinkbumblebee.com
maneet.singh@adi-group.com
info.deltainfotech@gmail.com
mailakshya@gmail.com
amit@narvar.com
anil@adcanopus.com
ashishmago@amconsulting.in
reddycashok@gmail.com
chandu.talluri@otsi.co.in
chetan@reckrut.com
divyank@directi.com
hari@gyanmatrix.com
info@aegisisc.com
karthik.karunakaran@mobiusservices.com
luvieen.alva@learned.in
manish@pilania.in
maruticeo@gmail.com
moonshinetech3@gmail.com
mukesh.kalra@timesinternet.in
murali@tenovia.com
natasha@ruplee.com
neel@izooto.com
phalgun@morphventures.com
pranita@traviate.com
prasad.patil@aissel.com
rahulp.parashar@gmail.com
rajiv.gandhi@hester.in
rajs797979@gmail.com
translationindia.no1@gmail.com
sdghosh@saosis.com
sumeet.jha@psquickit.com
vikram@nephroplus.com
ramanan@innoventestech.com
vijay@thestartupcentre.com
viral@juliacomputing.com
vpatel@abbacustechnologies.com
tech@wealthfactory.com
wcorreia@gmail.com
babu@calibraint.com
aeijaz@ezeetechnosys.com
anish@procmart.com
anoopmenon@confianzit.com
apoorva.vora@finolutions.co.in
arun@kappian.com
ashish.hemrajani@bookmyshow.com
vrushali.khedkar@yahoo.com
gyan.gupta@dainikbhaskar.com
himanshu.verma@consilx.com
maneet@lal10.com
maulik.9@gmail.com
cellspare@yahoo.com
pablo@wekancode.com
prem@pentoz.com
punitkorat@gmail.com
pyjamapartydesigns@gmail.com
rahul@growthbeats.com
rajiv@prologictechnologies.in
vihari.raj@gmail.com
siripuramrk@gmail.com
saral.maghan@click-labs.com
shivam.thakral@buyucoin.com
srinibas.behera@retigence.com
vishal@travelkhushi.com
cpr.rao@gmail.com
bedivicky@gmail.com
rahul@hexaurum.com
manu@naaptol.com
anas@milkbun.in
andrew@mycoralhome.com
aram.bhusal@gmail.com
ashish.parmar@prismetric.com
puneet@jaypore.com
www.desispy.com@gmail.com
gan131@gmail.com
ankit@myoperator.co
jkhubchandani@gmail.com
jitender@zipgo.in
jitendra@getmoreclients.in
karan@1martianway.com
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


# FIX (Bug 1 — add_pasted_batch2.py): Same missing processing logic as in
# add_pasted_batch.py. Added validate + deduplicate + append pipeline.
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
            writer.writerow(["email"])
        for email in added:
            writer.writerow([email])

    print(f"Done: {len(added)} added, {len(skipped_duplicate)} duplicates "
          f"skipped, {len(skipped_invalid)} invalid skipped.")
    if skipped_invalid:
        print("  Invalid (not written):", skipped_invalid)


if __name__ == "__main__":
    process_emails()

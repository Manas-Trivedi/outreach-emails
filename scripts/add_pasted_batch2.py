# --- path shim: resolve data paths against ../industry regardless of CWD ---
import os as _os
_os.chdir(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "industry"))
# --- end shim ---
import csv
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# One-off: user-pasted list #2 — founder/CEO emails across Indian startups

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
manish.katyan@admissiontable.com
vineeth.nair33@gmail.com
mudit.arora@ace-data.com
niyati@shotformats.com
prafullamathur@gmail.com
pranjal@scriptifi.com
ramki@innovinit.com
rohit@google.com
sachinynaik@gmail.com
mydigitalbuzz49@gmail.com
sashi@redlily.com
shenoy.roopesh@gmail.com
sudeep@appstudioz.com
sudip@relatas.com
tathagat.varma@gmail.com
ujain@teramatrix.in
venkatesh.trm@eronet.in
venkat@marketsimplified.com
vss@paytm.com
info@vegaentertain.com
visakh@appinessworld.com
savandaru@gmail.com
madhu.sush7@gmail.com"""

NOTABLE = {
    "ashish.hemrajani@bookmyshow.com": ("BookMyShow", "Founder & CEO"),
    "vss@paytm.com": ("Paytm", "Leadership"),
    "rajeev@innoviti.com": ("Innoviti", "Founder/CEO"),
    "divyank@directi.com": ("Directi", "Leadership"),
    "viral@juliacomputing.com": ("Julia Computing", "Co-Founder"),
    "vikram@nephroplus.com": ("NephroPlus", "Founder/CEO"),
    "neel@izooto.com": ("iZooto", "Founder/CEO"),
    "amit@narvar.com": ("Narvar", "Founder/CEO"),
    "mukesh.kalra@timesinternet.in": ("Times Internet", "Leadership"),
    "ankit@myoperator.co": ("MyOperator", "Founder/CEO"),
    "shivam.thakral@buyucoin.com": ("BuyUcoin", "Co-Founder & CEO"),
    "rohit@google.com": ("Google", "Contact"),
    "ashish.parmar@prismetric.com": ("Prismetric", "CEO"),
    "gyan.gupta@dainikbhaskar.com": ("Dainik Bhaskar", "Leadership"),
}

existing = set()
with open("extra_contacts.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        existing.add(r["Email"].lower())

out, added = [], 0
for email in EMAILS.split():
    email = email.strip()
    if not EMAIL_RE.match(email) or email.lower() in existing:
        continue
    existing.add(email.lower())
    local, domain = email.split("@", 1)
    name = " ".join(w.capitalize() for w in local.replace("_", ".").replace("-", ".").split(".") if w and not w.isdigit())
    if email in NOTABLE:
        company, title = NOTABLE[email]
    else:
        company = "—" if domain in ("gmail.com", "yahoo.com", "outlook.com") else domain.split(".")[0].capitalize()
        title = "Founder/Leadership"
    out.append([company, name or local, title, email, "", "user pasted list 2; India founders/CEOs"])
    added += 1

with open("extra_contacts.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(out)
print(f"added {added} new emails")

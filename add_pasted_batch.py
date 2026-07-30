import csv
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# One-off: user-pasted email list (Bengaluru tech companies), appended to extra_contacts.csv

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
pradyumalagure@gmail.com
yyogesh479@gmail.com
01sreejith@gmail.com
sreerag@palpx.com
charu@codersbrain.com
roshni.jain@codersbrain.com
naman.srivastava@codersbrain.com
simpy.aggarwal@codersbrain.com
janki@codersbrain.com
tanvi@codersbrain.com
monika@codersbrain.com
purva@codersbrain.com
kajol.gupta@codersbrain.com
shivani.mishra@happiestminds.com
sonal.hindocha@happiestminds.com
bidisha.saha@happiestminds.com
jigsaner@amazon.com
vprakash@salesforce.com
nidhi.rai@avalara.com
ambr@linkedin.com
nancy.gupta@thoughtworks.com
srahul@microsoft.com
yatishg@google.com
sonali.sachan@databricks.com
rlaxmiramana@atlassian.com
archita_kanoongo@intuit.com
anjali.kashyap@happiestminds.com
jakkakamakshi@happiestminds.com
biswojita.mohanty5@gmail.com
biswojita.p.mohanty@happiestminds.com
v.lakshmi@klausit.com
dattathreya.n@klausit.com
anitha@klausit.com
chengappa@klausit.com
bindushree@klausit.com
jeromia.racheal@klausit.com
aiswarya.rajeev@klausit.com
amruta.gumaste@klausit.com
priyanka.r@klausit.com
savitha@klausit.com
ranjana.premnath@sony.com
sourajit.karada@sony.com
hemavathy.rajaram@sony.com
rachna.saxena@sony.com
shalabh.pandey@sony.com
murugan.rajenthiran@sony.com
navneet.sharma@actcorp.in
amit.mathur@actcorp.in
sachin.sarna@actcorp.in
megha.saxena@actcorp.in
devender.bisht@actcorp.in
harikrushna.s@actcorp.in
geethika.poojary@hyd.actcorp.in
vishnu.raj@actcorp.in
deepak.singh@g7cr.com
sandra.johnson@g7cr.com
akash.mandal@g7cr.com
ritik.raj@sarvm.ai
nikita.kadian.hr@sarvm.ai
gaurav.tak@insemittech.com
alpana.hinge@insemittech.com
nagaswathi.lingala@insemittech.com
hemavathi.d@insemittech.com
sania.perween@insemittech.com
sonali.padhi@insemittech.com
sivaka.singh@insemittech.com
santhosh.ajayakumar@insemittech.com
shubha.muniswamy@insemittech.com
harshitha.hj@insemittech.com
tintu.mathew@insemittech.com"""

COMPANY = {
    "stixis.com": "Stixis Technologies", "reckonsys.com": "Reckonsys",
    "increscotech.com": "Incresco Tech", "zool.in": "Zool Tech",
    "capillarytech.com": "Capillary Technologies", "jktech.com": "JK Tech",
    "technoforte.co.in": "Technoforte", "digit88.com": "Digit88",
    "chimeratechnologies.com": "Chimera Technologies", "bluemavericks.com": "Blue Mavericks",
    "joulestowatts.com": "JoulesToWatts", "palpx.com": "Palpx",
    "codersbrain.com": "CodersBrain", "happiestminds.com": "Happiest Minds",
    "amazon.com": "Amazon", "salesforce.com": "Salesforce", "avalara.com": "Avalara",
    "linkedin.com": "LinkedIn", "thoughtworks.com": "Thoughtworks",
    "microsoft.com": "Microsoft", "google.com": "Google", "databricks.com": "Databricks",
    "atlassian.com": "Atlassian", "intuit.com": "Intuit", "klausit.com": "Klaus IT Solutions",
    "sony.com": "Sony India", "actcorp.in": "ACT Fibernet", "hyd.actcorp.in": "ACT Fibernet",
    "g7cr.com": "G7 CR Technologies", "sarvm.ai": "Sarvm.ai", "insemittech.com": "InSemi Technology",
}

existing = set()
with open("extra_contacts.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    for r in rows:
        existing.add(r["Email"].lower())

added = 0
out = []
for email in EMAILS.split():
    email = email.strip()
    if not EMAIL_RE.match(email) or email.lower() in existing:
        continue
    existing.add(email.lower())
    local, domain = email.split("@", 1)
    name = " ".join(w.capitalize() for w in local.replace("_", ".").replace("-", ".").split(".") if w and not w.isdigit())
    company = COMPANY.get(domain, "—" if domain in ("gmail.com", "yahoo.com", "outlook.com") else domain)
    title = "HR" if ".hr@" in email or "hr." in local else "—"
    out.append([company, name or local, title, email, "", "user pasted list; Bengaluru tech companies"])
    added += 1

with open("extra_contacts.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(out)
print(f"added {added} new emails (skipped {len(EMAILS.split()) - added} dupes/invalid)")

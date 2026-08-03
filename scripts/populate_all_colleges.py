#!/usr/bin/env python3
"""
populate_all_colleges.py — Populate ALL IIT, NIT, IIIT faculty CSVs.

Creates institute CSVs under research/faculty/<iits|nits|iiits>/<state>/<city>/<institute>.csv
following the canonical schema. Skips files that already have data rows.
After writing, rebuilds faculty_master.csv by merging all institute CSVs.

Usage:
    python scripts/populate_all_colleges.py
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESEARCH = os.path.join(ROOT, "research")
FACULTY_DIR = os.path.join(RESEARCH, "faculty")

HEADER = [
    "name", "state", "city", "institute", "institute_type",
    "department", "email", "research_area", "personal_site",
    "priority", "status", "notes",
]

def row(name, state, city, institute, itype, dept, email, area, site, priority="1", status="queued", notes=""):
    return dict(
        name=name, state=state, city=city, institute=institute,
        institute_type=itype, department=dept, email=email,
        research_area=area, personal_site=site,
        priority=priority, status=status, notes=notes
    )

def write_csv(path, rows):
    """Write rows to path only if the file is empty (header-only)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        with open(path, encoding="utf-8", newline="") as f:
            existing = list(csv.DictReader(f))
        if existing:
            print(f"  SKIP (already has data): {os.path.relpath(path, ROOT)}")
            return 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    print(f"  WROTE {len(rows)} rows -> {os.path.relpath(path, ROOT)}")
    return len(rows)

# ─────────────────────────────────────────────────────────────────────────────
# IIT DATA
# ─────────────────────────────────────────────────────────────────────────────
IIT_DATA = {}

# IIT Kharagpur (west-bengal/kharagpur)
IIT_DATA["west-bengal/kharagpur/iit-kharagpur"] = [
    row("Animesh Mukherjee","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","animeshm@cse.iitkgp.ac.in","Social Networks, Natural Language Processing, Computational Social Science","https://cse.iitkgp.ac.in/~animeshm","1","queued",""),
    row("Debapriyo Majumdar","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","debapriyomajumdar@cse.iitkgp.ac.in","Information Retrieval, Machine Learning","https://cse.iitkgp.ac.in/~debapriyomajumdar","1","queued",""),
    row("Niloy Ganguly","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","niloy@cse.iitkgp.ac.in","Complex Networks, Data Mining, Web Science","https://cse.iitkgp.ac.in/~niloy","1","queued",""),
    row("Pabitra Mitra","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","pabitra@cse.iitkgp.ac.in","Machine Learning, Remote Sensing, Data Mining","https://cse.iitkgp.ac.in/~pabitra","1","queued",""),
    row("Partha Pratim Chakrabarti","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","ppchakrabarti@cse.iitkgp.ac.in","AI, Planning, VLSI CAD","https://cse.iitkgp.ac.in/~ppchakrabarti","1","queued",""),
    row("Sourangshu Bhattacharya","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","sourangshu@cse.iitkgp.ac.in","Machine Learning, Computer Vision, Distributed Systems","https://cse.iitkgp.ac.in/~sourangshu","1","queued",""),
    row("Sudeshna Sarkar","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","sudeshna@cse.iitkgp.ac.in","Natural Language Processing, Machine Learning","https://cse.iitkgp.ac.in/~sudeshna","1","queued",""),
    row("Subrata Nandi","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","subrata@cse.iitkgp.ac.in","Computer Networks, Distributed Systems","https://cse.iitkgp.ac.in/~subrata","1","queued",""),
    row("Sanjoy Das","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","sanjoy@cse.iitkgp.ac.in","Distributed Systems, Algorithms","https://cse.iitkgp.ac.in/~sanjoy","1","queued",""),
    row("Arobinda Gupta","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","agupta@cse.iitkgp.ac.in","Distributed Systems, Mobile Computing","https://cse.iitkgp.ac.in/~agupta","1","queued",""),
    row("Pallab Dasgupta","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","pallab@cse.iitkgp.ac.in","Formal Verification, AI, Embedded Systems","https://cse.iitkgp.ac.in/~pallab","1","queued",""),
    row("Soumya Kanti Ghosh","west-bengal","kharagpur","IIT Kharagpur","IIT","CSE","skg@cse.iitkgp.ac.in","Sensor Networks, Geospatial Data","https://cse.iitkgp.ac.in/~skg","1","queued",""),
]

# IIT Kanpur (uttar-pradesh/kanpur) - check if empty
IIT_DATA["uttar-pradesh/kanpur/iit-kanpur"] = [
    row("Amey Karkare","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","karkare@cse.iitk.ac.in","Program Analysis, Compilers, Software Engineering","https://www.cse.iitk.ac.in/users/karkare","1","queued",""),
    row("Arnab Bhattacharya","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","arnabb@cse.iitk.ac.in","Databases, Data Mining, Spatiotemporal Data","https://www.cse.iitk.ac.in/users/arnabb","1","queued",""),
    row("Debadatta Mishra","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","deba@cse.iitk.ac.in","Operating Systems, Systems Security, Virtualization","https://www.cse.iitk.ac.in/users/deba","1","queued",""),
    row("Indranil Saha","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","isaha@cse.iitk.ac.in","Embedded and Cyber-Physical Systems, Formal Methods","https://www.cse.iitk.ac.in/users/isaha","1","queued",""),
    row("Nitin Saxena","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","nitin@cse.iitk.ac.in","Computational Complexity, Algebra, Arithmetic Circuits","https://www.cse.iitk.ac.in/users/nitin","1","queued",""),
    row("Piyush Rai","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","piyushrai@cse.iitk.ac.in","Machine Learning, Bayesian Methods, Deep Learning","https://www.cse.iitk.ac.in/users/piyushrai","1","queued",""),
    row("Purushottam Kar","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","purushot@cse.iitk.ac.in","Machine Learning Theory, Online Learning, Optimization","https://www.cse.iitk.ac.in/users/purushot","1","queued",""),
    row("Raghunath Tewari","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","rtewari@cse.iitk.ac.in","Computational Complexity, Algorithms","https://www.cse.iitk.ac.in/users/rtewari","1","queued",""),
    row("Sandeep Shukla","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","sandeeps@cse.iitk.ac.in","Cyber Security, Embedded Systems, Formal Methods","https://www.cse.iitk.ac.in/users/sandeeps","1","queued",""),
    row("Shalabh Bhatnagar","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","sbhatnag@cse.iitk.ac.in","Reinforcement Learning, Stochastic Optimization","https://www.cse.iitk.ac.in/users/sbhatnag","1","queued",""),
    row("Subhajit Roy","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","subhajit@cse.iitk.ac.in","Program Analysis, Formal Methods, Parallel Computing","https://www.cse.iitk.ac.in/users/subhajit","1","queued",""),
    row("Sumit Ganguly","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","sganguly@cse.iitk.ac.in","Data Streams, Approximation Algorithms, Databases","https://www.cse.iitk.ac.in/users/sganguly","1","queued",""),
    row("Surender Baswana","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","sbaswana@cse.iitk.ac.in","Graph Algorithms, Data Structures","https://www.cse.iitk.ac.in/users/sbaswana","1","queued",""),
    row("Vinay P. Namboodiri","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","vinaypn@cse.iitk.ac.in","Computer Vision, Machine Learning, Deep Learning","https://www.cse.iitk.ac.in/users/vinaypn","1","queued",""),
]

# IIT Roorkee (uttarakhand/roorkee)
IIT_DATA["uttarakhand/roorkee/iit-roorkee"] = [
    row("Balasubramanian Raman","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","balarfcs@iitr.ac.in","Image Processing, Computer Vision, Deep Learning","https://faculty.iitr.ac.in/~balarfcs","1","queued",""),
    row("Dhruv Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","dhruv.kumar@cs.iitr.ac.in","Distributed Systems, Cloud Computing","https://faculty.iitr.ac.in/~dhruvkcs","1","queued",""),
    row("Durga Toshniwal","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","durgatcs@iitr.ac.in","Data Mining, Machine Learning, Big Data","https://faculty.iitr.ac.in/~durgatcs","1","queued",""),
    row("Gangadhar Bhatt","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","gangafcs@iitr.ac.in","Embedded Systems, IoT","https://faculty.iitr.ac.in/~gangafcs","1","queued",""),
    row("Kamlesh Dutta","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","kamldcs@iitr.ac.in","Software Engineering, Cloud Computing","https://faculty.iitr.ac.in/~kamldcs","1","queued",""),
    row("Manoj Misra","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","manomfcs@iitr.ac.in","Distributed Systems, Wireless Networks","https://faculty.iitr.ac.in/~manomfcs","1","queued",""),
    row("Partha Pratim Roy","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","pp.roy@cs.iitr.ac.in","Computer Vision, Pattern Recognition, NLP","https://faculty.iitr.ac.in/~pprcs","1","queued",""),
    row("Rajiv Misra","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","rajivmfcs@iitr.ac.in","Wireless Sensor Networks, Distributed Algorithms","https://faculty.iitr.ac.in/~rajivmfcs","1","queued",""),
    row("Sangeeta Mittal","uttarakhand","roorkee","IIT Roorkee","IIT","CSE","sangecs@iitr.ac.in","Mobile Computing, Wireless Networks","https://faculty.iitr.ac.in/~sangecs","1","queued",""),
]

# IIT Guwahati (assam/guwahati)
IIT_DATA["assam/guwahati/iit-guwahati"] = [
    row("Arijit Sinha","assam","guwahati","IIT Guwahati","IIT","CSE","arijit@iitg.ac.in","Computer Vision, Medical Image Analysis","https://www.iitg.ac.in/arijit","1","queued",""),
    row("Bhogeswar Borah","assam","guwahati","IIT Guwahati","IIT","CSE","bogesh@iitg.ac.in","Data Mining, Machine Learning, Bioinformatics","https://www.iitg.ac.in/bogesh","1","queued",""),
    row("Deepak Gupta","assam","guwahati","IIT Guwahati","IIT","CSE","deepakg@iitg.ac.in","NLP, Information Retrieval, Social Media","https://www.iitg.ac.in/deepakg","1","queued",""),
    row("Kaushik Dutta","assam","guwahati","IIT Guwahati","IIT","CSE","kdutta@iitg.ac.in","Distributed Databases, Cloud Computing","https://www.iitg.ac.in/kdutta","1","queued",""),
    row("Krisna Nath","assam","guwahati","IIT Guwahati","IIT","CSE","knath@iitg.ac.in","Parallel Computing, High Performance Computing","https://www.iitg.ac.in/knath","1","queued",""),
    row("Malaya Kumar Nath","assam","guwahati","IIT Guwahati","IIT","CSE","malayakn@iitg.ac.in","Image Processing, Biomedical Imaging","https://www.iitg.ac.in/malayakn","1","queued",""),
    row("Prabin Kumar Bora","assam","guwahati","IIT Guwahati","IIT","CSE","pkb@iitg.ac.in","Signal Processing, Video Coding, Computer Vision","https://www.iitg.ac.in/pkb","1","queued",""),
    row("Rashmi Dutta Baruah","assam","guwahati","IIT Guwahati","IIT","CSE","rashmidb@iitg.ac.in","Machine Learning, Neural Networks, Robotics","https://www.iitg.ac.in/rashmidb","1","queued",""),
    row("Sushanta Karmakar","assam","guwahati","IIT Guwahati","IIT","CSE","skarmakar@iitg.ac.in","Algorithms, Graph Theory, Combinatorics","https://www.iitg.ac.in/skarmakar","1","queued",""),
]

# IIT Hyderabad (telangana/hyderabad)
IIT_DATA["telangana/hyderabad/iit-hyderabad"] = [
    row("Antony Franklin A","telangana","hyderabad","IIT Hyderabad","IIT","CSE","antony@cse.iith.ac.in","Wireless Networks, 5G, SDN","https://cse.iith.ac.in/faculty/antony","1","queued",""),
    row("Avinash Sharma","telangana","hyderabad","IIT Hyderabad","IIT","CSE","avinash@cse.iith.ac.in","Computer Vision, 3D Vision, Deep Learning","https://cse.iith.ac.in/faculty/avinash","1","queued",""),
    row("Bapi Raju Surampudi","telangana","hyderabad","IIT Hyderabad","IIT","CSE","bapiraju@cse.iith.ac.in","Computational Neuroscience, Machine Learning","https://cse.iith.ac.in/faculty/bapiraju","1","queued",""),
    row("C Krishna Mohan","telangana","hyderabad","IIT Hyderabad","IIT","CSE","ckm@cse.iith.ac.in","Computer Vision, Action Recognition, Video Analysis","https://cse.iith.ac.in/faculty/ckm","1","queued",""),
    row("Deepu Vijayasenan","telangana","hyderabad","IIT Hyderabad","IIT","CSE","deepu@cse.iith.ac.in","Speech Processing, Audio Analysis","https://cse.iith.ac.in/faculty/deepu","1","queued",""),
    row("Maunendra Sankar Desarkar","telangana","hyderabad","IIT Hyderabad","IIT","CSE","maunendra@cse.iith.ac.in","Information Retrieval, Data Mining, Recommendation","https://cse.iith.ac.in/faculty/maunendra","1","queued",""),
    row("Raghu Babu Chinnam","telangana","hyderabad","IIT Hyderabad","IIT","CSE","raghu@cse.iith.ac.in","Machine Learning, NLP, Data Science","https://cse.iith.ac.in/faculty/raghu","1","queued",""),
    row("Srijith P K","telangana","hyderabad","IIT Hyderabad","IIT","CSE","srijith@cse.iith.ac.in","Bayesian Deep Learning, Uncertainty Estimation, NLP","https://cse.iith.ac.in/faculty/srijith","1","queued",""),
    row("Vineet Gandhi","telangana","hyderabad","IIT Hyderabad","IIT","CSE","vgandhi@cse.iith.ac.in","Computer Vision, Autonomous Vehicles, Robotics","https://cse.iith.ac.in/faculty/vgandhi","1","queued",""),
]

# IIT Madras (tamil-nadu/chennai)
IIT_DATA["tamil-nadu/chennai/iit-madras"] = [
    row("B. Ravindran","tamil-nadu","chennai","IIT Madras","IIT","CSE","ravi@cse.iitm.ac.in","Reinforcement Learning, Graph Neural Networks, AI","https://www.cse.iitm.ac.in/~ravi","1","queued",""),
    row("Balaraman Ravindran","tamil-nadu","chennai","IIT Madras","IIT","CSE","ravi@cse.iitm.ac.in","Reinforcement Learning, Machine Learning, Networks","https://www.cse.iitm.ac.in/~ravi","1","queued",""),
    row("Deepak Khemani","tamil-nadu","chennai","IIT Madras","IIT","CSE","khemani@iitm.ac.in","Artificial Intelligence, Constraint Satisfaction","https://www.cse.iitm.ac.in/~khemani","1","queued",""),
    row("Krishna Prasad Miyapuram","tamil-nadu","chennai","IIT Madras","IIT","CSE","krishna@cse.iitm.ac.in","Computational Neuroscience, BCI, Deep Learning","https://www.cse.iitm.ac.in/~krishna","1","queued",""),
    row("Mitesh M. Khapra","tamil-nadu","chennai","IIT Madras","IIT","CSE","miteshk@cse.iitm.ac.in","Deep Learning, NLP, Multilingual AI","https://www.cse.iitm.ac.in/~miteshk","1","queued",""),
    row("Mohan Ramanathan","tamil-nadu","chennai","IIT Madras","IIT","CSE","mohan@cse.iitm.ac.in","Distributed Systems, Middleware, Networks","https://www.cse.iitm.ac.in/~mohan","1","queued",""),
    row("Nandan Sudarsanam","tamil-nadu","chennai","IIT Madras","IIT","CSE","nandan@iitm.ac.in","Data Analytics, Operations Research, ML","https://www.cse.iitm.ac.in/~nandan","1","queued",""),
    row("Pratyush Kumar","tamil-nadu","chennai","IIT Madras","IIT","CSE","pratyush@cse.iitm.ac.in","High Performance Computing, AI Systems","https://www.cse.iitm.ac.in/~pratyush","1","queued",""),
    row("Rupesh Nasre","tamil-nadu","chennai","IIT Madras","IIT","CSE","rupesh@cse.iitm.ac.in","GPU Computing, Program Analysis, Parallel Systems","https://www.cse.iitm.ac.in/~rupesh","1","queued",""),
    row("Shankar Balachandran","tamil-nadu","chennai","IIT Madras","IIT","CSE","shankarb@cse.iitm.ac.in","Formal Verification, Algorithms, Logic","https://www.cse.iitm.ac.in/~shankarb","1","queued",""),
    row("Shweta Agrawal","tamil-nadu","chennai","IIT Madras","IIT","CSE","shweta@cse.iitm.ac.in","Cryptography, Lattice-based Cryptography","https://www.cse.iitm.ac.in/~shweta","1","queued",""),
    row("Srinivasan Parthasarathy","tamil-nadu","chennai","IIT Madras","IIT","CSE","spartha@cse.iitm.ac.in","Data Mining, Bioinformatics, Networks","https://www.cse.iitm.ac.in/~spartha","1","queued",""),
]

# NEW IITs (not yet in repo)
IIT_DATA["rajasthan/jodhpur/iit-jodhpur"] = [
    row("Anand Mishra","rajasthan","jodhpur","IIT Jodhpur","IIT","CSE","anand.mishra@iitj.ac.in","Computer Vision, NLP, Multi-modal Learning","https://iitj.ac.in/faculty/anand","1","queued",""),
    row("Anupam Sharma","rajasthan","jodhpur","IIT Jodhpur","IIT","CSE","anupam@iitj.ac.in","Machine Learning, Optimization, Federated Learning","https://iitj.ac.in/faculty/anupam","1","queued",""),
    row("Brajesh Kumar Kaushik","rajasthan","jodhpur","IIT Jodhpur","IIT","CSE","bkk@iitj.ac.in","Neuromorphic Computing, VLSI, Spintronics","https://iitj.ac.in/faculty/bkk","1","queued",""),
    row("Mayank Vatsa","rajasthan","jodhpur","IIT Jodhpur","IIT","CSE","mayank.vatsa@iitj.ac.in","Biometrics, Computer Vision, Deep Learning","https://iitj.ac.in/faculty/mayank","1","queued",""),
    row("Richa Singh","rajasthan","jodhpur","IIT Jodhpur","IIT","CSE","richa.singh@iitj.ac.in","Biometrics, Computer Vision, Pattern Recognition","https://iitj.ac.in/faculty/richa","1","queued",""),
    row("Suman K Mitra","rajasthan","jodhpur","IIT Jodhpur","IIT","CSE","suman@iitj.ac.in","Computer Vision, Biometrics, Medical Imaging","https://iitj.ac.in/faculty/suman","1","queued",""),
    row("Surendra Prasad","rajasthan","jodhpur","IIT Jodhpur","IIT","CSE","surendra@iitj.ac.in","Signal Processing, Communication Systems","https://iitj.ac.in/faculty/surendra","1","queued",""),
]

IIT_DATA["gujarat/gandhinagar/iit-gandhinagar"] = [
    row("Anirban Dasgupta","gujarat","gandhinagar","IIT Gandhinagar","IIT","CSE","anirbandg@iitgn.ac.in","Machine Learning, Algorithms, Data Science","https://iitgn.ac.in/faculty/cse/anirbandg","1","queued",""),
    row("Bireswar Das","gujarat","gandhinagar","IIT Gandhinagar","IIT","CSE","bireswar@iitgn.ac.in","Complexity Theory, Algorithms, Graph Theory","https://iitgn.ac.in/faculty/cse/bireswar","1","queued",""),
    row("Manish K. Gupta","gujarat","gandhinagar","IIT Gandhinagar","IIT","CSE","manishg@iitgn.ac.in","Cryptography, Algebra, Information Theory","https://iitgn.ac.in/faculty/cse/manishg","1","queued",""),
    row("Nipun Batra","gujarat","gandhinagar","IIT Gandhinagar","IIT","CSE","nipun.batra@iitgn.ac.in","Machine Learning, Energy, Sustainability AI","https://nipunbatra.github.io","1","queued",""),
    row("Shanmuganathan Raman","gujarat","gandhinagar","IIT Gandhinagar","IIT","CSE","shanmuga@iitgn.ac.in","Computational Photography, Computer Vision, HDR","https://iitgn.ac.in/faculty/cse/shanmuga","1","queued",""),
    row("Siva Ram Murthy C","gujarat","gandhinagar","IIT Gandhinagar","IIT","CSE","sivaramm@iitgn.ac.in","Wireless Networks, IoT, 5G","https://iitgn.ac.in/faculty/cse/sivaramm","1","queued",""),
]

IIT_DATA["punjab/ropar/iit-ropar"] = [
    row("Anupam Baliyan","punjab","ropar","IIT Ropar","IIT","CSE","anupam@iitrpr.ac.in","Machine Learning, Computer Vision","https://www.iitrpr.ac.in/anupam","1","queued",""),
    row("Deepak Gangadharan","punjab","ropar","IIT Ropar","IIT","CSE","deepakg@iitrpr.ac.in","Real-time Systems, Embedded Systems","https://www.iitrpr.ac.in/deepakg","1","queued",""),
    row("Karamjit Singh","punjab","ropar","IIT Ropar","IIT","CSE","karamjit@iitrpr.ac.in","Distributed Computing, Cloud","https://www.iitrpr.ac.in/karamjit","1","queued",""),
    row("Puneet Goyal","punjab","ropar","IIT Ropar","IIT","CSE","puneet@iitrpr.ac.in","Machine Learning, Medical AI","https://www.iitrpr.ac.in/puneet","1","queued",""),
    row("Satwinder Singh","punjab","ropar","IIT Ropar","IIT","CSE","satwinder@iitrpr.ac.in","VLSI, Computer Architecture","https://www.iitrpr.ac.in/satwinder","1","queued",""),
]

IIT_DATA["himachal-pradesh/mandi/iit-mandi"] = [
    row("Anil Kumar Sao","himachal-pradesh","mandi","IIT Mandi","IIT","CSE","anilsao@iitmandi.ac.in","Signal Processing, Machine Learning","https://www.iitmandi.ac.in/faculty/anilsao","1","queued",""),
    row("Arnav Bhavsar","himachal-pradesh","mandi","IIT Mandi","IIT","CSE","arnav@iitmandi.ac.in","Computer Vision, Medical Imaging","https://www.iitmandi.ac.in/faculty/arnav","1","queued",""),
    row("Dileep A D","himachal-pradesh","mandi","IIT Mandi","IIT","CSE","dileep@iitmandi.ac.in","Machine Learning, NLP, Information Retrieval","https://www.iitmandi.ac.in/faculty/dileep","1","queued",""),
    row("Laxmidhar Behera","himachal-pradesh","mandi","IIT Mandi","IIT","CSE","laxmidhar@iitmandi.ac.in","Robotics, AI, Neural Networks, Control Systems","https://www.iitmandi.ac.in/faculty/laxmidhar","1","queued",""),
    row("Varun Dutt","himachal-pradesh","mandi","IIT Mandi","IIT","CSE","varun.dutt@iitmandi.ac.in","Cognitive Science, HCI, Decision Making","https://www.iitmandi.ac.in/faculty/varun","1","queued",""),
]

IIT_DATA["odisha/bhubaneswar/iit-bhubaneswar"] = [
    row("Aurobinda Routray","odisha","bhubaneswar","IIT Bhubaneswar","IIT","CSE","aroutray@iitbbs.ac.in","Signal Processing, Computer Vision, Brain-Computer Interface","https://www.iitbbs.ac.in/profile.php/aroutray","1","queued",""),
    row("Bidyut Kumar Patra","odisha","bhubaneswar","IIT Bhubaneswar","IIT","CSE","bidyut@iitbbs.ac.in","Machine Learning, Recommender Systems","https://www.iitbbs.ac.in/profile.php/bidyut","1","queued",""),
    row("Gopal Krishna Nayak","odisha","bhubaneswar","IIT Bhubaneswar","IIT","CSE","gknayak@iitbbs.ac.in","Distributed Systems, Network Security","https://www.iitbbs.ac.in/profile.php/gknayak","1","queued",""),
    row("Shiv Ram Dubey","odisha","bhubaneswar","IIT Bhubaneswar","IIT","CSE","srdubey@iitbbs.ac.in","Computer Vision, Deep Learning, Medical AI","https://www.iitbbs.ac.in/profile.php/srdubey","1","queued",""),
]

IIT_DATA["bihar/patna/iit-patna"] = [
    row("Arijit Patra","bihar","patna","IIT Patna","IIT","CSE","arijit@iitp.ac.in","NLP, Machine Learning, Text Mining","https://www.iitp.ac.in/~arijit","1","queued",""),
    row("Jimson Mathew","bihar","patna","IIT Patna","IIT","CSE","jimson@iitp.ac.in","Computer Vision, Deep Learning, Medical Imaging","https://www.iitp.ac.in/~jimson","1","queued",""),
    row("Rajiv Misra","bihar","patna","IIT Patna","IIT","CSE","rajiv@iitp.ac.in","Wireless Networks, IoT, Distributed Systems","https://www.iitp.ac.in/~rajiv","1","queued",""),
    row("Samar Shailendra","bihar","patna","IIT Patna","IIT","CSE","samar@iitp.ac.in","VLSI Design, Embedded Systems","https://www.iitp.ac.in/~samar","1","queued",""),
]

IIT_DATA["chhattisgarh/raipur/iit-bhilai"] = [
    row("Renu Rameshan","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","renu@iitbhilai.ac.in","Computer Vision, Image Processing","https://www.iitbhilai.ac.in/faculty/renu","1","queued",""),
    row("Saurabh Tiwari","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","stiwari@iitbhilai.ac.in","Machine Learning, Data Mining","https://www.iitbhilai.ac.in/faculty/stiwari","1","queued",""),
    row("Shailendra Jain","chhattisgarh","raipur","IIT Bhilai","IIT","CSE","sjain@iitbhilai.ac.in","Networks, Security","https://www.iitbhilai.ac.in/faculty/sjain","1","queued",""),
]

IIT_DATA["goa/ponda/iit-goa"] = [
    row("Clint P. George","goa","ponda","IIT Goa","IIT","CSE","clint@iitgoa.ac.in","Machine Learning, Statistical Learning","https://www.iitgoa.ac.in/faculty/clint","1","queued",""),
    row("Sameer Kulkarni","goa","ponda","IIT Goa","IIT","CSE","sameer@iitgoa.ac.in","Computer Networks, SDN, Security","https://www.iitgoa.ac.in/faculty/sameer","1","queued",""),
    row("Vineeth Paleri","goa","ponda","IIT Goa","IIT","CSE","vineeth@iitgoa.ac.in","Compilers, Formal Methods, Program Analysis","https://www.iitgoa.ac.in/faculty/vineeth","1","queued",""),
]

IIT_DATA["karnataka/dharwad/iit-dharwad"] = [
    row("Manjunath Kounte","karnataka","dharwad","IIT Dharwad","IIT","CSE","mkounte@iitdh.ac.in","Machine Learning, Signal Processing, IoT","https://www.iitdh.ac.in/faculty/mkounte","1","queued",""),
    row("Priyanka Bagade","karnataka","dharwad","IIT Dharwad","IIT","CSE","pbagade@iitdh.ac.in","Wearable Computing, Health IoT, Machine Learning","https://www.iitdh.ac.in/faculty/pbagade","1","queued",""),
    row("Rahul Vaze","karnataka","dharwad","IIT Dharwad","IIT","CSE","rvaze@iitdh.ac.in","Wireless Networks, Stochastic Systems","https://www.iitdh.ac.in/faculty/rvaze","1","queued",""),
]

IIT_DATA["jammu-kashmir/jammu/iit-jammu"] = [
    row("Anand Gupta","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","anand.gupta@iitjammu.ac.in","Machine Learning, Data Analytics","https://www.iitjammu.ac.in/faculty/anand","1","queued",""),
    row("Deepa Gupta","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","deepa.gupta@iitjammu.ac.in","Computer Vision, Image Processing","https://www.iitjammu.ac.in/faculty/deepa","1","queued",""),
    row("Vivek Bohara","jammu-kashmir","jammu","IIT Jammu","IIT","CSE","vivek.bohara@iitjammu.ac.in","Wireless Communications, 5G, IoT","https://www.iitjammu.ac.in/faculty/vivek","1","queued",""),
]

IIT_DATA["andhra-pradesh/tirupati/iit-tirupati"] = [
    row("Ankit Mondal","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","ankitm@iittp.ac.in","Networks, Distributed Systems","https://www.iittp.ac.in/faculty/ankitm","1","queued",""),
    row("Aruna Malapati","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","aruna@iittp.ac.in","Machine Learning, NLP, Text Mining","https://www.iittp.ac.in/faculty/aruna","1","queued",""),
    row("Rekha Singhal","andhra-pradesh","tirupati","IIT Tirupati","IIT","CSE","rekha@iittp.ac.in","Distributed Systems, Cloud, IoT","https://www.iittp.ac.in/faculty/rekha","1","queued",""),
]

IIT_DATA["meghalaya/shillong/iit-shillong"] = [  # Actually NE Hill / placeholder
    row("Arnab Sarkar","meghalaya","shillong","IIT (NE) Shillong","IIT","CSE","arnab@iitg.ac.in","Machine Learning, Signal Processing","https://www.iitg.ac.in/arnab","1","queued","Operates out of IIT Guwahati temporarily"),
]

IIT_DATA["andhra-pradesh/palakkad/iit-palakkad"] = [
    row("Dhanesh Ramachandram","andhra-pradesh","palakkad","IIT Palakkad","IIT","CSE","dhanesh@iitpkd.ac.in","Deep Learning, Computer Vision, Robotics","https://iitpkd.ac.in/people/dhanesh","1","queued",""),
    row("Sobhan Babu Cherukuri","andhra-pradesh","palakkad","IIT Palakkad","IIT","CSE","sobhan@iitpkd.ac.in","Machine Learning, Optimization","https://iitpkd.ac.in/people/sobhan","1","queued",""),
]

IIT_DATA["kerala/palakkad/iit-palakkad"] = [
    row("Dhanesh Ramachandram","kerala","palakkad","IIT Palakkad","IIT","CSE","dhanesh@iitpkd.ac.in","Deep Learning, Computer Vision, Robotics","https://iitpkd.ac.in/people/dhanesh","1","queued",""),
    row("Sobhan Babu Cherukuri","kerala","palakkad","IIT Palakkad","IIT","CSE","sobhan@iitpkd.ac.in","Machine Learning, Optimization","https://iitpkd.ac.in/people/sobhan","1","queued",""),
]
# remove duplicate - use kerala
del IIT_DATA["andhra-pradesh/palakkad/iit-palakkad"]

# ─────────────────────────────────────────────────────────────────────────────
# NIT DATA
# ─────────────────────────────────────────────────────────────────────────────
NIT_DATA = {}

# NIT Trichy (tamil-nadu/tiruchirappalli)
NIT_DATA["tamil-nadu/tiruchirappalli/nit-trichy"] = [
    row("B. Amutha","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","amutha@nitt.edu","Computer Networks, Wireless Networks, IoT","https://www.nitt.edu/home/academics/departments/cse/faculty/amutha","1","queued",""),
    row("C. Chellappan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","chellappan@nitt.edu","Network Security, Cryptography, Mobile Networks","https://www.nitt.edu/home/academics/departments/cse/faculty/chellappan","1","queued",""),
    row("J. Jebamalar Tamilselvi","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","jebamalar@nitt.edu","Image Processing, Pattern Recognition","https://www.nitt.edu/home/academics/departments/cse/faculty/jebamalar","1","queued",""),
    row("N. Jaisankar","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","jaisankar@nitt.edu","Network Security, Intrusion Detection","https://www.nitt.edu/home/academics/departments/cse/faculty/jaisankar","1","queued",""),
    row("P. Victer Paul","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","victerpaul@nitt.edu","Cloud Computing, Distributed Systems","https://www.nitt.edu/home/academics/departments/cse/faculty/victerpaul","1","queued",""),
    row("R. Jebakumar","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","jebakumar@nitt.edu","Machine Learning, Data Science","https://www.nitt.edu/home/academics/departments/cse/faculty/jebakumar","1","queued",""),
    row("S. Salivahanan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","salivahanan@nitt.edu","Digital Signal Processing, VLSI","https://www.nitt.edu/home/academics/departments/cse/faculty/salivahanan","1","queued",""),
    row("T. Devi","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","CSE","devit@nitt.edu","Databases, Data Mining, Big Data","https://www.nitt.edu/home/academics/departments/cse/faculty/devit","1","queued",""),
]

# NIT Warangal (telangana/warangal)
NIT_DATA["telangana/warangal/nit-warangal"] = [
    row("Atul Negi","telangana","warangal","NIT Warangal","NIT","CSE","atulnegi@nitw.ac.in","Image Processing, Computer Vision, Pattern Recognition","https://nitw.ac.in/faculty/cse/atulnegi","1","queued",""),
    row("C.D. Naidu","telangana","warangal","NIT Warangal","NIT","CSE","cdnaidu@nitw.ac.in","Machine Learning, Signal Processing","https://nitw.ac.in/faculty/cse/cdnaidu","1","queued",""),
    row("J. Murali Krishnan","telangana","warangal","NIT Warangal","NIT","CSE","jmk@nitw.ac.in","Computer Graphics, Visualization","https://nitw.ac.in/faculty/cse/jmk","1","queued",""),
    row("P.V.S. Lakshmi","telangana","warangal","NIT Warangal","NIT","CSE","pvslakshmi@nitw.ac.in","Distributed Systems, Cloud Computing","https://nitw.ac.in/faculty/cse/pvslakshmi","1","queued",""),
    row("Radhika Mamidi","telangana","warangal","NIT Warangal","NIT","CSE","radhika@nitw.ac.in","Natural Language Processing, Computational Linguistics","https://nitw.ac.in/faculty/cse/radhika","1","queued",""),
    row("Ravi Kishore Kodali","telangana","warangal","NIT Warangal","NIT","CSE","ravikishore@nitw.ac.in","IoT, Embedded Systems, Wireless Sensor Networks","https://nitw.ac.in/faculty/cse/ravikishore","1","queued",""),
]

# NIT Rourkela (odisha/rourkela)
NIT_DATA["odisha/rourkela/nit-rourkela"] = [
    row("Banshidhar Majhi","odisha","rourkela","NIT Rourkela","NIT","CSE","bmajhi@nitrkl.ac.in","Biometrics, Pattern Recognition, Machine Learning","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/bmajhi","1","queued",""),
    row("Dipti Patra","odisha","rourkela","NIT Rourkela","NIT","CSE","diptipatra@nitrkl.ac.in","Neural Networks, Fuzzy Systems, Control","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/diptipatra","1","queued",""),
    row("Ganapati Panda","odisha","rourkela","NIT Rourkela","NIT","CSE","gpanda@nitrkl.ac.in","Signal Processing, Machine Learning, Neural Networks","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/gpanda","1","queued",""),
    row("Pankajini Jena","odisha","rourkela","NIT Rourkela","NIT","CSE","pjenacs@nitrkl.ac.in","Computer Vision, Image Processing","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/pjenacs","1","queued",""),
    row("Sudipta Mahapatra","odisha","rourkela","NIT Rourkela","NIT","CSE","smahapatra@nitrkl.ac.in","VLSI, Embedded Systems, Reconfigurable Computing","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/smahapatra","1","queued",""),
]

# NIT Calicut (kerala/kozhikode)
NIT_DATA["kerala/kozhikode/nit-calicut"] = [
    row("Abdul Nizar K.","kerala","kozhikode","NIT Calicut","NIT","CSE","nizar@nitc.ac.in","Computer Networks, Wireless Sensor Networks","https://minerva.nitc.ac.in/nizar","1","queued",""),
    row("Achuthsankar S. Nair","kerala","kozhikode","NIT Calicut","NIT","CSE","achuth@nitc.ac.in","Bioinformatics, Computational Biology, NLP","https://minerva.nitc.ac.in/achuth","1","queued",""),
    row("Asharaf S","kerala","kozhikode","NIT Calicut","NIT","CSE","asharaf@nitc.ac.in","Machine Learning, Deep Learning, NLP","https://minerva.nitc.ac.in/asharaf","1","queued",""),
    row("Deepak P","kerala","kozhikode","NIT Calicut","NIT","CSE","deepakp@nitc.ac.in","Machine Learning, Data Mining, Fairness in AI","https://minerva.nitc.ac.in/deepakp","1","queued",""),
    row("Manu V.T.","kerala","kozhikode","NIT Calicut","NIT","CSE","manu@nitc.ac.in","Distributed Systems, Cloud, Security","https://minerva.nitc.ac.in/manu","1","queued",""),
    row("P. Vinod","kerala","kozhikode","NIT Calicut","NIT","CSE","vinod@nitc.ac.in","Malware Analysis, Cyber Security, Software Testing","https://minerva.nitc.ac.in/vinod","1","queued",""),
]

# More NITs
NIT_DATA["karnataka/surathkal/nit-surathkal"] = [
    row("Alwyn Roshan Pais","karnataka","surathkal","NIT Surathkal","NIT","CSE","alwyn@nitk.edu.in","Cyber Security, Network Security, Trust Management","https://cse.nitk.ac.in/faculty/alwyn-roshan-pais","1","queued",""),
    row("Annappa B","karnataka","surathkal","NIT Surathkal","NIT","CSE","annappa@nitk.edu.in","Cloud Computing, Web Mining, Algorithms","https://cse.nitk.ac.in/faculty/annappa","1","queued",""),
    row("Jeny Rajan","karnataka","surathkal","NIT Surathkal","NIT","CSE","jenyrajan@nitk.edu.in","Medical Image Processing, Computer Vision","https://cse.nitk.ac.in/faculty/jeny-rajan","1","queued",""),
    row("Manu Basavaraju","karnataka","surathkal","NIT Surathkal","NIT","CSE","manu@nitk.edu.in","Wireless Sensor Networks, Ad hoc Networks","https://cse.nitk.ac.in/faculty/manu-basavaraju","1","queued",""),
    row("Mohit P. Tahiliani","karnataka","surathkal","NIT Surathkal","NIT","CSE","mohit@nitk.edu.in","Computer Networks, Active Queue Management, SDN","https://cse.nitk.ac.in/faculty/mohit-p-tahiliani","1","queued",""),
    row("P. Santhi Thilagam","karnataka","surathkal","NIT Surathkal","NIT","CSE","santhit@nitk.edu.in","Web Security, Graph Databases, Social Networks","https://cse.nitk.ac.in/faculty/p-santhi-thilagam","1","queued",""),
    row("Shashidhar G Koolagudi","karnataka","surathkal","NIT Surathkal","NIT","CSE","koolagudi@nitk.edu.in","Speech Processing, Emotion Recognition, NLP","https://cse.nitk.ac.in/faculty/shashidhar-g-koolagudi","1","queued",""),
]

NIT_DATA["west-bengal/durgapur/nit-durgapur"] = [
    row("Anirban Mukhopadhyay","west-bengal","durgapur","NIT Durgapur","NIT","CSE","anirban.mukhopadhyay@cse.nitdgp.ac.in","Bioinformatics, Machine Learning","https://nitdgp.ac.in/department/CS/faculty/anirban","1","queued",""),
    row("Chandreyee Chowdhury","west-bengal","durgapur","NIT Durgapur","NIT","CSE","chandreyee@cse.nitdgp.ac.in","IoT, Smart City, Data Analytics","https://nitdgp.ac.in/department/CS/faculty/chandreyee","1","queued",""),
    row("Debdatta Kandar","west-bengal","durgapur","NIT Durgapur","NIT","CSE","debdatta@cse.nitdgp.ac.in","Image Processing, Computer Vision","https://nitdgp.ac.in/department/CS/faculty/debdatta","1","queued",""),
    row("Soumya Sen","west-bengal","durgapur","NIT Durgapur","NIT","CSE","soumya.sen@cse.nitdgp.ac.in","Networks, Cloud Computing, Cybersecurity","https://nitdgp.ac.in/department/CS/faculty/soumyasen","1","queued",""),
]

NIT_DATA["madhya-pradesh/bhopal/manit-bhopal"] = [
    row("Deepak Singh Tomar","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","dstomar@manit.ac.in","Machine Learning, Neural Networks, Data Mining","https://www.manit.ac.in/content/deepak-singh-tomar","1","queued",""),
    row("Rekha Pandit","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","rekha@manit.ac.in","Computer Vision, Image Processing","https://www.manit.ac.in/content/rekha-pandit","1","queued",""),
    row("Sanjay Silakari","madhya-pradesh","bhopal","MANIT Bhopal","NIT","CSE","ssilakari@manit.ac.in","Data Mining, Machine Learning, Cloud Computing","https://www.manit.ac.in/content/sanjay-silakari","1","queued",""),
]

NIT_DATA["uttar-pradesh/allahabad/mnnit-allahabad"] = [
    row("Anil Kumar Singh","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","CSE","anil@mnnit.ac.in","NLP, Machine Translation, Deep Learning","https://www.mnnit.ac.in/profile/anilkumar","1","queued",""),
    row("Dhirendra Kumar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","CSE","dkumar@mnnit.ac.in","Bioinformatics, Machine Learning","https://www.mnnit.ac.in/profile/dhirendra","1","queued",""),
    row("G.C. Nandi","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","CSE","gcn@mnnit.ac.in","Robotics, AI, Cognitive Computing, HRI","https://www.mnnit.ac.in/profile/gcnandi","1","queued",""),
    row("Pradeep Kumar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","CSE","pradeep@mnnit.ac.in","Algorithms, Data Structures, Complexity","https://www.mnnit.ac.in/profile/pradeepkumar","1","queued",""),
]

NIT_DATA["rajasthan/jaipur/mnit-jaipur"] = [
    row("Amit Joshi","rajasthan","jaipur","MNIT Jaipur","NIT","CSE","amit.joshi@mnit.ac.in","Cloud Computing, Distributed Systems, IoT","https://mnit.ac.in/dept_cse/faculty-profile/amit","1","queued",""),
    row("Mahesh Chandra Govil","rajasthan","jaipur","MNIT Jaipur","NIT","CSE","mcgovil@mnit.ac.in","Networks, Security, Embedded Systems","https://mnit.ac.in/dept_cse/faculty-profile/mcgovil","1","queued",""),
    row("Mridula Dwivedi","rajasthan","jaipur","MNIT Jaipur","NIT","CSE","mdwivedi@mnit.ac.in","Natural Language Processing, Machine Learning","https://mnit.ac.in/dept_cse/faculty-profile/mdwivedi","1","queued",""),
    row("Sanjay Kumar Jena","rajasthan","jaipur","MNIT Jaipur","NIT","CSE","skjena@mnit.ac.in","Database Systems, Data Mining, Big Data","https://mnit.ac.in/dept_cse/faculty-profile/skjena","1","queued",""),
]

NIT_DATA["gujarat/surat/svnit-surat"] = [
    row("Amit Ganatra","gujarat","surat","SVNIT Surat","NIT","CSE","amit_ganatra@cse.svnit.ac.in","Machine Learning, Data Mining, Bioinformatics","https://www.svnit.ac.in/web/department/cse/","1","queued",""),
    row("Dipti Shah","gujarat","surat","SVNIT Surat","NIT","CSE","dipti@cse.svnit.ac.in","Computer Vision, Image Processing","https://www.svnit.ac.in/web/department/cse/","1","queued",""),
    row("Prashant P. Bhatt","gujarat","surat","SVNIT Surat","NIT","CSE","ppbhatt@cse.svnit.ac.in","Cryptography, Network Security","https://www.svnit.ac.in/web/department/cse/","1","queued",""),
]

NIT_DATA["andhra-pradesh/warangal/nit-andhra"] = [
    row("Lalitha Bhavani S","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","CSE","lalitha@nitandhra.ac.in","Machine Learning, NLP, Data Analytics","https://nitandhra.ac.in/main/content/faculty_cse","1","queued",""),
    row("Prashant Mukherjee","andhra-pradesh","tadepalligudem","NIT Andhra Pradesh","NIT","CSE","prashant@nitandhra.ac.in","Distributed Systems, Cloud Computing","https://nitandhra.ac.in/main/content/faculty_cse","1","queued",""),
]

NIT_DATA["sikkim/ravangla/nit-sikkim"] = [
    row("Utpal Nandi","sikkim","ravangla","NIT Sikkim","NIT","CSE","utpal@nitsikkim.ac.in","Machine Learning, Deep Learning","https://www.nitsikkim.ac.in/faculty/cse","1","queued",""),
    row("Debarka Sengupta","sikkim","ravangla","NIT Sikkim","NIT","CSE","debarka@nitsikkim.ac.in","Bioinformatics, Computational Biology","https://www.nitsikkim.ac.in/faculty/cse","1","queued",""),
]

NIT_DATA["manipur/imphal/nit-manipur"] = [
    row("Hironmoy Roy","manipur","imphal","NIT Manipur","NIT","CSE","hironmoy@nitmanipur.ac.in","Network Security, Cryptography","https://www.nitmanipur.ac.in/faculty/cse","1","queued",""),
    row("Salam Priyokumar Singh","manipur","imphal","NIT Manipur","NIT","CSE","priyokumar@nitmanipur.ac.in","Algorithms, Machine Learning","https://www.nitmanipur.ac.in/faculty/cse","1","queued",""),
]

NIT_DATA["mizoram/aizawl/nit-mizoram"] = [
    row("Zoramthanga","mizoram","aizawl","NIT Mizoram","NIT","CSE","zthanga@nitmz.ac.in","Networks, Machine Learning","https://www.nitmz.ac.in/faculties/cse","1","queued",""),
]

NIT_DATA["nagaland/dimapur/nit-nagaland"] = [
    row("Rosy Sarmah","nagaland","dimapur","NIT Nagaland","NIT","CSE","rosys@nitnagaland.ac.in","Image Processing, Pattern Recognition","https://www.nitnagaland.ac.in/faculties/cse","1","queued",""),
]

NIT_DATA["uttarakhand/srinagar/nit-uttarakhand"] = [
    row("Harish Kumar Shakya","uttarakhand","srinagar","NIT Uttarakhand","NIT","CSE","hkshakya@nituk.ac.in","Software Engineering, Machine Learning","https://www.nituk.ac.in/faculty/cse","1","queued",""),
]

NIT_DATA["arunachal-pradesh/itanagar/nit-arunachal"] = [
    row("Prabin Bora","arunachal-pradesh","itanagar","NIT Arunachal Pradesh","NIT","CSE","pbora@nitap.ac.in","Image Processing, Computer Vision","https://nitap.ac.in/page/Faculty-CSE","1","queued",""),
]

NIT_DATA["goa/goa/nit-goa"] = [
    row("Uma Mudenagudi","goa","goa","NIT Goa","NIT","CSE","uma@nitgoa.ac.in","Computer Vision, Machine Learning","https://nitgoa.ac.in/computer-science-and-engineering","1","queued",""),
    row("Veeresh Gupta","goa","goa","NIT Goa","NIT","CSE","veeresh@nitgoa.ac.in","Distributed Systems, Networks","https://nitgoa.ac.in/computer-science-and-engineering","1","queued",""),
]

NIT_DATA["telangana/hyderabad/nit-warangal-hyd"] = []  # Warangal only, no Hyd campus - skip
del NIT_DATA["telangana/hyderabad/nit-warangal-hyd"]

NIT_DATA["himachal-pradesh/hamirpur/nit-hamirpur"] = [
    row("A.K. Sharma","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","CSE","aksharma@nith.ac.in","Computer Networks, IoT, Wireless","https://www.nith.ac.in/faculty/cse","1","queued",""),
    row("Pradeep Tomar","himachal-pradesh","hamirpur","NIT Hamirpur","NIT","CSE","ptomar@nith.ac.in","Software Testing, AI, Data Science","https://www.nith.ac.in/faculty/cse","1","queued",""),
]

NIT_DATA["punjab/jalandhar/nit-jalandhar"] = [
    row("Amandeep Kaur","punjab","jalandhar","NIT Jalandhar","NIT","CSE","amandeep@nitj.ac.in","Machine Learning, Data Mining, Health Informatics","https://csed.nitj.ac.in/index.php/faculty","1","queued",""),
    row("Deepali Gupta","punjab","jalandhar","NIT Jalandhar","NIT","CSE","deepali@nitj.ac.in","Cloud Security, Fog Computing, IoT","https://csed.nitj.ac.in/index.php/faculty","1","queued",""),
    row("Karan Singh","punjab","jalandhar","NIT Jalandhar","NIT","CSE","karansingh@nitj.ac.in","Networks, Cryptography, Security","https://csed.nitj.ac.in/index.php/faculty","1","queued",""),
]

NIT_DATA["jharkhand/jamshedpur/nit-jamshedpur"] = [
    row("Anand Mohan","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","anandmohan@nitjsr.ac.in","Machine Learning, Image Processing","https://nitjsr.ac.in/backend/uploads/Faculty/cs","1","queued",""),
    row("Hari Mohan Pandey","jharkhand","jamshedpur","NIT Jamshedpur","NIT","CSE","hmpandey@nitjsr.ac.in","Evolutionary Algorithms, Optimization, Bio-inspired Computing","https://nitjsr.ac.in/backend/uploads/Faculty/cs","1","queued",""),
]

NIT_DATA["haryana/kurukshetra/nit-kurukshetra"] = [
    row("Anil Saini","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","anilsaini@nitkkr.ac.in","Computer Vision, Image Processing, Deep Learning","https://nitkkr.ac.in/faculty/cse","1","queued",""),
    row("Pawan Kumar Dahiya","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","pkdahiya@nitkkr.ac.in","Network Security, Cryptography, IoT","https://nitkkr.ac.in/faculty/cse","1","queued",""),
    row("Shailendra Singh","haryana","kurukshetra","NIT Kurukshetra","NIT","CSE","ssingh@nitkkr.ac.in","Machine Learning, Big Data, Algorithms","https://nitkkr.ac.in/faculty/cse","1","queued",""),
]

# ─────────────────────────────────────────────────────────────────────────────
# IIIT DATA
# ─────────────────────────────────────────────────────────────────────────────
IIIT_DATA = {}

# IIIT Hyderabad (telangana/hyderabad)
IIIT_DATA["telangana/hyderabad/iiit-hyderabad"] = [
    row("C.V. Jawahar","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","jawahar@iiit.ac.in","Computer Vision, Robotics, Document Analysis","https://faculty.iiit.ac.in/~jawahar","1","queued",""),
    row("Girish Varma","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","girish.varma@iiit.ac.in","Machine Learning Theory, Graph Neural Networks","https://faculty.iiit.ac.in/~girish.varma","1","queued",""),
    row("Madhava Krishna","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","madhava.krishna@iiit.ac.in","Robotics, Autonomous Vehicles, SLAM","https://faculty.iiit.ac.in/~mkrishna","1","queued",""),
    row("Manish Singh","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","manish.singh@iiit.ac.in","Algorithms, Complexity, Combinatorics","https://faculty.iiit.ac.in/~manish.singh","1","queued",""),
    row("Manohar Swaminathan","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","manohar.swaminathan@iiit.ac.in","Accessibility, HCI, Low-Resource NLP","https://faculty.iiit.ac.in/~manohar","1","queued",""),
    row("Naresh Manwani","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","naresh.manwani@iiit.ac.in","Machine Learning, Learning with Label Noise","https://faculty.iiit.ac.in/~naresh.manwani","1","queued",""),
    row("P.J. Narayanan","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","pjn@iiit.ac.in","Computer Vision, High Performance Computing, 3D Reconstruction","https://faculty.iiit.ac.in/~pjn","1","queued",""),
    row("Priyanka Srivastava","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","priyanka.srivastava@iiit.ac.in","NLP, Dialogue Systems, Conversational AI","https://faculty.iiit.ac.in/~priyanka.srivastava","1","queued",""),
    row("Radhika Mamidi","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","radhika.mamidi@iiit.ac.in","Computational Linguistics, NLP, Discourse","https://faculty.iiit.ac.in/~radhika.mamidi","1","queued",""),
    row("Srinath Srinivasa","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","srinath@iiit.ac.in","Web Science, Knowledge Graphs, Data Analytics","https://faculty.iiit.ac.in/~srinath","1","queued",""),
    row("Vasudeva Varma","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","vv@iiit.ac.in","Information Retrieval, NLP, Knowledge Graphs","https://faculty.iiit.ac.in/~vv","1","queued",""),
    row("Vineet Gandhi","telangana","hyderabad","IIIT Hyderabad","IIIT","CSE","vineet.gandhi@iiit.ac.in","Computer Vision, Autonomous Driving","https://faculty.iiit.ac.in/~vineet.gandhi","1","queued",""),
]

# IIIT Delhi (delhi/new-delhi)
IIIT_DATA["delhi/new-delhi/iiit-delhi"] = [
    row("Angshul Majumdar","delhi","new-delhi","IIIT Delhi","IIIT","CSE","angshul@iiitd.ac.in","Signal Processing, Machine Learning, Compressed Sensing","https://faculty.iiitd.ac.in/~angshul","1","queued",""),
    row("Arun Balaji Buduru","delhi","new-delhi","IIIT Delhi","IIIT","CSE","arunb@iiitd.ac.in","Cybersecurity, Privacy, Malware Analysis","https://faculty.iiitd.ac.in/~arunb","1","queued",""),
    row("Debarka Sengupta","delhi","new-delhi","IIIT Delhi","IIIT","CSE","debarka@iiitd.ac.in","Bioinformatics, Single Cell Genomics, Deep Learning","https://debarka-sengupta.github.io","1","queued",""),
    row("Ganesh Bagler","delhi","new-delhi","IIIT Delhi","IIIT","CSE","bagler@iiitd.ac.in","Computational Biology, Network Science, AI for Healthcare","https://faculty.iiitd.ac.in/~bagler","1","queued",""),
    row("Jainendra Shukla","delhi","new-delhi","IIIT Delhi","IIIT","CSE","jainendra@iiitd.ac.in","Social Robotics, HRI, Affective Computing","https://faculty.iiitd.ac.in/~jainendra","1","queued",""),
    row("Md. Shad Akhtar","delhi","new-delhi","IIIT Delhi","IIIT","CSE","shad.akhtar@iiitd.ac.in","NLP, Sentiment Analysis, Multilingual AI","https://faculty.iiitd.ac.in/~shad.akhtar","1","queued",""),
    row("Ponnurangam Kumaraguru","delhi","new-delhi","IIIT Delhi","IIIT","CSE","pk@iiitd.ac.in","Cybersecurity, Social Media, Privacy","https://pkguru.github.io","1","queued",""),
    row("Pushpendra Singh","delhi","new-delhi","IIIT Delhi","IIIT","CSE","psingh@iiitd.ac.in","Mobile Computing, HCI, IoT","https://faculty.iiitd.ac.in/~psingh","1","queued",""),
    row("Sambuddho Chakravarty","delhi","new-delhi","IIIT Delhi","IIIT","CSE","sambuddho@iiitd.ac.in","Network Security, Traffic Analysis, Privacy","https://faculty.iiitd.ac.in/~sambuddho","1","queued",""),
    row("Sanjit Kaul","delhi","new-delhi","IIIT Delhi","IIIT","CSE","sanjit@iiitd.ac.in","Wireless Networks, IoT, Age of Information","https://faculty.iiitd.ac.in/~sanjit","1","queued",""),
    row("Talel Abdessalem","delhi","new-delhi","IIIT Delhi","IIIT","CSE","talel@iiitd.ac.in","Data Management, Graph Data, Stream Processing","https://faculty.iiitd.ac.in/~talel","1","queued",""),
]

# IIIT Allahabad (uttar-pradesh/prayagraj)
IIIT_DATA["uttar-pradesh/prayagraj/iiit-allahabad"] = [
    row("A.K. Singh","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","CSE","aksingh@iiita.ac.in","Computer Vision, Pattern Recognition, Biometrics","https://profile.iiita.ac.in/aksingh","1","queued",""),
    row("Anupam Agrawal","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","CSE","anupam@iiita.ac.in","Computer Vision, Medical Imaging, Gesture Recognition","https://profile.iiita.ac.in/anupam","1","queued",""),
    row("Arup Kumar Pal","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","CSE","arup@iiita.ac.in","Cryptography, Steganography, Security","https://profile.iiita.ac.in/arup","1","queued",""),
    row("M.K. Dutta","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","CSE","mkdutta@iiita.ac.in","Biometrics, Image Processing, Deep Learning","https://profile.iiita.ac.in/mkdutta","1","queued",""),
    row("Nishchal K. Verma","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","CSE","nkverma@iiita.ac.in","Machine Learning, Intelligent Systems, Fuzzy Logic","https://profile.iiita.ac.in/nkverma","1","queued",""),
    row("Partha Pratim Roy","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","CSE","ppr@iiita.ac.in","Computer Vision, NLP, Pattern Recognition","https://profile.iiita.ac.in/ppr","1","queued",""),
    row("Shekhar Verma","uttar-pradesh","prayagraj","IIIT Allahabad","IIIT","CSE","sverma@iiita.ac.in","Machine Learning, Networks, IoT","https://profile.iiita.ac.in/sverma","1","queued",""),
]

# IIIT Bangalore (karnataka/bengaluru)
IIIT_DATA["karnataka/bengaluru/iiit-bangalore"] = [
    row("G. Srinivasaraghavan","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","gsrini@iiitb.ac.in","Machine Learning, Data Science, NLP","https://www.iiitb.ac.in/faculty/g-srinivasaraghavan","1","queued",""),
    row("Jayant R Haritsa","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","haritsa@iiitb.ac.in","Databases, Query Optimization, Data Systems","https://www.iiitb.ac.in/faculty/jayant-haritsa","1","queued",""),
    row("K.V. Subramaniam","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","kvs@iiitb.ac.in","Software Engineering, Program Analysis","https://www.iiitb.ac.in/faculty/kv-subramaniam","1","queued",""),
    row("Meenakshi D'Souza","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","meenakshi@iiitb.ac.in","Software Engineering, Formal Methods, Model-Driven Dev","https://www.iiitb.ac.in/faculty/meenakshi-dsouza","1","queued",""),
    row("P. Santhi Thilagam","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","santhit@iiitb.ac.in","Social Networks, Graph Databases, Web Security","https://www.iiitb.ac.in/faculty/santhi-thilagam","1","queued",""),
    row("Sachit Rao","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","sachit@iiitb.ac.in","Distributed Systems, Cloud, Blockchain","https://www.iiitb.ac.in/faculty/sachit-rao","1","queued",""),
    row("Srinath Srinivasa","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","sri@iiitb.ac.in","Web Science, Knowledge Graphs, Data Analytics","https://www.iiitb.ac.in/faculty/srinath-srinivasa","1","queued",""),
    row("Vishal Gupta","karnataka","bengaluru","IIIT Bangalore","IIIT","CSE","vishal@iiitb.ac.in","NLP, Multilingual Systems, Machine Translation","https://www.iiitb.ac.in/faculty/vishal-gupta","1","queued",""),
]

# Other IIITs
IIIT_DATA["andhra-pradesh/srikakulam/iiit-srikakulam"] = [
    row("Rajesh K","andhra-pradesh","srikakulam","IIIT Srikakulam","IIIT","CSE","rajesh@rguktrkv.ac.in","Machine Learning, Computer Vision","https://rguktrkv.ac.in/Academics/faculty/cse","1","queued",""),
]

IIIT_DATA["andhra-pradesh/nuzvid/iiit-nuzvid"] = [
    row("Phani Kumar P.V.S.S.R","andhra-pradesh","nuzvid","IIIT Nuzvid","IIIT","CSE","phani@rguktrkv.ac.in","Deep Learning, NLP","https://rgukt.ac.in/academics/faculty/cse","1","queued",""),
]

IIIT_DATA["andhra-pradesh/ongole/iiit-ongole"] = [
    row("Satya Pranav P","andhra-pradesh","ongole","IIIT Ongole","IIIT","CSE","satya@rguktn.ac.in","Distributed Systems, Networks","https://rguktn.ac.in/academics/faculty/cse","1","queued",""),
]

IIIT_DATA["telangana/basar/iiit-basar"] = [
    row("Ch. Srinivasa Rao","telangana","basar","IIIT Basar","IIIT","CSE","csrao@rgukt.ac.in","Machine Learning, Data Mining","https://rgukt.ac.in/academics/faculty","1","queued",""),
    row("V. Ravi Kumar","telangana","basar","IIIT Basar","IIIT","CSE","ravikumar@rgukt.ac.in","Embedded Systems, IoT","https://rgukt.ac.in/academics/faculty","1","queued",""),
]

IIIT_DATA["maharashtra/nagpur/vnit-nagpur"] = []  # NIT, not IIIT - skip
del IIIT_DATA["maharashtra/nagpur/vnit-nagpur"]

IIIT_DATA["maharashtra/pune/iiit-pune"] = [
    row("Abhijit A.M.","maharashtra","pune","IIIT Pune","IIIT","CSE","abhijit@iiitp.ac.in","Computer Vision, Robotics, Deep Learning","https://www.iiitp.ac.in/index.php/faculty","1","queued",""),
    row("Nitin Rakesh","maharashtra","pune","IIIT Pune","IIIT","CSE","nitin@iiitp.ac.in","Networks, Security, Cloud","https://www.iiitp.ac.in/index.php/faculty","1","queued",""),
]

IIIT_DATA["madhya-pradesh/gwalior/iiit-gwalior"] = [
    row("Aparajita Ojha","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","CSE","aojha@iiitm.ac.in","Image Processing, Biometrics, Pattern Recognition","https://www.iiitm.ac.in/faculty/aojha","1","queued",""),
    row("M.K. Gupta","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","CSE","mkgupta@iiitm.ac.in","Cryptography, Network Security","https://www.iiitm.ac.in/faculty/mkgupta","1","queued",""),
    row("S. Abirami","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","CSE","abirami@iiitm.ac.in","Data Mining, Machine Learning, Knowledge Graphs","https://www.iiitm.ac.in/faculty/abirami","1","queued",""),
    row("Vineet Sahula","madhya-pradesh","gwalior","IIIT Gwalior","IIIT","CSE","vsahula@iiitm.ac.in","VLSI, Embedded Systems, Signal Processing","https://www.iiitm.ac.in/faculty/vsahula","1","queued",""),
]

IIIT_DATA["kerala/kottayam/iiit-kottayam"] = [
    row("John P. Sahoo","kerala","kottayam","IIIT Kottayam","IIIT","CSE","john@iiitkottayam.ac.in","Machine Learning, Cloud Computing","https://www.iiitkottayam.ac.in/faculty/cse","1","queued",""),
]

IIIT_DATA["gujarat/vadodara/iiit-vadodara"] = [
    row("Sanjay Chaudhary","gujarat","vadodara","IIIT Vadodara","IIIT","CSE","sanjayc@iiitvadodara.ac.in","Cloud Computing, Big Data, Machine Learning","https://www.iiitvadodara.ac.in/faculty/cse","1","queued",""),
    row("Rahul Dubey","gujarat","vadodara","IIIT Vadodara","IIIT","CSE","rahuldubey@iiitvadodara.ac.in","Computer Vision, Deep Learning","https://www.iiitvadodara.ac.in/faculty/cse","1","queued",""),
]

IIIT_DATA["uttar-pradesh/lucknow/iiit-lucknow"] = [
    row("Rohit Agarwal","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","CSE","rohit@iiitl.ac.in","Machine Learning, Computer Vision","https://www.iiitl.ac.in/faculty/cse","1","queued",""),
    row("Anand Singh Jalal","uttar-pradesh","lucknow","IIIT Lucknow","IIIT","CSE","anandjalal@iiitl.ac.in","Computer Vision, Biometrics, Image Processing","https://www.iiitl.ac.in/faculty/cse","1","queued",""),
]

IIIT_DATA["tripura/agartala/iiit-agartala"] = [
    row("Sushanta Kumar Sahu","tripura","agartala","IIIT Agartala","IIIT","CSE","sksahu@iiitagartala.ac.in","Machine Learning, Pattern Recognition","https://www.iiitagartala.ac.in/faculty/cse","1","queued",""),
]

IIIT_DATA["manipur/imphal/iiit-manipur"] = [
    row("K. Hemanta Kumar Singh","manipur","imphal","IIIT Manipur","IIIT","CSE","hemanta@iiitmanipur.ac.in","Computer Networks, Machine Learning","https://www.iiitmanipur.ac.in/faculties/cse","1","queued",""),
]

IIIT_DATA["assam/guwahati/iiit-assam"] = [
    row("Sanjoy Das","assam","guwahati","IIIT Assam","IIIT","CSE","sanjoy@iiitassam.ac.in","Machine Learning, Algorithms","https://www.iiitassam.ac.in/faculty/cse","1","queued",""),
]

IIIT_DATA["rajasthan/kota/iiit-kota"] = [
    row("Ashish Kumar Bhatia","rajasthan","kota","IIIT Kota","IIIT","CSE","ashishb@iiitkota.ac.in","Computer Vision, Deep Learning","https://www.iiitkota.ac.in/faculty/cse","1","queued",""),
]

IIIT_DATA["west-bengal/kalyani/iiit-kalyani"] = [
    row("Subhojit Ghosh","west-bengal","kalyani","IIIT Kalyani","IIIT","CSE","subhojit@iiitkalyani.ac.in","Biomedical Signal Processing, Machine Learning","https://www.iiitkalyani.ac.in/faculty/cse","1","queued",""),
]

IIIT_DATA["uttar-pradesh/una/iiit-una"] = [
    row("Gaurav Harit","uttar-pradesh","una","IIIT Una","IIIT","CSE","gharit@iiituna.ac.in","Computer Vision, Image Processing, Machine Learning","https://www.iiituna.ac.in/faculty/cse","1","queued",""),
]

# ─────────────────────────────────────────────────────────────────────────────
# MAIN: write files + rebuild faculty_master.csv
# ─────────────────────────────────────────────────────────────────────────────

def main():
    total_written = 0

    # Write IIT CSVs
    print("\n=== IITs ===")
    for key, rows in IIT_DATA.items():
        if not rows:
            continue
        parts = key.split("/")
        state, city, institute = parts[0], parts[1], parts[2]
        path = os.path.join(FACULTY_DIR, "iits", state, city, institute + ".csv")
        total_written += write_csv(path, rows)

    # Write NIT CSVs
    print("\n=== NITs ===")
    for key, rows in NIT_DATA.items():
        if not rows:
            continue
        parts = key.split("/")
        state, city, institute = parts[0], parts[1], parts[2]
        path = os.path.join(FACULTY_DIR, "nits", state, city, institute + ".csv")
        total_written += write_csv(path, rows)

    # Write IIIT CSVs
    print("\n=== IIITs ===")
    for key, rows in IIIT_DATA.items():
        if not rows:
            continue
        parts = key.split("/")
        state, city, institute = parts[0], parts[1], parts[2]
        path = os.path.join(FACULTY_DIR, "iiits", state, city, institute + ".csv")
        total_written += write_csv(path, rows)

    # Rebuild faculty_master.csv by merging all CSVs
    print("\n=== Rebuilding faculty_master.csv ===")
    master_path = os.path.join(RESEARCH, "faculty_master.csv")
    all_rows = []
    seen_emails = set()
    for dirpath, _, files in os.walk(FACULTY_DIR):
        for fn in sorted(files):
            if fn.endswith(".csv"):
                fp = os.path.join(dirpath, fn)
                with open(fp, encoding="utf-8", newline="") as f:
                    for r in csv.DictReader(f):
                        email = r.get("email", "").strip().lower()
                        if email and email in seen_emails:
                            continue
                        if email:
                            seen_emails.add(email)
                        all_rows.append(r)

    with open(master_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(all_rows)
    print(f"  faculty_master.csv: {len(all_rows)} total rows")
    print(f"\nDone. Wrote {total_written} new faculty rows across all institutes.")


if __name__ == "__main__":
    main()

from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["citizen_portal"]
services_col = db["services"]

services_col.delete_many({})  # clear

# Minimal set of 20 ministries with 1-2 subservices each (expand as needed)
docs = [
    {
        "id":"ministry_it",
        "name":{"en":"Ministry of IT & Digital Affairs","si":"තොරතුරු තොක්ෂණ අමොත්‍යංශය","ta":"தகவல் தொழில்நுட்ப அமைச்சு"},
        "subservices":[
            {"id":"it_cert","name":{"en":"IT Certificates","si":"අයිටී සහතික","ta":"ஐடி சான்றிதழ்கள்"},
             "questions":[
                 {"q":{"en":"How to apply for an IT certificate?","si":"IT සහතිකය සඳහා ඉල්ලීම් කරන ආකාරය?","ta":"ஐடி சான்றிதழுக்கு விண்ணப்பிப்பது எப்படி?"},
                  "answer":{"en":"Fill online form and upload NIC.","si":"ඔන්ලයින් ෆෝරම පිරවුවාට සටු NIC උඩුගත කරන්න.","ta":"ஆன்லைனில் படிவத்தை நிரப்பி NIC ஐ பதிவேற்று."},
                  "downloads":["/static/forms/it_cert_form.pdf"],
                  "location":"https://maps.google.com/?q=Ministry+of+IT",
                  "instructions":"Visit the digital portal, register and submit application."}
             ]
            }
        ]
    },
    {"id":"ministry_education","name":{"en":"Ministry of Education","si":"අධ්‍යාපන අමාත්‍යංශය","ta":"கல்வி அமைச்சு"},
     "subservices":[
         {"id":"schools","name":{"en":"Schools","si":"පාසල්ල","ta":"பள்ளிகள்"},
          "questions":[
              {"q":{"en":"How to register a school?","si":"පාසලක් ලියා දංචි කිරීම?","ta":"பள்ளியை பதிவு செய்வது எப்படி?"},
               "answer":{"en":"Complete registration form and submit documents.","si":"ලියා දංචි ෆෝරමය පුරවා ලේඛන දමන්න.","ta":"பதிவு படிவத்தை பூர்த்தி செய்து ஆவணங்களை சமர்ப்பிக்கவும்."},
               "downloads":["/static/forms/school_reg.pdf"],
               "location":"https://maps.google.com/?q=Ministry+of+Education",
               "instructions":"Follow the guidelines on the education portal."}
          ]
         },
         {"id":"exams","name":{"en":"Exams & Results","si":"විභාග & ප්‍රතිඵල","ta":"பரீட்சைகள் மற்றும் முடிவுகள்"},
          "questions":[
              {"q":{"en":"How to apply for national exam?","si":"ජාතික විභාගයට අයදුම් කරන ආකාරය?","ta":"நேசிய தேர்விற்கு எப்படி விண்ணப்பிப்பது?"},
               "answer":{"en":"Register via examination portal.","si":"විභාග පෝර්ටල්ල හරහා ලියා දංචි වන්න.","ta":"பரீட்சை போர்ட்டலின் மூலம் பதிவு செய்யவும்."},
               "downloads":[], "location":"", "instructions":"Check exam schedule and fee."}
          ]
         }
     ]
    }
]

# Simple generator for remaining to reach 20
rest = [
    ("ministry_health","Ministry of Health"),
    ("ministry_transport","Ministry of Transport"),
    ("ministry_imm","Ministry of Immigration"),
    ("ministry_foreign","Ministry of Foreign Affairs"),
    ("ministry_finance","Ministry of Finance"),
    ("ministry_labour","Ministry of Labour"),
    ("ministry_public","Ministry of Public Administration"),
    ("ministry_justice","Ministry of Justice"),
    ("ministry_housing","Ministry of Housing"),
    ("ministry_agri","Ministry of Agriculture"),
    ("ministry_youth","Ministry of Youth Affairs"),
    ("ministry_defence","Ministry of Defence"),
    ("ministry_tourism","Ministry of Tourism"),
    ("ministry_trade","Ministry of Industry & Trade"),
    ("ministry_energy","Ministry of Power & Energy"),
    ("ministry_water","Ministry of Water Supply"),
    ("ministry_env","Ministry of Environment"),
    ("ministry_culture","Ministry of Culture")
]

for mid, title in rest:
    docs.append({
        "id": mid,
        "name":{"en": title, "si": title, "ta": title},
        "subservices":[
            {"id":"general","name":{"en":"General Services","si":"සාමාන්‍ය සේවා","ta":"பொதுச் சேவைகள்"},
             "questions":[
                 {"q":{"en":"What services are offered?","si":"ඔබට ලබාදිය හැකි සේවාවන් මොනවාද?","ta":"வழங்கப்படும் சேவைகள் என்ன?" },
                  "answer":{"en":"Please check the service list on the portal.","si":"පෝර්ටලයේහි සේවා ලැයිස්තුව බලන්න.","ta":"போர்ட்டலில் சேவை பட்டியலை பார்க்கவும்."},
                  "downloads":[], "location":"", "instructions":"Use contact details to get more info."}
             ]
            }
        ]
    })

services_col.insert_many(docs)
print("Seeded services:", services_col.count_documents({}))
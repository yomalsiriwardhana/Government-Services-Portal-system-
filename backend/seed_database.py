from pymongo import MongoClient
import os
from datetime import datetime

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["government_portal"]
services_col = db["services"]

# Clear existing data
services_col.delete_many({})
print("🗑️  Cleared existing services")

# Comprehensive Government Services Data
services_data = [
    {
        "id": "driving-license",
        "name": "Driving License Application & Renewal",
        "description": "Apply for a new driving license, learner permit, or renew your existing license. Available for two-wheelers, four-wheelers, and commercial vehicles.",
        "category": "Transportation",
        "ministry": "Ministry of Road Transport and Highways",
        "icon": "🚗",
        "popular": True,
        "clicks": 1250,
        "details": {
            "full_description": "The driving license is an official document that permits an individual to operate motor vehicles on public roads. In India, driving licenses are issued by the Regional Transport Office (RTO) under the provisions of the Motor Vehicles Act, 1988. The process involves both a written test and a practical driving test.",
            "eligibility": [
                "Minimum age 18 years for non-transport vehicles",
                "Minimum age 20 years for transport vehicles",
                "Should not be disqualified under any court order",
                "Must pass medical fitness test"
            ],
            "required_documents": [
                "Proof of Identity (Aadhaar Card/PAN Card/Passport)",
                "Proof of Address (Aadhaar Card/Utility Bill/Rent Agreement)",
                "Age Proof (Birth Certificate/School Certificate/Passport)",
                "Passport size photographs (8 copies)",
                "Medical Certificate (Form 1 & 1A)",
                "Learning License (for permanent license)"
            ],
            "application_process": [
                "Visit the Parivahan Sewa website (parivahan.gov.in/parivahan)",
                "Select your state RTO",
                "Choose 'Apply for Driving License' option",
                "Fill in Form 4 (Learning License) or Form 5 (Permanent License)",
                "Upload all required documents",
                "Pay application fees online",
                "Book slot for written test (for LL) or driving test (for DL)",
                "Visit RTO on scheduled date with original documents",
                "Pass the tests and collect your license"
            ],
            "fees": {
                "learning_license": "Rs. 200",
                "permanent_license": "Rs. 200",
                "renewal": "Rs. 200",
                "duplicate": "Rs. 200",
                "international_permit": "Rs. 1,000"
            },
            "processing_time": "15-30 days after passing tests",
            "validity": {
                "non_transport": "Valid until age 50 (then renewable every 5 years)",
                "transport": "Valid for 3 years, renewable",
                "learners": "Valid for 6 months"
            },
            "important_notes": [
                "Learning license is mandatory before applying for permanent license",
                "Must hold learning license for at least 30 days before DL test",
                "Bring original documents to RTO on test day",
                "License will be sent to registered address via Speed Post"
            ],
            "contact": {
                "website": "https://parivahan.gov.in",
                "helpline": "1800-110-321",
                "email": "support@parivahan.gov.in"
            },
            "online_services": [
                "Apply for new license",
                "Renew existing license",
                "Apply for duplicate license",
                "Update address",
                "Check application status"
            ]
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "passport",
        "name": "Passport Application & Renewal",
        "description": "Apply for Indian passport, renew expired passport, or apply for tatkal (urgent) passport services for international travel.",
        "category": "Immigration & Travel",
        "ministry": "Ministry of External Affairs",
        "icon": "🛂",
        "popular": True,
        "clicks": 2150,
        "details": {
            "full_description": "An Indian passport is an official travel document issued by the Government of India to Indian citizens for international travel. It serves as proof of Indian citizenship and identity. Passports are issued by the Passport Seva Kendra (PSK) under the Ministry of External Affairs.",
            "types": [
                "Ordinary Passport (Blue Cover) - For general travel",
                "Official Passport (White Cover) - For government officials",
                "Diplomatic Passport (Maroon Cover) - For diplomats"
            ],
            "eligibility": [
                "Must be an Indian citizen",
                "All age groups eligible",
                "No criminal record (for certain cases)",
                "Valid proof of identity and address"
            ],
            "required_documents": [
                "Proof of Present Address (Aadhaar Card/Utility Bill/Rent Agreement)",
                "Proof of Date of Birth (Birth Certificate/School Certificate/Aadhaar)",
                "Copy of first and last page of existing passport (for renewal)",
                "Marriage certificate (if name change after marriage)",
                "Annexure D (if both parents not Indian citizens)",
                "Divorce decree (if applicable)",
                "ECR/Non-ECR proof (educational certificates)"
            ],
            "application_process": [
                "Register on Passport Seva Online Portal (www.passportindia.gov.in)",
                "Fill Online Application Form",
                "Pay fee online (Regular/Tatkal)",
                "Schedule appointment at nearest Passport Seva Kendra (PSK)",
                "Visit PSK with original documents on appointment date",
                "Biometric data collection (fingerprints & photograph)",
                "Document verification by officer",
                "Police verification (if required)",
                "Passport printing and dispatch to address"
            ],
            "fees": {
                "fresh_passport_36_pages": "Rs. 1,500",
                "fresh_passport_60_pages": "Rs. 2,000",
                "renewal_36_pages": "Rs. 1,500",
                "renewal_60_pages": "Rs. 2,000",
                "tatkal_36_pages": "Rs. 3,500",
                "tatkal_60_pages": "Rs. 4,000",
                "minor_passport": "Rs. 1,000",
                "police_clearance_certificate": "Rs. 500"
            },
            "processing_time": {
                "normal": "30-45 days",
                "tatkal": "3-7 working days",
                "reissue": "15-20 days"
            },
            "validity": {
                "adult": "10 years from date of issue",
                "minor": "5 years or until age 18, whichever is earlier"
            },
            "important_notes": [
                "Carry all original documents to PSK",
                "Arrive 15 minutes before appointment time",
                "Dress code: Avoid sleeveless clothes for photo",
                "Police verification may be required for first-time applicants",
                "Track application status online using file number"
            ],
            "contact": {
                "website": "https://www.passportindia.gov.in",
                "helpline": "1800-258-1800 (National Call Center)",
                "email": "cpvdelhi@mea.gov.in"
            },
            "online_services": [
                "Fresh passport application",
                "Passport renewal",
                "Lost/damaged passport reissue",
                "Address change",
                "Police clearance certificate",
                "Track application status"
            ]
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "pan-card",
        "name": "PAN Card Application",
        "description": "Apply for Permanent Account Number (PAN) card required for all financial transactions, tax filing, and banking services.",
        "category": "Finance & Tax",
        "ministry": "Income Tax Department",
        "icon": "💳",
        "popular": True,
        "clicks": 1850,
        "details": {
            "full_description": "PAN (Permanent Account Number) is a 10-digit alphanumeric identifier issued by the Income Tax Department of India. It is mandatory for all financial transactions above Rs. 50,000 and for filing income tax returns.",
            "eligibility": [
                "Indian citizens",
                "Foreign citizens",
                "Companies and firms",
                "Hindu Undivided Families (HUF)",
                "Any person with taxable income"
            ],
            "required_documents": [
                "Proof of Identity (Aadhaar/Passport/Voter ID/Driving License)",
                "Proof of Address (Aadhaar/Passport/Bank Statement/Utility Bill)",
                "Proof of Date of Birth (Birth Certificate/School Certificate/Passport)",
                "Two passport size photographs",
                "For foreigners: Copy of passport and visa"
            ],
            "application_process": [
                "Visit NSDL (www.tin-nsdl.com) or UTIITSL (www.utiitsl.com) website",
                "Select 'Apply for New PAN Card' option",
                "Choose Form 49A (Indian citizens) or 49AA (Foreign citizens)",
                "Fill online application form",
                "Upload scanned documents (colored)",
                "Pay application fee online",
                "Submit application",
                "Note down acknowledgment number",
                "PAN card will be dispatched to address within 15-20 days",
                "Download e-PAN instantly after verification"
            ],
            "fees": {
                "indian_applicant": "Rs. 110 (incl. GST)",
                "foreign_applicant": "Rs. 1,020 (incl. GST)",
                "correction_reprint": "Rs. 110",
                "e_pan": "Rs. 8.26 (digital download)"
            },
            "processing_time": "15-30 days (physical card), Instant (e-PAN)",
            "validity": "Lifetime (No renewal required)",
            "pan_structure": "Format: AAAPL1234C (5 letters, 4 digits, 1 letter)",
            "important_notes": [
                "Each person can have only one PAN",
                "PAN is mandatory for income tax return filing",
                "Required for opening bank accounts",
                "Mandatory for property transactions above Rs. 10 lakhs",
                "Link PAN with Aadhaar to keep it active",
                "E-PAN is equally valid as physical PAN card"
            ],
            "contact": {
                "nsdl_website": "https://www.tin-nsdl.com",
                "utiitsl_website": "https://www.utiitsl.com",
                "helpline": "020-27218080 (NSDL), 020-40712000 (UTIITSL)",
                "email": "tininfo@nsdl.co.in"
            },
            "online_services": [
                "New PAN application",
                "Changes or correction in PAN",
                "Reprint of PAN card",
                "Check PAN application status",
                "Download e-PAN",
                "Verify PAN online"
            ]
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "aadhaar-card",
        "name": "Aadhaar Card Enrollment & Update",
        "description": "Apply for Aadhaar card - India's unique 12-digit identity number. Update demographics, biometrics, and download e-Aadhaar.",
        "category": "Identity Services",
        "ministry": "UIDAI (Unique Identification Authority of India)",
        "icon": "🆔",
        "popular": True,
        "clicks": 2450,
        "details": {
            "full_description": "Aadhaar is a 12-digit unique identity number issued by UIDAI to all residents of India. It is based on biometric and demographic data and serves as proof of identity and address throughout India. Aadhaar is the world's largest biometric ID system.",
            "eligibility": [
                "All residents of India (citizens and non-citizens)",
                "No age limit - from newborns to senior citizens",
                "Must have resided in India for 182 days in preceding 12 months"
            ],
            "required_documents": [
                "Proof of Identity (Passport/PAN Card/Driving License/Voter ID/Bank Statement)",
                "Proof of Address (Passport/Bank Statement/Utility Bill/Rent Agreement)",
                "Proof of Date of Birth (Birth Certificate/School Certificate/PAN Card)",
                "For children below 5 years: Parents' Aadhaar",
                "No documents required if enrolling with Aadhaar holder as introducer"
            ],
            "enrollment_process": [
                "Locate nearest Aadhaar Enrollment Center (search on uidai.gov.in)",
                "Visit the center with original documents",
                "Fill Aadhaar enrollment form",
                "Provide biometric data (10 fingerprints, 2 iris scans, photograph)",
                "Submit documents for verification",
                "Collect acknowledgment slip with 14-digit enrollment ID",
                "Check status online using enrollment ID",
                "Aadhaar will be generated within 90 days",
                "Download e-Aadhaar from UIDAI website"
            ],
            "update_process": [
                "Book appointment online at myaadhaar.uidai.gov.in",
                "Visit enrollment center with documents",
                "Pay update fees",
                "Update required details (name/address/DOB/gender/mobile/email)",
                "Update biometrics if needed",
                "Collect update request number (URN)",
                "Updated Aadhaar available within 30 days"
            ],
            "fees": {
                "new_enrollment": "Free",
                "demographic_update": "Rs. 50",
                "biometric_update": "Rs. 100",
                "both_updates": "Rs. 100"
            },
            "processing_time": "60-90 days (new enrollment), 7-30 days (updates)",
            "validity": "Lifetime (Update required at age 5 and 15 for children)",
            "important_notes": [
                "Aadhaar is mandatory for government subsidies and benefits",
                "Link Aadhaar with bank account, mobile number, and PAN",
                "Children under 5 must update biometrics at age 5 and 15",
                "Download e-Aadhaar and save password-protected PDF",
                "Masked Aadhaar can be used to hide first 8 digits",
                "Virtual ID (VID) can be used instead of Aadhaar number"
            ],
            "contact": {
                "website": "https://uidai.gov.in",
                "helpline": "1947 (Toll-free)",
                "email": "help@uidai.gov.in"
            },
            "online_services": [
                "Download e-Aadhaar",
                "Check enrollment status",
                "Update Aadhaar details online",
                "Book appointment for updates",
                "Generate Virtual ID (VID)",
                "Lock/unlock biometrics",
                "Verify Aadhaar",
                "Retrieve enrollment ID"
            ]
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "birth-certificate",
        "name": "Birth Certificate Registration",
        "description": "Register birth and obtain official birth certificate - essential document for school admission, passport, and other services.",
        "category": "Civil Registration",
        "ministry": "Ministry of Home Affairs",
        "icon": "👶",
        "popular": True,
        "clicks": 980,
        "details": {
            "full_description": "Birth certificate is an official document issued by the government that records a person's birth. It includes details like name, date and place of birth, parents' names, and is governed by the Registration of Births and Deaths Act, 1969. It is essential for obtaining most other identity documents.",
            "eligibility": [
                "All births occurring in India must be registered",
                "Parents or guardians can apply",
                "Hospital authorities can register institutional births",
                "Registration can be done within 21 days (free) or as delayed registration"
            ],
            "required_documents": [
                "Hospital birth certificate or delivery record",
                "Parents' identity proof (Aadhaar/Passport/Voter ID)",
                "Parents' marriage certificate (if available)",
                "Parents' address proof",
                "Immunization card of child",
                "Affidavit from parents (for delayed registration)",
                "Age proof of mother (if required)"
            ],
            "registration_process": [
                "Register within 21 days of birth (no fee)",
                "Visit local Municipal Corporation/Gram Panchayat office",
                "Or register online through state government portal",
                "Fill birth registration form",
                "Attach hospital birth certificate",
                "Submit parents' documents",
                "Pay fee (if delayed registration)",
                "Receive acknowledgment receipt",
                "Birth certificate will be issued within 7-15 days",
                "Download digital certificate if available"
            ],
            "delayed_registration": {
                "21_days_to_1_year": "Register with late fee of Rs. 2-5",
                "1_year_to_5_years": "Requires affidavit and late fee",
                "after_5_years": "Requires court order and late fee"
            },
            "fees": {
                "within_21_days": "Free",
                "21_days_to_1_year": "Rs. 2-5",
                "after_1_year": "Rs. 5-10",
                "duplicate_copy": "Rs. 10-50",
                "correction": "Rs. 50-100"
            },
            "processing_time": "Immediate to 15 days (depending on state)",
            "validity": "Lifetime (permanent document)",
            "uses": [
                "School admission",
                "Passport application",
                "Aadhaar enrollment",
                "Proof of age for various services",
                "Legal identity establishment",
                "Property inheritance",
                "Government benefit schemes"
            ],
            "important_notes": [
                "Register birth within 21 days to avoid late fee",
                "Keep multiple copies of birth certificate",
                "Correction in birth certificate requires proper documents",
                "Birth certificate cannot be changed after 1 year without court order",
                "Digital birth certificates have same legal validity"
            ],
            "contact": {
                "varies_by_state": "Contact local Municipal Corporation or Gram Panchayat",
                "crsorgi_website": "https://crsorgi.gov.in (for online registration)",
                "helpline": "Contact local registrar office"
            },
            "online_services": [
                "Online birth registration",
                "Download birth certificate",
                "Check registration status",
                "Apply for duplicate certificate",
                "Request for correction"
            ]
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "voter-id",
        "name": "Voter ID Card (EPIC) Application",
        "description": "Apply for Election Photo Identity Card (EPIC) - essential for voting in elections and useful as identity and address proof.",
        "category": "Electoral Services",
        "ministry": "Election Commission of India",
        "icon": "🗳️",
        "popular": True,
        "clicks": 750,
        "details": {
            "full_description": "The Voter ID card, officially known as Electors Photo Identity Card (EPIC), is an identity document issued by the Election Commission of India to eligible Indian citizens. It serves as both an identity proof and proof of voting eligibility.",
            "eligibility": [
                "Indian citizen",
                "Minimum age 18 years on or before January 1st of the year",
                "Resident of the constituency where applying",
                "Not disqualified under any law"
            ],
            "required_documents": [
                "Proof of Age (Birth Certificate/School Certificate/PAN Card/Passport)",
                "Proof of Address (Aadhaar Card/Passport/Utility Bill/Bank Statement/Rent Agreement)",
                "Recent passport size photographs (3 copies)",
                "Aadhaar Card (optional but recommended for address verification)"
            ],
            "application_process": [
                "Visit National Voters' Service Portal (www.nvsp.in)",
                "Click on 'Register as a New Voter' (Form 6)",
                "Fill online application with personal details",
                "Upload required documents (colored scans)",
                "Upload recent photograph",
                "Submit application online",
                "Note down reference number for tracking",
                "BLO (Booth Level Officer) will visit for verification",
                "After verification, name added to electoral roll",
                "Voter ID card dispatched to address within 30-60 days"
            ],
            "correction_process": [
                "Login to NVSP portal",
                "Select 'Correction in Voter Details' (Form 8)",
                "Choose fields to correct (name/address/age/photo)",
                "Upload supporting documents",
                "Submit correction request",
                "Wait for BLO verification",
                "Corrected card issued within 30 days"
            ],
            "fees": "Free (No charges for application or correction)",
            "processing_time": "30-60 days after verification",
            "validity": "Lifetime (No renewal required, but can update details)",
            "important_notes": [
                "Apply before final electoral roll publication",
                "Electoral roll updated annually before major elections",
                "BLO visit mandatory for verification",
                "Voter ID can be used as identity proof for various services",
                "Link Aadhaar with Voter ID for automatic updates",
                "Check electoral roll to ensure your name is listed"
            ],
            "contact": {
                "website": "https://www.nvsp.in",
                "helpline": "1950 (Toll-free)",
                "email": "eci-ceo@eci.gov.in"
            },
            "online_services": [
                "New voter registration",
                "Correction in voter details",
                "Deletion of name from electoral roll",
                "Transposition of entry",
                "Download e-EPIC (digital voter card)",
                "Search name in electoral roll",
                "Track application status"
            ]
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "ration-card",
        "name": "Ration Card Application",
        "description": "Apply for ration card to receive subsidized food grains and essential commodities through Public Distribution System (PDS).",
        "category": "Welfare Schemes",
        "ministry": "Ministry of Consumer Affairs, Food and Public Distribution",
        "icon": "🌾",
        "popular": False,
        "clicks": 650,
        "details": {
            "full_description": "Ration card is an official document issued by State Governments to identify families eligible for subsidized food grains and essential commodities under the Public Distribution System (PDS). It also serves as proof of residence.",
            "types": [
                "APL (Above Poverty Line) - For families above poverty line",
                "BPL (Below Poverty Line) - For families below poverty line",
                "AAY (Antyodaya Anna Yojana) - For poorest of poor families"
            ],
            "eligibility": [
                "Indian citizen",
                "Permanent resident of the state",
                "Should not hold ration card from another state",
                "Income criteria as per state guidelines"
            ],
            "required_documents": [
                "Aadhaar cards of all family members",
                "Proof of residence (Electricity bill/Water bill/Rent agreement)",
                "Income certificate from competent authority",
                "Passport size photographs of all members",
                "Bank account details",
                "Caste certificate (if applicable)",
                "BPL certificate (for BPL card)"
            ],
            "application_process": [
                "Visit state food and civil supplies department website",
                "Download ration card application form",
                "Fill form with all family member details",
                "Attach required documents",
                "Submit at Fair Price Shop or online portal",
                "Pay application fee (if applicable)",
                "Inspection officer will verify address",
                "After approval, collect ration card from designated office"
            ],
            "fees": "Rs. 10-50 (varies by state) or Free for BPL families",
            "processing_time": "30-45 days after verification",
            "benefits": [
                "Subsidized wheat, rice, sugar, and kerosene",
                "APL: 15 kg grains per month",
                "BPL: 25 kg grains per month",
                "AAY: 35 kg grains per month",
                "Can be used as address proof"
            ],
            "important_notes": [
                "Link all family Aadhaar numbers with ration card",
                "Update ration card if family member added or removed",
                "Collect monthly quota from designated fair price shop",
                "Ration card is transferable between states (One Nation One Ration Card)",
                "Report if ration card is lost immediately"
            ],
            "contact": {
                "varies_by_state": "Contact State Food and Civil Supplies Department",
                "helpline": "1967 (varies by state)",
                "nfsa_portal": "https://nfsa.gov.in"
            }
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "marriage-certificate",
        "name": "Marriage Certificate Registration",
        "description": "Register your marriage and obtain official marriage certificate - legal proof of marriage required for various services.",
        "category": "Civil Registration",
        "ministry": "Ministry of Home Affairs",
        "icon": "💍",
        "popular": False,
        "clicks": 420,
        "details": {
            "full_description": "Marriage certificate is a legal document that proves the marriage between two individuals. In India, marriage registration is governed by different acts based on religion: Hindu Marriage Act (1955), Special Marriage Act (1954), etc.",
            "types": [
                "Hindu Marriage Act Registration - For Hindu, Buddhist, Jain, Sikh marriages",
                "Special Marriage Act Registration - For inter-faith or civil marriages",
                "Muslim Marriage Registration - Under state-specific laws",
                "Christian Marriage Act - For Christian marriages"
            ],
            "eligibility": [
                "Bride minimum age 18 years, Groom minimum age 21 years",
                "Both parties consent to marriage",
                "Neither party has living spouse",
                "Parties not within prohibited degrees of relationship"
            ],
            "required_documents": [
                "Marriage invitation card",
                "Proof of date of birth of both parties",
                "Address proof of both bride and groom",
                "Passport size photographs (bride and groom)",
                "Identity proof of bride, groom, and witnesses (3 witnesses required)",
                "Affidavit stating marital status",
                "Divorce decree (if applicable)",
                "Death certificate of spouse (if widow/widower)"
            ],
            "registration_process": [
                "Marriage can be registered within 60 days or after years (late registration)",
                "Visit Sub-Registrar office or apply online through state portal",
                "Fill marriage registration form",
                "Attach marriage photographs and documents",
                "Both bride and groom must be present with 3 witnesses",
                "Pay registration fees",
                "Submit application",
                "Verification by registrar",
                "Certificate issued within 7-30 days"
            ],
            "fees": {
                "within_60_days": "Rs. 100-200",
                "delayed_registration": "Rs. 200-500",
                "duplicate_certificate": "Rs. 50-100"
            },
            "processing_time": "7-30 days (varies by state)",
            "importance": [
                "Legal proof of marriage",
                "Required for passport application (name change)",
                "Needed for visa applications",
                "Property and inheritance rights",
                "Sponsorship for spouse in foreign countries",
                "Social security benefits"
            ],
            "important_notes": [
                "Marriage registration is mandatory in many states",
                "Can register marriage anytime after wedding",
                "Both parties must be present during registration",
                "Three witnesses required with identity proof",
                "Certificate issued in both parties' names"
            ],
            "contact": {
                "varies_by_state": "Contact local Sub-Registrar office or Municipal Corporation",
                "helpline": "Contact state registration department"
            }
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

# Insert all services
result = services_col.insert_many(services_data)
print(f"✅ Successfully seeded {len(result.inserted_ids)} services into database")
print(f"📊 Popular services: {len([s for s in services_data if s.get('popular')])}")
print(f"🔗 Service IDs: {[s['id'] for s in services_data]}")

# Create indexes for better performance
services_col.create_index("id", unique=True)
services_col.create_index("category")
services_col.create_index("popular")
services_col.create_index("clicks")
print("✅ Created database indexes")

print("\n🎉 Database seeding completed successfully!")
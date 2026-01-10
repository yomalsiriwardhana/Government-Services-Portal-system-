// Multilingual translation system
const translations = {
    en: {
        // Navigation
        nav_home: "Home",
        nav_services: "Services",
        nav_dashboard: "Dashboard",
        
        // Home Page
        home_title: "Government Services Portal",
        home_subtitle: "Access all government services in one place",
        home_search_placeholder: "Search for services...",
        home_popular_services: "Popular Services",
        home_view_all: "View All Services",
        home_ai_search: "AI-Powered Search",
        home_ask_question: "Ask me anything about government services:",
        home_get_answer: "Get AI Answer",
        
        // Services Page
        services_title: "Government Services",
        services_subtitle: "Browse and search all available government services",
        services_filter: "Filter by Category:",
        services_all_categories: "All Categories",
        services_search: "Search Services:",
        services_search_placeholder: "Search services...",
        services_search_btn: "Search",
        services_loading: "Loading services...",
        services_no_results: "No services found matching your criteria.",
        services_view_details: "View Details",
        
        // Service Categories
        category_transportation: "Transportation",
        category_immigration: "Immigration & Travel",
        category_finance: "Finance & Tax",
        category_identity: "Identity Services",
        category_electoral: "Electoral Services",
        category_civil: "Civil Registration",
        category_welfare: "Welfare Schemes",
        category_healthcare: "Healthcare",
        category_property: "Property & Land",
        category_business: "Business & Commerce",
        
        // Service Modal
        modal_overview: "Overview",
        modal_types: "Types",
        modal_eligibility: "Eligibility Criteria",
        modal_documents: "Required Documents",
        modal_process: "Application Process",
        modal_fees: "Fees",
        modal_processing_time: "Processing Time",
        modal_validity: "Validity",
        modal_important_notes: "Important Notes",
        modal_contact: "Contact Information",
        modal_online_services: "Online Services Available",
        modal_website: "Website",
        modal_helpline: "Helpline",
        modal_email: "Email",
        modal_close: "Close",
        modal_visit_website: "Visit Official Website",
        
        // AI Search
        ai_answer: "AI Answer",
        ai_confidence: "Confidence",
        ai_relevant_services: "Relevant Services & Information",
        ai_no_sources: "No additional sources found",
        ai_error: "Sorry, I encountered an error while processing your question. Please try again or use regular search.",
        
        // Common
        loading: "Loading...",
        error: "Error",
        success: "Success",
        ministry: "Ministry",
        department: "Department",
        click_tracking: "Click tracked",
        
        // Footer
        footer_text: "© 2025 Government Services Portal - Sri Lanka. All rights reserved.",
        
        // Service Names
        service_driving_license: "Driving License Application & Renewal",
        service_passport: "Passport Application & Renewal",
        service_pan_card: "PAN Card Application",
        service_aadhaar: "Aadhaar Card Enrollment & Update",
        service_birth_certificate: "Birth Certificate Registration",
        service_voter_id: "Voter ID Card (EPIC) Application",
        service_ration_card: "Ration Card Application",
        service_marriage_certificate: "Marriage Certificate Registration",
        
        // Descriptions
        desc_driving_license: "Apply for a new driving license, learner permit, or renew your existing license. Available for two-wheelers, four-wheelers, and commercial vehicles.",
        desc_passport: "Apply for Indian passport, renew expired passport, or apply for tatkal (urgent) passport services for international travel.",
        desc_pan_card: "Apply for Permanent Account Number (PAN) card required for all financial transactions, tax filing, and banking services.",
        desc_aadhaar: "Apply for Aadhaar card - India's unique 12-digit identity number. Update demographics, biometrics, and download e-Aadhaar.",
        desc_birth_certificate: "Register birth and obtain official birth certificate - essential document for school admission, passport, and other services.",
        desc_voter_id: "Apply for Election Photo Identity Card (EPIC) - essential for voting in elections and useful as identity and address proof.",
        desc_ration_card: "Apply for ration card to receive subsidized food grains and essential commodities through Public Distribution System (PDS).",
        desc_marriage_certificate: "Register your marriage and obtain official marriage certificate - legal proof of marriage required for various services."
    },
    
    si: {
        // Navigation - සංචාලනය
        nav_home: "මුල් පිටුව",
        nav_services: "සේවා",
        nav_dashboard: "උපකරණ පුවරුව",
        
        // Home Page - මුල් පිටුව
        home_title: "රජයේ සේවා ද්වාරය",
        home_subtitle: "සියලුම රජයේ සේවා එක් තැනකින්",
        home_search_placeholder: "සේවා සොයන්න...",
        home_popular_services: "ජනප්‍රිය සේවා",
        home_view_all: "සියල්ල බලන්න",
        home_ai_search: "AI බුද්ධිමත් සෙවීම",
        home_ask_question: "රජයේ සේවා ගැන ඕනෑම දෙයක් අසන්න:",
        home_get_answer: "AI පිළිතුර ලබා ගන්න",
        
        // Services Page - සේවා පිටුව
        services_title: "රජයේ සේවා",
        services_subtitle: "සියලුම රජයේ සේවා පිරික්සන්න සහ සොයන්න",
        services_filter: "වර්ගය අනුව පෙරීම:",
        services_all_categories: "සියලු වර්ග",
        services_search: "සේවා සොයන්න:",
        services_search_placeholder: "සේවා සොයන්න...",
        services_search_btn: "සොයන්න",
        services_loading: "සේවා පූරණය වෙමින්...",
        services_no_results: "ඔබේ නිර්ණායක වලට ගැලපෙන සේවා හමු නොවීය.",
        services_view_details: "විස්තර බලන්න",
        
        // Service Categories - සේවා වර්ග
        category_transportation: "ප්‍රවාහනය",
        category_immigration: "සංක්‍රමණ සහ සංචාරක",
        category_finance: "මුල්‍ය හා බදු",
        category_identity: "අනන්‍යතා සේවා",
        category_electoral: "මැතිවරණ සේවා",
        category_civil: "සිවිල් ලියාපදිංචිය",
        category_welfare: "සුභසාධන යෝජනා",
        category_healthcare: "සෞඛ්‍ය සේවා",
        category_property: "දේපල සහ ඉඩම්",
        category_business: "ව්‍යාපාර සහ වාණිජ",
        
        // Service Modal - සේවා විස්තර
        modal_overview: "දළ විශ්ලේෂණය",
        modal_types: "වර්ග",
        modal_eligibility: "සුදුසුකම් නිර්ණායක",
        modal_documents: "අවශ්‍ය ලියකියවිලි",
        modal_process: "අයදුම් ක්‍රියාවලිය",
        modal_fees: "ගාස්තු",
        modal_processing_time: "ප්‍රතිකරණ කාලය",
        modal_validity: "වලංගුභාවය",
        modal_important_notes: "වැදගත් සටහන්",
        modal_contact: "සම්බන්ධතා තොරතුරු",
        modal_online_services: "මාර්ගගත සේවා ලබා ගත හැකිය",
        modal_website: "වෙබ් අඩවිය",
        modal_helpline: "උදවු මාර්ගය",
        modal_email: "විද්‍යුත් තැපෑල",
        modal_close: "වසන්න",
        modal_visit_website: "නිල වෙබ් අඩවියට පිවිසෙන්න",
        
        // AI Search - AI සෙවීම
        ai_answer: "AI පිළිතුර",
        ai_confidence: "විශ්වාසනීයත්වය",
        ai_relevant_services: "අදාළ සේවා සහ තොරතුරු",
        ai_no_sources: "අතිරේක මූලාශ්‍ර හමු නොවීය",
        ai_error: "කණගාටුයි, ඔබේ ප්‍රශ්නය සැකසීමේදී දෝෂයක් ඇති විය. කරුණාකර නැවත උත්සාහ කරන්න.",
        
        // Common - පොදු
        loading: "පූරණය වෙමින්...",
        error: "දෝෂය",
        success: "සාර්ථකයි",
        ministry: "අමාත්‍යාංශය",
        department: "දෙපාර්තමේන්තුව",
        click_tracking: "ක්ලික් එක සටහන් කරන ලදී",
        
        // Footer - පාදකය
        footer_text: "© 2025 රජයේ සේවා ද්වාරය - ශ්‍රී ලංකාව. සියලුම හිමිකම් ඇවිරිණි.",
        
        // Service Names - සේවා නම්
        service_driving_license: "රියදුරු බලපත්‍ර අයදුම්පත සහ අළුත් කිරීම",
        service_passport: "විදේශ ගමන් බලපත්‍ර අයදුම්පත සහ අළුත් කිරීම",
        service_pan_card: "PAN කාඩ් අයදුම්පත",
        service_aadhaar: "ආධාර් කාඩ් ලියාපදිංචිය සහ යාවත්කාලීන කිරීම",
        service_birth_certificate: "උප්පැන්න සහතිකය ලියාපදිංචිය",
        service_voter_id: "ඡන්දදායක හැඳුනුම්පත් අයදුම්පත",
        service_ration_card: "සලාක කාඩ් අයදුම්පත",
        service_marriage_certificate: "විවාහ සහතිකය ලියාපදිංචිය",
        
        // Descriptions - විස්තර
        desc_driving_license: "නව රියදුරු බලපත්‍රයක් සඳහා අයදුම් කරන්න, ඉගෙනුම් බලපත්‍රය හෝ ඔබගේ පවතින බලපත්‍රය අළුත් කරන්න. ද්වි රෝද, සතර රෝද සහ වාණිජ වාහන සඳහා ලබා ගත හැකිය.",
        desc_passport: "ඉන්දියානු විදේශ ගමන් බලපත්‍රයක් සඳහා අයදුම් කරන්න, කල් ඉකුත් වූ විදේශ ගමන් බලපත්‍රය අළුත් කරන්න හෝ ත්වරිත සේවා සඳහා අයදුම් කරන්න.",
        desc_pan_card: "සියලුම මූල්‍ය ගනුදෙනු, බදු ගොනුකිරීම සහ බැංකු සේවා සඳහා අවශ්‍ය ස්ථිර ගිණුම් අංකය (PAN) කාඩ්පත සඳහා අයදුම් කරන්න.",
        desc_aadhaar: "ආධාර් කාඩ්පත සඳහා අයදුම් කරන්න - ඉන්දියාවේ අද්විතීය ඉලක්කම් 12 හැඳුනුම්පත. ජන විකාශන, ජීවමිතික සහ ඊ-ආධාර් බාගත කරන්න.",
        desc_birth_certificate: "උපත ලියාපදිංචි කර නිල උප්පැන්න සහතිකය ලබා ගන්න - පාසල් ඇතුළත් කිරීම, විදේශ ගමන් බලපත්‍රය සහ අනෙකුත් සේවා සඳහා අත්‍යවශ්‍ය ලේඛනය.",
        desc_voter_id: "මැතිවරණ ඡායාරූප හැඳුනුම්පත (EPIC) සඳහා අයදුම් කරන්න - මැතිවරණවලදී ඡන්දය දීම සඳහා අත්‍යවශ්‍ය සහ හැඳුනුම්පත සහ ලිපින සාක්ෂිය ලෙස ප්‍රයෝජනවත්.",
        desc_ration_card: "මහජන බෙදාහැරීමේ පද්ධතිය (PDS) හරහා සහනදායී ආහාර ධාන්‍ය සහ අත්‍යවශ්‍ය භාණ්ඩ ලබා ගැනීමට සලාක කාඩ්පත සඳහා අයදුම් කරන්න.",
        desc_marriage_certificate: "ඔබේ විවාහය ලියාපදිංචි කර නිල විවාහ සහතිකය ලබා ගන්න - විවිධ සේවා සඳහා අවශ්‍ය විවාහයේ නීතිමය සාක්ෂිය."
    },
    
    ta: {
        // Navigation - வழிசெலுத்தல்
        nav_home: "முகப்பு",
        nav_services: "சேவைகள்",
        nav_dashboard: "டாஷ்போர்டு",
        
        // Home Page - முகப்பு பக்கம்
        home_title: "அரசு சேவைகள் போர்ட்டல்",
        home_subtitle: "அனைத்து அரசு சேவைகளும் ஒரே இடத்தில்",
        home_search_placeholder: "சேவைகளைத் தேடுங்கள்...",
        home_popular_services: "பிரபலமான சேவைகள்",
        home_view_all: "அனைத்தையும் பார்க்கவும்",
        home_ai_search: "AI சக்தி வாய்ந்த தேடல்",
        home_ask_question: "அரசு சேவைகள் பற்றி எதையும் கேளுங்கள்:",
        home_get_answer: "AI பதில் பெறவும்",
        
        // Services Page - சேவைகள் பக்கம்
        services_title: "அரசு சேவைகள்",
        services_subtitle: "அனைத்து கிடைக்கக்கூடிய அரசு சேவைகளையும் உலாவவும் தேடவும்",
        services_filter: "வகையின்படி வடிகட்டவும்:",
        services_all_categories: "அனைத்து வகைகள்",
        services_search: "சேவைகளைத் தேடுங்கள்:",
        services_search_placeholder: "சேவைகளைத் தேடுங்கள்...",
        services_search_btn: "தேடு",
        services_loading: "சேவைகள் ஏற்றப்படுகின்றன...",
        services_no_results: "உங்கள் அளவுகோல்களுடன் பொருந்தும் சேவைகள் எதுவும் இல்லை.",
        services_view_details: "விவரங்களைக் காண்க",
        
        // Service Categories - சேவை வகைகள்
        category_transportation: "போக்குவரத்து",
        category_immigration: "குடிவரவு மற்றும் பயணம்",
        category_finance: "நிதி மற்றும் வரி",
        category_identity: "அடையாள சேவைகள்",
        category_electoral: "தேர்தல் சேவைகள்",
        category_civil: "சிவில் பதிவு",
        category_welfare: "நலத் திட்டங்கள்",
        category_healthcare: "சுகாதார சேவைகள்",
        category_property: "சொத்து மற்றும் நிலம்",
        category_business: "வணிகம் மற்றும் வர்த்தகம்",
        
        // Service Modal - சேவை விவரங்கள்
        modal_overview: "மேலோட்டம்",
        modal_types: "வகைகள்",
        modal_eligibility: "தகுதி விதிமுறைகள்",
        modal_documents: "தேவையான ஆவணங்கள்",
        modal_process: "விண்ணப்ப செயல்முறை",
        modal_fees: "கட்டணங்கள்",
        modal_processing_time: "செயலாக்க நேரம்",
        modal_validity: "செல்லுபடியாகும் காலம்",
        modal_important_notes: "முக்கிய குறிப்புகள்",
        modal_contact: "தொடர்பு தகவல்",
        modal_online_services: "ஆன்லைன் சேவைகள் கிடைக்கின்றன",
        modal_website: "இணையதளம்",
        modal_helpline: "உதவி எண்",
        modal_email: "மின்னஞ்சல்",
        modal_close: "மூடு",
        modal_visit_website: "அதிகாரப்பூர்வ இணையதளத்தைப் பார்வையிடவும்",
        
        // AI Search - AI தேடல்
        ai_answer: "AI பதில்",
        ai_confidence: "நம்பிக்கை",
        ai_relevant_services: "தொடர்புடைய சேவைகள் மற்றும் தகவல்",
        ai_no_sources: "கூடுதல் ஆதாரங்கள் எதுவும் இல்லை",
        ai_error: "மன்னிக்கவும், உங்கள் கேள்வியைச் செயலாக்கும்போது பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.",
        
        // Common - பொதுவானது
        loading: "ஏற்றப்படுகிறது...",
        error: "பிழை",
        success: "வெற்றி",
        ministry: "அமைச்சகம்",
        department: "துறை",
        click_tracking: "கிளிக் கண்காணிக்கப்பட்டது",
        
        // Footer - அடிக்குறிப்பு
        footer_text: "© 2025 அரசு சேவைகள் போர்ட்டல் - இலங்கை. அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.",
        
        // Service Names - சேவை பெயர்கள்
        service_driving_license: "ஓட்டுநர் உரிமம் விண்ணப்பம் மற்றும் புதுப்பித்தல்",
        service_passport: "கடவுச்சீட்டு விண்ணப்பம் மற்றும் புதுப்பித்தல்",
        service_pan_card: "PAN அட்டை விண்ணப்பம்",
        service_aadhaar: "ஆதார் அட்டை பதிவு மற்றும் புதுப்பித்தல்",
        service_birth_certificate: "பிறப்பு சான்றிதழ் பதிவு",
        service_voter_id: "வாக்காளர் அடையாள அட்டை விண்ணப்பம்",
        service_ration_card: "ரேஷன் கார்டு விண்ணப்பம்",
        service_marriage_certificate: "திருமண சான்றிதழ் பதிவு",
        
        // Descriptions - விளக்கங்கள்
        desc_driving_license: "புதிய ஓட்டுநர் உரிமத்திற்கு விண்ணப்பிக்கவும், கற்றல் அனுமதி அல்லது உங்கள் தற்போதைய உரிமத்தை புதுப்பிக்கவும். இரு சக்கர வாகனங்கள், நான்கு சக்கர வாகனங்கள் மற்றும் வணிக வாகனங்களுக்கு கிடைக்கும்.",
        desc_passport: "இந்திய கடவுச்சீட்டிற்கு விண்ணப்பிக்கவும், காலாவதியான கடவுச்சீட்டை புதுப்பிக்கவும் அல்லது தாக்கல் (அவசர) கடவுச்சீட்டு சேவைகளுக்கு விண்ணப்பிக்கவும்.",
        desc_pan_card: "அனைத்து நிதி பரிவர்த்தனைகள், வரி தாக்கல் மற்றும் வங்கி சேவைகளுக்கு தேவையான நிரந்தர கணக்கு எண் (PAN) அட்டைக்கு விண்ணப்பிக்கவும்.",
        desc_aadhaar: "ஆதார் அட்டைக்கு விண்ணப்பிக்கவும் - இந்தியாவின் தனித்துவமான 12 இலக்க அடையாள எண். மக்கள்தொகை, உயிரியல் அளவீடு மற்றும் இ-ஆதார் பதிவிறக்கம்.",
        desc_birth_certificate: "பிறப்பை பதிவு செய்து அதிகாரப்பூர்வ பிறப்பு சான்றிதழைப் பெறுங்கள் - பள்ளி சேர்க்கை, கடவுச்சீட்டு மற்றும் பிற சேவைகளுக்கு அவசியமான ஆவணம்.",
        desc_voter_id: "தேர்தல் புகைப்பட அடையாள அட்டைக்கு (EPIC) விண்ணப்பிக்கவும் - தேர்தல்களில் வாக்களிக்க அவசியமானது மற்றும் அடையாளம் மற்றும் முகவரி சான்றாக பயனுள்ளதாக இருக்கும்.",
        desc_ration_card: "பொது விநியோக முறை (PDS) மூலம் மானிய உணவு தானியங்கள் மற்றும் அத்தியாவசிய பொருட்களைப் பெற ரேஷன் கார்டுக்கு விண்ணப்பிக்கவும்.",
        desc_marriage_certificate: "உங்கள் திருமணத்தை பதிவு செய்து அதிகாரப்பூர்வ திருமண சான்றிதழைப் பெறுங்கள் - பல்வேறு சேவைகளுக்கு தேவையான திருமணத்தின் சட்ட ஆதாரம்."
    }
};

// Current language
let currentLanguage = localStorage.getItem('language') || 'en';

// Get translation
function t(key) {
    return translations[currentLanguage][key] || translations['en'][key] || key;
}

// Set language
function setLanguage(lang) {
    if (translations[lang]) {
        currentLanguage = lang;
        localStorage.setItem('language', lang);
        updatePageLanguage();
    }
}

// Update all text on page
function updatePageLanguage() {
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key);
        
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.placeholder = translation;
        } else {
            element.textContent = translation;
        }
    });
    
    // Update language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-lang') === currentLanguage) {
            btn.classList.add('active');
        }
    });
    
    // Reload dynamic content if needed
    if (typeof loadServices === 'function') {
        loadServices();
    }
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function() {
    updatePageLanguage();
});
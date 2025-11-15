import os
from email_service import EmailService, PremiumSuggestionService
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Test email configuration
def test_email_config():
    print("Testing email configuration...")
    print(f"MAIL_SERVER: {os.getenv('MAIL_SERVER')}")
    print(f"MAIL_PORT: {os.getenv('MAIL_PORT')}")
    print(f"MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
    print(f"MAIL_DEFAULT_SENDER: {os.getenv('MAIL_DEFAULT_SENDER')}")
    print(f"Password configured: {'Yes' if os.getenv('MAIL_PASSWORD') else 'No'}")

# Test email sending
def test_send_email():
    email_service = EmailService()
    
    # Test simple email
    print("\nTesting simple email...")
    success = email_service.send_email(
        to_email="jeewansiriwardhana5@gmail.com",
        subject="Test Email from Citizen Portal",
        html_content="<h2>Test Email</h2><p>This is a test email from your citizen portal admin system.</p>",
        text_content="Test Email\n\nThis is a test email from your citizen portal admin system."
    )
    
    if success:
        print("✅ Simple email sent successfully!")
    else:
        print("❌ Simple email failed to send")
    
    return success

# Test premium suggestions email
def test_premium_suggestions():
    # Connect to database
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client["citizen_portal"]
    
    email_service = EmailService()
    premium_service = PremiumSuggestionService(db, email_service)
    
    print("\nTesting premium suggestions...")
    
    # Get premium candidates
    candidates = premium_service.analyze_premium_candidates()
    print(f"Found {len(candidates)} premium candidates")
    
    if candidates:
        # Test sending premium suggestion email to first candidate
        candidate = candidates[0]
        success = email_service.send_premium_suggestion_email(
            candidate["user_email"],
            candidate["user_name"],
            [candidate]
        )
        
        if success:
            print("✅ Premium suggestion email sent successfully!")
        else:
            print("❌ Premium suggestion email failed to send")
    else:
        print("No premium candidates found - run create_test_data.py first")

# Test admin report email
def test_admin_report():
    # Connect to database
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client["citizen_portal"]
    
    email_service = EmailService()
    premium_service = PremiumSuggestionService(db, email_service)
    
    print("\nTesting admin report email...")
    
    # Generate report data
    report_data = premium_service.generate_admin_report()
    print(f"Report data: {report_data}")
    
    # Send admin report
    success = email_service.send_admin_report_email(
        "jeewansiriwardhana5@gmail.com",
        report_data
    )
    
    if success:
        print("✅ Admin report email sent successfully!")
    else:
        print("❌ Admin report email failed to send")

if __name__ == "__main__":
    print("=== Email System Test ===")
    
    # Test configuration
    test_email_config()
    
    # Test basic email
    email_works = test_send_email()
    
    if email_works:
        print("\n=== Testing Advanced Features ===")
        # Test premium suggestions
        test_premium_suggestions()
        
        # Test admin report
        test_admin_report()
    else:
        print("\n❌ Basic email failed - check your SMTP configuration")
        print("\nCommon issues:")
        print("1. Gmail requires App Password, not regular password")
        print("2. Enable 2-Factor Authentication on Gmail")
        print("3. Generate App Password in Google Account settings")
        print("4. Use the 16-character App Password in MAIL_PASSWORD")
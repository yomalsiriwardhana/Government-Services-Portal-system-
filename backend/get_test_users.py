"""
Get test user credentials for manual testing
"""
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

print("\n" + "=" * 70)
print("TEST USER CREDENTIALS")
print("=" * 70)

# Find teacher
teacher = db.users.find_one({'job': {'$regex': 'teacher', '$options': 'i'}})
if teacher:
    print(f"\n👨‍🏫 TEACHER:")
    print(f"   Email: {teacher.get('email', 'N/A')}")
    print(f"   Name: {teacher.get('name', 'N/A')}")
    print(f"   Job: {teacher.get('job', 'N/A')}")
    print(f"   Password: test123 (default)")

# Find software engineer
engineer = db.users.find_one({'job': {'$regex': 'software|engineer', '$options': 'i'}})
if engineer:
    print(f"\n💻 SOFTWARE ENGINEER:")
    print(f"   Email: {engineer.get('email', 'N/A')}")
    print(f"   Name: {engineer.get('name', 'N/A')}")
    print(f"   Job: {engineer.get('job', 'N/A')}")
    print(f"   Password: test123 (default)")

# Find student
student = db.users.find_one({'job': {'$regex': 'student', '$options': 'i'}})
if student:
    print(f"\n🎓 STUDENT:")
    print(f"   Email: {student.get('email', 'N/A')}")
    print(f"   Name: {student.get('name', 'N/A')}")
    print(f"   Job: {student.get('job', 'N/A')}")
    print(f"   Password: test123 (default)")

print("\n" + "=" * 70)
print("TESTING STEPS:")
print("=" * 70)
print("\n1. Go to: http://localhost:5000")
print("2. Click 'Login' and use one of the emails above")
print("3. Password is usually: test123 (or password123)")
print("4. After login, use the search bar to search for:")
print("   - 'O/L results' (for education-related ads)")
print("   - 'How to get passport' (for travel ads)")
print("   - 'Driving license' (for vehicle ads)")
print("5. Go to Dashboard to see personalized ads")
print("\n" + "=" * 70)

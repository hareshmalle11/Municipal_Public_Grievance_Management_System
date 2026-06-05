import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

from services.supabase_client import supabase
from services.security import hash_password

def seed_test_officer():
    print("Checking officers...")
    existing = supabase.select("officers", params={"username": "eq.officer_rajesh", "limit": "1"})
    
    if existing:
        print("Officer 'officer_rajesh' already exists.")
        return
        
    try:
        officer_data = {
            "officer_name": "Municipal Officer Rajesh",
            "username": "officer_rajesh",
            "email": "officer_rajesh@municipal.gov.in",
            "password_hash": hash_password("officerpassword"),
            "locality": "Madhapur",
            "is_active": True
        }
        new_off = supabase.insert("officers", officer_data)
        print(f"Created default officer 'officer_rajesh' (password: officerpassword, ID: {new_off.get('officer_id')})")
    except Exception as e:
        print(f"Error seeding officer: {e}")

if __name__ == "__main__":
    print("Starting locality-based database seed...")
    seed_test_officer()
    print("Seeding completed.")

#!/usr/bin/env python
"""
Setup script to initialize the Boat Menu AI Assistant application.
Run this after installing requirements to set up the database and create admin user.
"""

import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_ai.settings')
django.setup()

from django.contrib.auth import get_user_model
from assistant.models import City, Boat

def setup_database():
    """Set up initial database with sample data."""
    print("=" * 60)
    print("🚢 Boat Menu AI Assistant - Initial Setup")
    print("=" * 60)
    
    # Create superuser
    User = get_user_model()
    
    print("\n📝 Creating Admin User...")
    if not User.objects.filter(username='admin').exists():
        username = input("Enter admin username (default: admin): ").strip() or 'admin'
        email = input("Enter admin email (default: admin@example.com): ").strip() or 'admin@example.com'
        password = input("Enter admin password (default: admin123): ").strip() or 'admin123'
        
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Admin user '{username}' created successfully!")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
    else:
        print("ℹ️  Admin user already exists.")
    
    # Add sample cities
    print("\n🏙️  Adding Sample Cities...")
    cities_data = [
        ('Ahmedabad', 'અમદાવાદ'),
        ('Surat', 'સુરત'),
        ('Vadodara', 'વડોદરા'),
        ('Rajkot', 'રાજકોટ'),
    ]
    
    for name, name_gujarati in cities_data:
        city, created = City.objects.get_or_create(
            name=name,
            defaults={'name_gujarati': name_gujarati}
        )
        if created:
            print(f"   ✅ Added: {name} ({name_gujarati})")
        else:
            print(f"   ℹ️  Exists: {name}")
    
    # Add sample boats
    print("\n⛵ Adding Sample Boats...")
    boats_data = [
        ('Sea Princess', 'સી પ્રિન્સેસ', 'Ahmedabad', 'BP-001', 150),
        ('Ocean Star', 'ઓશન સ્ટાર', 'Ahmedabad', 'BP-002', 120),
        ('River Queen', 'રિવર ક્વીન', 'Surat', 'BP-101', 100),
        ('Water Wave', 'વોટર વેવ', 'Surat', 'BP-102', 80),
    ]
    
    for name, name_gujarati, city_name, boat_number, capacity in boats_data:
        try:
            city = City.objects.get(name=city_name)
            boat, created = Boat.objects.get_or_create(
                name=name,
                city=city,
                defaults={
                    'name_gujarati': name_gujarati,
                    'boat_number': boat_number,
                    'capacity': capacity,
                    'is_active': True
                }
            )
            if created:
                print(f"   ✅ Added: {name} in {city_name}")
            else:
                print(f"   ℹ️  Exists: {name}")
        except City.DoesNotExist:
            print(f"   ❌ City {city_name} not found for boat {name}")
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("   1. Run: python manage.py runserver")
    print("   2. Visit: http://127.0.0.1:8000/admin/")
    print("   3. Login with your admin credentials")
    print("   4. Add menu entries manually or upload Excel files")
    print("\n🌐 User Interface: http://127.0.0.1:8000/")
    print("=" * 60)

if __name__ == '__main__':
    setup_database()

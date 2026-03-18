#!/usr/bin/env python
"""
Automated setup script - creates admin and sample data without prompts.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_ai.settings')
django.setup()

from django.contrib.auth import get_user_model
from assistant.models import City, Boat
from datetime import datetime, time

def setup():
    print("=" * 60)
    print("🚢 Boat Menu AI Assistant - Auto Setup")
    print("=" * 60)
    
    User = get_user_model()
    
    # Create admin user
    print("\n📝 Creating Admin User...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Admin user created!")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("ℹ️  Admin user already exists")
    
    # Add cities
    print("\n🏙️  Adding Cities...")
    cities_data = [
        ('Ahmedabad', 'અમદાવાદ'),
        ('Surat', 'સુરત'),
        ('Vadodara', 'વડોદરા'),
        ('Rajkot', 'રાજકોટ'),
    ]
    
    for name, name_gujarati in cities_data:
        city, created = City.objects.get_or_create(
            name=name,
            defaults={'name_gujarati': name_gujarati, 'is_active': True}
        )
        status = "✅ Added" if created else "ℹ️  Exists"
        print(f"   {status}: {name} ({name_gujarati})")
    
    # Add boats
    print("\n⛵ Adding Boats...")
    boats_data = [
        ('Sea Princess', 'સી પ્રિન્સેસ', 'Ahmedabad', 'BP-001', 150),
        ('Ocean Star', 'ઓશન સ્ટાર', 'Ahmedabad', 'BP-002', 120),
        ('River Queen', 'રિવર ક્વીન', 'Surat', 'BP-101', 100),
        ('Water Wave', 'વોટર વેવ', 'Surat', 'BP-102', 80),
        ('Royal Boat', 'રોયલ બોટ', 'Vadodara', 'BP-201', 90),
        ('King Fisher', 'કિંગ ફિશર', 'Rajkot', 'BP-301', 110),
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
                    'is_active': True,
                    'description': f'A beautiful boat operating in {city_name}'
                }
            )
            status = "✅ Added" if created else "ℹ️  Exists"
            print(f"   {status}: {name} in {city_name}")
        except Exception as e:
            print(f"   ❌ Error adding {name}: {e}")
    
    # Add sample menu for today
    print("\n🍽️  Adding Sample Menu for Today...")
    from assistant.models import MenuEntry
    from datetime import date
    
    try:
        boat = Boat.objects.filter(is_active=True).first()
        if boat:
            today = date.today()
            
            # Breakfast
            MenuEntry.objects.get_or_create(
                boat=boat,
                meal_type='નાસ્તો',
                date=today,
                defaults={
                    'items': 'પોહા, ઢોકળા, ચા, કોફી',
                    'time_from': time(8, 0),
                    'time_to': time(9, 30),
                    'price': 50,
                    'special_note': 'તાજું બનાવેલું નાસ્તો'
                }
            )
            
            # Lunch
            MenuEntry.objects.get_or_create(
                boat=boat,
                meal_type='બપોર',
                date=today,
                defaults={
                    'items': 'રોટલી, દાળ, ભાત, શાક, સલાડ',
                    'time_from': time(12, 0),
                    'time_to': time(14, 0),
                    'price': 100,
                    'special_note': 'થાળી સ્ટાઇલ ભોજન'
                }
            )
            
            # Dinner
            MenuEntry.objects.get_or_create(
                boat=boat,
                meal_type='રાત',
                date=today,
                defaults={
                    'items': 'રોટલી, પરાઠા, પનીર સબ્જી, દહીં',
                    'time_from': time(20, 0),
                    'time_to': time(22, 0),
                    'price': 120,
                    'special_note': 'સ્પેશિયલ ડિનર'
                }
            )
            
            print(f"   ✅ Sample menu added for {boat.name}")
        else:
            print("   ℹ️  No boats available for sample menu")
    except Exception as e:
        print(f"   ⚠️  Could not add sample menu: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n📋 Quick Start:")
    print("   1. Run: python manage.py runserver")
    print("   2. Admin: http://127.0.0.1:8000/admin/")
    print("   3. Login: admin / admin123")
    print("   4. User UI: http://127.0.0.1:8000/")
    print("=" * 60)
    print("\n💡 Tips:")
    print("   - Go to Admin → Menu Entries to add more menus")
    print("   - Upload Excel files in Admin → Excel Uploads")
    print("   - Sample menu added for today!")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    setup()

# 🚢 Quick Reference Card

## 🔗 URLs
- **User App:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 🔐 Admin Login
```
Username: admin
Password: admin123
```

## ⚡ Quick Commands

### Start Server
```bash
python manage.py runserver
```

### Stop Server
Press `Ctrl + C`

### Reset Everything
```bash
del db.sqlite3
python manage.py migrate
python auto_setup.py
```

### Add Menu via Admin
Admin → Menu Entries → Add Menu Entry

### Upload Excel
Admin → Excel Uploads → Add Excel Upload

## 📊 Excel Format
```
Boat Name | Meal Type | Date | Items | Time From | Time To | Price | Special Note
```

## 🎯 Sample Queries (User Interface)
- નાસ્તો (Breakfast)
- બપોર (Lunch)
- રાત (Dinner)
- મેનૂ (Full Menu)
- સમય (Timings)

## ✅ What's Set Up
- 4 Cities (અમદાવાદ, સુરત, વડોદરા, રાજકોટ)
- 6 Boats across cities
- Sample menu for today
- Admin user ready
- All features working

## 📝 Admin Sections
1. **Cities** - Manage cities
2. **Boats** - Manage boats
3. **Menu Entries** - Add/edit menus
4. **Excel Uploads** - Bulk upload menus
5. **User Queries** - View analytics

## 🎨 User Features
✅ City & Boat Selection
✅ Voice Input (browser support)
✅ Text Input
✅ Gujarati Language
✅ Animated AI Orb
✅ Mobile Responsive

---
**Need Help?** Check [SUCCESS.md](SUCCESS.md) for detailed guide!

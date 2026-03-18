# Quick Start Guide

## 🚀 Installation & Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Setup Initial Data (Creates admin user & sample data)
```bash
python setup_initial_data.py
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

*(You can customize these during setup)*

### Step 4: Run the Server
```bash
python manage.py runserver
```

## 🎯 Access Points

- **User Interface**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📝 Admin Panel Features

### 1. **Login**
- Go to: http://127.0.0.1:8000/admin/
- Enter admin username and password
- Click "Log in"

### 2. **Manage Cities**
- Click on "Cities" in admin panel
- Add new cities with English and Gujarati names
- Mark cities as active/inactive

### 3. **Manage Boats**
- Click on "Boats" in admin panel
- Add new boats with:
  - Boat name (English & Gujarati)
  - Select city
  - Boat number
  - Capacity
  - Description

### 4. **Add Menu Manually**
- Click on "Menu Entries" in admin panel
- Click "Add Menu Entry"
- Fill in:
  - Select Boat
  - Meal Type (નાસ્તો, બપોર, રાત)
  - Date
  - Menu Items
  - Time From/To
  - Price
  - Special Notes

### 5. **Upload Menu via Excel**
- Click on "Excel Uploads" in admin panel
- Click "Add Excel Upload"
- Select Excel file
- Choose City
- Click Save
- System automatically processes and creates menu entries!

**Excel Format:**
```
| Boat Name | Meal Type | Date       | Items           | Time From | Time To | Price | Special Note |
|-----------|-----------|------------|-----------------|-----------|---------|-------|--------------|
| સી પ્રિન્સેસ | નાસ્તો    | 2026-01-06 | પોહા, ઢોકળા, ચા | 08:00    | 09:30   | 50    | તાજું        |
```

See [EXCEL_FORMAT_GUIDE.md](EXCEL_FORMAT_GUIDE.md) for detailed format.

## 🎨 User Interface Usage

1. Open: http://127.0.0.1:8000/
2. Select City from dropdown
3. Select Boat from dropdown
4. Ask questions:
   - "નાસ્તો" - Get breakfast menu
   - "બપોર" - Get lunch menu
   - "રાત" - Get dinner menu
   - "મેનૂ" - Get full day menu
   - "સમય" - Get meal timings

## 🔧 Troubleshooting

### Database Error?
```bash
# Delete database and recreate
del db.sqlite3
python manage.py migrate
python setup_initial_data.py
```

### Static Files Not Loading?
```bash
python manage.py collectstatic --noinput
```

### Can't Login to Admin?
```bash
# Create new superuser
python manage.py createsuperuser
```

### Excel Upload Not Working?
- Ensure `pandas` and `openpyxl` are installed
- Check file format matches guide
- Verify boat names exist in database
- Check error log in Excel Upload record

## 📊 Database Models

- **City**: Cities where boats operate
- **Boat**: Boat information linked to cities
- **Menu Entry**: Daily menus for each boat
- **Excel Upload**: Tracks uploaded Excel files
- **Query**: Stores user queries for analytics

## 🔐 Security Notes

**Important for Production:**
1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Change admin password from default
4. Configure `ALLOWED_HOSTS`
5. Use PostgreSQL instead of SQLite
6. Set up proper media file storage

## 📱 Features

✅ Multi-city boat management
✅ Gujarati language support
✅ Voice recognition (browser-based)
✅ Text-to-speech responses
✅ Excel bulk upload
✅ Admin panel for management
✅ Mobile responsive design
✅ Query analytics
✅ Animated AI orb interface

## 🆘 Need Help?

Check the following files:
- [README.md](README.md) - Full documentation
- [EXCEL_FORMAT_GUIDE.md](EXCEL_FORMAT_GUIDE.md) - Excel upload format
- Django Admin Panel - Has built-in help text

## 🎉 Quick Test

After setup:
1. Login to admin
2. Add a menu entry for today
3. Go to user interface
4. Select city and boat
5. Ask "મેનૂ" to see the menu!

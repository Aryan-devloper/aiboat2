# 🚢 બોટ મેનૂ AI સહાયક (Boat Menu AI Assistant)

A modern, futuristic AI voice assistant web application built with Django for boat menu management and queries in Gujarati.

## Features

- 🎨 Beautiful futuristic UI with animated AI orb
- 🎤 Voice recognition (Gujarati language support)
- 🔊 Text-to-speech responses
- 💬 Text-based chat interface
- 📱 Fully mobile responsive
- 🌐 Django backend with API
- 💾 Database models for menu management

## 🚀 Quick Installation (Windows)

**Automatic Setup:**
```bash
setup.bat
```

**Manual Setup:**
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Setup initial data: `python setup_initial_data.py`
4. Start server: `python manage.py runserver`

**Access:**
- User Interface: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- Default Login: `admin` / `admin123`

📖 See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## Project Structure

```
hostel_ai/
├── hostel_ai/          # Main project directory
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL configuration
│   └── wsgi.py         # WSGI config
├── assistant/          # Main app
│   ├── models.py       # Database models
│   ├── views.py        # Views and API endpoints
│   ├── urls.py         # App URL configuration
│   ├── admin.py        # Admin configuration
│   ├── static/         # Static files (CSS, JS)
│   └── templates/      # HTML templates
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Usage

### Voice Commands (Gujarati):
- "નાસ્તો" - Ask about breakfast
- "બપોર" - Ask about lunch
- "રાત" - Ask about dinner
- "મેનૂ" - Get full menu
- "સમય" - Get meal timings

### Admin Panel:
Log in to the admin panel to:
- Manage daily menu entries
- View user query analytics
- Update meal timings and items

## API Endpoints

- `GET /` - Main application page
- `POST /api/query/` - Submit queries (accepts JSON with `query` field)

## Models

### MenuEntry
- Stores daily menu items
- Fields: meal_type, items, time_from, time_to, date

### Query
- Stores user queries for analytics
- Fields: query_text, response_text, timestamp

## Technologies Used

- **Backend:** Django 5.0
- **Frontend:** HTML5, CSS3, JavaScript
- **APIs:** Web Speech API (Recognition & Synthesis)
- **Database:** SQLite (default, can be changed)

## Browser Support

For best experience, use:
- Google Chrome
- Microsoft Edge
- Safari (limited Gujarati voice support)

## Development

To make changes:

1. Modify templates in `assistant/templates/assistant/`
2. Update styles in `assistant/static/assistant/css/`
3. Edit JavaScript in `assistant/static/assistant/js/`
4. Add/modify views in `assistant/views.py`

## Production Deployment

Before deploying to production:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use a production database (PostgreSQL recommended)
5. Run `python manage.py collectstatic`
6. Use a production WSGI server (gunicorn, uWSGI)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the documentation or contact the development team.

@echo off
echo ========================================
echo Boat Menu AI Assistant - Quick Setup
echo ========================================
echo.

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo [3/4] Setting up initial data...
python setup_initial_data.py
if errorlevel 1 (
    echo ERROR: Failed to setup initial data
    pause
    exit /b 1
)

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo Access the application:
echo   - User Interface: http://127.0.0.1:8000/
echo   - Admin Panel: http://127.0.0.1:8000/admin/
echo.
echo Default Admin Login:
echo   Username: admin
echo   Password: admin123
echo ========================================
echo.
echo To start the server, run:
echo   python manage.py runserver
echo.
pause

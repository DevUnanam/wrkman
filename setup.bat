@echo off
echo ========================================
echo    ArtisanConnect Setup Script
echo ========================================
echo.

echo 1. Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 2. Making migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ERROR: Failed to make migrations
    pause
    exit /b 1
)

echo.
echo 3. Applying migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to apply migrations
    pause
    exit /b 1
)

echo.
echo 4. Creating sample data...
python manage.py populate_data
if %errorlevel% neq 0 (
    echo ERROR: Failed to create sample data
    pause
    exit /b 1
)

echo.
echo ========================================
echo       Setup completed successfully!
echo ========================================
echo.
echo Login credentials:
echo Admin: admin / admin123
echo Client: john_client / password123
echo Artisan: ahmed_plumber / password123
echo.
echo To start the server, run:
echo python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/
echo.
pause
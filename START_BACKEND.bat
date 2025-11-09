@echo off
echo ========================================
echo Starting Empire Automation Backend API
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo [2/3] Checking database...
if not exist "empire.db" (
    echo Database not found. Initializing...
    python -m empire_automation.database.init_db
    if errorlevel 1 (
        echo ERROR: Database initialization failed!
        pause
        exit /b 1
    )
)

echo [3/3] Starting API server on http://localhost:8000...
echo.
echo ========================================
echo Backend will be available at:
echo   Health: http://localhost:8000/api/health
echo   Docs:   http://localhost:8000/docs
echo ========================================
echo.
echo Press CTRL+C to stop the server
echo.

python start_api.py

pause


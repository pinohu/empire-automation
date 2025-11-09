# PowerShell script to start backend API server
# Run: .\start_backend.ps1

Write-Host "🚀 Starting Empire Automation Backend API" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\python.exe") {
    Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\python.exe" --version
} else {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Create one with: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Check if database exists
if (-not (Test-Path "empire.db")) {
    Write-Host "[2/3] Database not found. Initializing..." -ForegroundColor Yellow
    & "venv\Scripts\python.exe" -m empire_automation.database.init_db
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Database initialization failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Database initialized" -ForegroundColor Green
} else {
    Write-Host "[2/3] Database found, skipping initialization" -ForegroundColor Gray
}

# Start API server
Write-Host "[3/3] Starting API server on http://localhost:8000..." -ForegroundColor Yellow
Write-Host ""
Write-Host "API will be available at:" -ForegroundColor Cyan
Write-Host "  Health: http://localhost:8000/api/health" -ForegroundColor White
Write-Host "  Docs:   http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

& "venv\Scripts\python.exe" start_api.py


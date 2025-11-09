# Launch Empire Automation System
# PowerShell version for Windows

Write-Host "🚀 Launching Empire Automation System" -ForegroundColor Cyan
Write-Host ""

# Start all services
Write-Host "[1/6] Starting Docker services..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services
Write-Host "[2/6] Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if initialized
$initializedFile = ".initialized"
if (-not (Test-Path $initializedFile)) {
    Write-Host "[3/6] First time setup..." -ForegroundColor Yellow
    
    # Initialize database
    Write-Host "  - Initializing database..." -ForegroundColor Gray
    .\venv\Scripts\python.exe empire_automation\database\init_db.py
    
    # Seed data
    Write-Host "  - Seeding database..." -ForegroundColor Gray
    .\venv\Scripts\python.exe empire_automation\database\seed_data.py
    
    # Mark as initialized
    New-Item -ItemType File -Path $initializedFile -Force | Out-Null
    Write-Host "  [OK] Database initialized" -ForegroundColor Green
} else {
    Write-Host "[3/6] System already initialized, skipping setup..." -ForegroundColor Gray
}

# Check if API is already running
Write-Host "[4/6] Checking API status..." -ForegroundColor Yellow
try {
    $apiResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "  [OK] API already running on port 8000" -ForegroundColor Green
} catch {
    Write-Host "  [INFO] Starting API server..." -ForegroundColor Gray
    Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "empire_automation.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -WindowStyle Minimized
    Start-Sleep -Seconds 3
    Write-Host "  [OK] API started" -ForegroundColor Green
}

# Check if Dashboard is already running
Write-Host "[5/6] Checking Dashboard status..." -ForegroundColor Yellow
try {
    $dashboardResponse = Invoke-WebRequest -Uri "http://localhost:8501" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "  [OK] Dashboard already running on port 8501" -ForegroundColor Green
} catch {
    Write-Host "  [INFO] Starting Dashboard..." -ForegroundColor Gray
    Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8501" -WindowStyle Minimized
    Start-Sleep -Seconds 3
    Write-Host "  [OK] Dashboard started" -ForegroundColor Green
}

# Verify services
Write-Host "[6/6] Verifying services..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ System launched!" -ForegroundColor Green
Write-Host ""
Write-Host "Services:" -ForegroundColor Cyan
Write-Host "  📡 API:        http://localhost:8000" -ForegroundColor White
Write-Host "  📊 Dashboard:  http://localhost:8501" -ForegroundColor White
Write-Host "  🔄 n8n:        http://localhost:5678" -ForegroundColor White
Write-Host "  📚 API Docs:   http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Open dashboard: http://localhost:8501" -ForegroundColor White
Write-Host "  2. Navigate to '90-Day Plan' page" -ForegroundColor White
Write-Host "  3. Execute Day 1 tasks" -ForegroundColor White
Write-Host "  4. Review daily briefing" -ForegroundColor White
Write-Host ""

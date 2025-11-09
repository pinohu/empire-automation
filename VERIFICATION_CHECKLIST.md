# System Verification Checklist

## Quick Verification Commands

### 1. Check Docker Services
```bash
docker-compose ps
```
**Expected:** All services (postgres, redis, n8n) should show "Up" status

### 2. Check Database Connection
```bash
python -c "from empire_automation.database.models import *; print('DB OK')"
```
**Expected:** Should print "DB OK" without errors

### 3. Test API Health
```bash
curl http://localhost:8000/api/health
```
**Expected:** `{"status":"healthy","timestamp":"..."}`

### 4. Test Dashboard
```bash
# Streamlit runs on port 8501
# Open in browser: http://localhost:8501
# Or check if process is running:
netstat -an | findstr :8501
```

### 5. Test n8n Health
```bash
curl http://localhost:5678/healthz
```
**Expected:** `{"status":"ok"}` or similar

### 6. Run All Tests
```bash
pytest tests/ -v
```
**Expected:** All tests should pass (some may skip if services not configured)

### 7. Check Docker Logs
```bash
docker-compose logs -f
```
**Expected:** No critical errors in logs

## Service Status

### PostgreSQL
- **Port:** 5432
- **Database:** empire_automation
- **Check:** `docker-compose ps postgres`

### Redis
- **Port:** 6379
- **Check:** `docker-compose ps redis`

### n8n
- **Port:** 5678
- **Web UI:** http://localhost:5678
- **Check:** `docker-compose ps n8n`

### FastAPI
- **Port:** 8000
- **API Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/api/health
- **Check:** Process should be running (started with `uvicorn`)

### Streamlit Dashboard
- **Port:** 8501
- **URL:** http://localhost:8501
- **Check:** Process should be running (started with `streamlit run`)

## Common Issues

### Services Not Running
- **Solution:** Run `docker-compose up -d` to start services
- **Check:** `docker-compose ps` to verify

### Database Connection Failed
- **Solution:** Ensure PostgreSQL container is running
- **Check:** `docker-compose logs postgres`

### API Not Responding
- **Solution:** Start API with `uvicorn empire_automation.api.main:app --reload --port 8000`
- **Check:** `curl http://localhost:8000/api/health`

### Dashboard Not Accessible
- **Solution:** Start dashboard with `streamlit run dashboard/app.py`
- **Check:** Open http://localhost:8501 in browser

### Tests Failing
- **Solution:** Ensure all services are running and database is initialized
- **Check:** Run `python database/init_db.py` if needed

## Full System Check Script

```bash
#!/bin/bash
# Run all verification checks

echo "=== System Verification ==="
echo ""

echo "1. Docker Services:"
docker-compose ps
echo ""

echo "2. Database Connection:"
python -c "from empire_automation.database.models import *; print('DB OK')"
echo ""

echo "3. API Health:"
curl http://localhost:8000/api/health
echo ""

echo "4. n8n Health:"
curl http://localhost:5678/healthz
echo ""

echo "5. Running Tests:"
pytest tests/ -v
echo ""

echo "=== Verification Complete ==="
```

## Windows PowerShell Version

```powershell
# System Verification Script
Write-Host "=== System Verification ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Docker Services:" -ForegroundColor Yellow
docker-compose ps
Write-Host ""

Write-Host "2. Database Connection:" -ForegroundColor Yellow
python -c "from empire_automation.database.models import *; print('DB OK')"
Write-Host ""

Write-Host "3. API Health:" -ForegroundColor Yellow
curl http://localhost:8000/api/health
Write-Host ""

Write-Host "4. n8n Health:" -ForegroundColor Yellow
curl http://localhost:5678/healthz
Write-Host ""

Write-Host "5. Running Tests:" -ForegroundColor Yellow
pytest tests/ -v
Write-Host ""

Write-Host "=== Verification Complete ===" -ForegroundColor Green
```


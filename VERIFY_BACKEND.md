# ✅ Verify Backend is Running

## Quick Check

Open in your browser: **http://localhost:8000/api/health**

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "empire-automation-api"
}
```

---

## If Backend is Not Running

### Start Backend Manually

**Option 1: PowerShell Script**
```powershell
cd empire-automation
.\start_backend.ps1
```

**Option 2: Direct Command**
```powershell
cd empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py
```

**Option 3: Using uvicorn**
```powershell
cd empire-automation
.\venv\Scripts\Activate.ps1
uvicorn empire_automation.api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Check Backend Status

### Test 1: Health Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/health"
```

### Test 2: API Documentation
Open: **http://localhost:8000/docs**

Should show Swagger UI with all endpoints.

### Test 3: Root Endpoint
Open: **http://localhost:8000/**

Should return API info.

---

## After Backend Starts

1. **Wait 2-3 seconds** for server to fully start
2. **Refresh frontend** (http://localhost:3000)
3. **Check API status bar** - Should turn green "✅ API Connected"
4. **Data should appear** on all pages

---

## Troubleshooting

### Backend Won't Start

**Error: ModuleNotFoundError**
```powershell
cd empire-automation
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error: Port 8000 in use**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**Error: Database errors**
```powershell
python -m empire_automation.database.init_db
```

---

## Expected Terminal Output

When backend starts successfully:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

**Once you see "Uvicorn running on http://0.0.0.0:8000", refresh the frontend!** 🚀


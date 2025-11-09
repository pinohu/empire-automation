# ✅ Backend Startup Instructions

## Dependencies Installed ✅

The missing `slowapi` package has been installed. The backend should now start successfully.

---

## Start Backend Server

A new PowerShell window should have opened with the backend server starting.

**If the window didn't open, start manually:**

```powershell
cd empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py
```

---

## Expected Output

You should see in the terminal:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Keep this terminal window open** - the backend needs to keep running.

---

## Verify Backend is Running

### Test 1: Health Endpoint

Open in browser: **http://localhost:8000/api/health**

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "empire-automation-api"
}
```

### Test 2: API Documentation

Open: **http://localhost:8000/docs**

Should show Swagger UI with all API endpoints.

---

## After Backend Starts

1. **Wait 2-3 seconds** for server to fully initialize
2. **Go to frontend** (http://localhost:3000)
3. **Refresh the page** (F5)
4. **Check API status bar** - Should show "✅ API Connected" (green)
5. **Data should appear** on all pages

---

## Expected Warnings (Safe to Ignore)

You may see these warnings - they're **normal** and won't prevent the backend from running:

```
AgenticFlow not available: AGENTICFLOW_API_KEY environment variable is required
Google Workspace features will be disabled
```

These are for optional integrations that can be configured later.

---

## Troubleshooting

### Backend Still Won't Start

**Check the terminal window** for error messages. Common issues:

1. **Port 8000 in use:**
   ```powershell
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. **Database errors:**
   ```powershell
   python -m empire_automation.database.init_db
   ```

3. **Import errors:**
   ```powershell
   pip install -r requirements.txt
   ```

---

**Once you see "Uvicorn running on http://0.0.0.0:8000", refresh your frontend!** 🚀


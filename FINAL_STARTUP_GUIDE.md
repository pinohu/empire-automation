# ✅ Final Startup Guide - Backend Ready!

## Status: ✅ All Issues Fixed

1. ✅ Missing dependencies installed (`slowapi`, `redis`)
2. ✅ Health endpoint route fixed
3. ✅ Rate limiting made optional
4. ✅ App loads successfully

---

## 🚀 Start Backend (Choose One Method)

### Method 1: PowerShell Script

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\start_backend.ps1
```

### Method 2: Manual Commands

**Open PowerShell and run:**

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py
```

### Method 3: Direct Python

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\python.exe start_api.py
```

---

## ✅ What You Should See

When backend starts successfully:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Keep this terminal window open!**

---

## ✅ Verify Backend is Running

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

Should show Swagger UI with all endpoints listed.

---

## 🎯 After Backend Starts

1. **Wait 3-5 seconds** for full startup
2. **Go to frontend**: http://localhost:3000
3. **Refresh page** (F5 or Ctrl+R)
4. **Check API status bar** - Should turn **GREEN**: "✅ API Connected"
5. **Data should appear** on all dashboard pages

---

## ⚠️ Expected Warnings (Normal)

These warnings are **safe to ignore** - they're for optional features:

```
AgenticFlow not available: AGENTICFLOW_API_KEY environment variable is required
Google Workspace features will be disabled
```

The backend will still work without these.

---

## 🔧 Troubleshooting

### Backend Won't Start

**Check terminal for errors:**
- Import errors → `pip install -r requirements.txt`
- Port in use → Kill process: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`
- Database errors → `python -m empire_automation.database.init_db`

### Frontend Still Shows "Disconnected"

1. **Verify backend is running**: http://localhost:8000/api/health
2. **Check browser console** (F12) for CORS errors
3. **Wait 5 seconds** after backend starts
4. **Hard refresh**: Ctrl+Shift+R

### No Data Showing

**Initialize database:**
```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\Activate.ps1
python -m empire_automation.database.init_db
```

---

## 📋 Quick Reference

**Backend:** http://localhost:8000
**Frontend:** http://localhost:3000
**API Docs:** http://localhost:8000/docs
**Health Check:** http://localhost:8000/api/health

---

**Start the backend in a terminal window, verify it's running, then refresh your frontend!** 🚀


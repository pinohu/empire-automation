# ⚠️ Backend Not Running - All "Failed to fetch" Errors

## Problem

All the "Failed to fetch" errors you're seeing are because **the backend API server is not running**.

The frontend is trying to connect to `http://localhost:8000` but getting no response.

---

## ✅ Solution: Start the Backend

### Step 1: Open PowerShell Terminal

Press `Win + X` → Select "Windows PowerShell" or "Terminal"

### Step 2: Navigate to Project

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
```

### Step 3: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your prompt.

### Step 4: Start Backend Server

```powershell
python start_api.py
```

### Step 5: Wait for Startup

You should see:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal window open!** The backend must keep running.

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

Should show Swagger UI with all endpoints.

---

## ✅ After Backend Starts

1. **Wait 3-5 seconds** for full startup
2. **Go to frontend**: http://localhost:3000
3. **Press Ctrl+Shift+R** (hard refresh) to clear cache
4. **Check API status bar** - Should turn **GREEN**: "✅ API Connected"
5. **All "Failed to fetch" errors should disappear**
6. **Data should appear** on all pages

---

## 🔧 Troubleshooting

### Backend Won't Start

**Check terminal for errors:**

- **Import errors** → `pip install -r requirements.txt`
- **Port 8000 in use** → Kill process: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`
- **Database errors** → `python -m empire_automation.database.init_db`

### Still Getting "Failed to fetch"

1. **Verify backend is running**: http://localhost:8000/api/health
2. **Check browser console** (F12) - Look for CORS errors
3. **Check API status bar** - Should show connection status
4. **Hard refresh**: Ctrl+Shift+R

### Frontend Shows Errors But Backend is Running

1. **Check CORS settings** in backend `.env`:
   ```
   CORS_ORIGINS=http://localhost:3000,http://localhost:8501
   ```
2. **Restart backend** after changing CORS settings
3. **Clear browser cache** and refresh

---

## 📋 Quick Reference

**Backend URL:** http://localhost:8000
**Frontend URL:** http://localhost:3000
**Health Check:** http://localhost:8000/api/health
**API Docs:** http://localhost:8000/docs

---

## 🚀 Quick Start Commands

```powershell
# Terminal 1: Backend
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py

# Terminal 2: Frontend (if not already running)
cd C:\Users\polyc\Documents\Empire\empire-automation\frontend
npm run dev
```

---

**Start the backend in a terminal window, then refresh your frontend!** 🚀

All "Failed to fetch" errors will disappear once the backend is running.


# 📋 Manual Backend Start Instructions

## Step-by-Step Guide

### Step 1: Open PowerShell Terminal

Press `Win + X` and select "Windows PowerShell" or "Terminal"

### Step 2: Navigate to Project

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
```

### Step 3: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` appear in your prompt.

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

## Verify It's Working

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

### Test 2: API Docs

Open: **http://localhost:8000/docs**

Should show Swagger UI.

---

## After Backend Starts

1. **Go to frontend**: http://localhost:3000
2. **Refresh page** (F5)
3. **Check status bar** - Should show "✅ API Connected" (green)
4. **Data should appear** on all pages

---

## Common Errors & Fixes

### Error: "ModuleNotFoundError"

```powershell
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "Database not found"

```powershell
python -m empire_automation.database.init_db
```

---

## Two Terminal Windows Needed

**Terminal 1: Backend**
```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py
```

**Terminal 2: Frontend**
```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation\frontend
npm run dev
```

---

**Start the backend manually in a terminal, then refresh your frontend!** 🚀


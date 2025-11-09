# 🚀 Start Backend API - Step by Step

## The Issue

The backend API server is not running, which is why:
- Health endpoint doesn't work
- Frontend shows "Checking API connection..."
- No data displays on pages

---

## Solution: Start the Backend

### Step 1: Activate Virtual Environment

```bash
cd empire-automation
.\venv\Scripts\Activate.ps1
```

**OR if using Command Prompt:**
```bash
cd empire-automation
venv\Scripts\activate.bat
```

### Step 2: Install Dependencies (if needed)

```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database (First Time Only)

```bash
python -m empire_automation.database.init_db
```

### Step 4: Start the API Server

```bash
python start_api.py
```

**OR:**

```bash
uvicorn empire_automation.api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Expected Output

When backend starts successfully, you'll see:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

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

Open in browser: **http://localhost:8000/docs**

Should show Swagger UI with all API endpoints.

---

## After Backend Starts

1. **Go back to frontend** (http://localhost:3000)
2. **Refresh the page** (F5)
3. **Check API status bar** - Should show "✅ API Connected" (green)
4. **Check browser console** (F12) - Should see successful API calls
5. **Data should appear** on all pages

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

**Solution:** Find and kill the process
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Error: "Database not found"

**Solution:** Initialize database
```bash
python -m empire_automation.database.init_db
```

### Backend starts but health endpoint still fails

**Check:**
1. Backend is actually running (check terminal output)
2. No firewall blocking port 8000
3. Try: http://localhost:8000/docs (should show API docs)

---

## Quick Commands Summary

```bash
# 1. Activate venv
cd empire-automation
.\venv\Scripts\Activate.ps1

# 2. Start backend
python start_api.py

# 3. In another terminal, start frontend
cd empire-automation\frontend
npm run dev
```

---

**Once backend is running, refresh frontend and data will appear!** ✅


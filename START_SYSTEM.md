# 🚀 Start Empire Automation System

## Quick Start Guide

To view data in the frontend, you need to start the backend API server.

---

## Step 1: Start Backend API

Open a terminal and run:

```bash
cd empire-automation
python start_api.py
```

**OR** using uvicorn directly:

```bash
cd empire-automation
uvicorn empire_automation.api.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 2: Initialize Database (First Time Only)

If this is your first time running the system:

```bash
cd empire-automation
python -m empire_automation.database.init_db
```

This creates the database tables and seeds initial data.

---

## Step 3: Verify Backend is Running

Open in browser: **http://localhost:8000/api/health**

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "empire-automation-api"
}
```

---

## Step 4: Refresh Frontend

Once backend is running:
1. Go back to your frontend (http://localhost:3000)
2. Refresh the page (F5)
3. The API status bar should change from "Checking..." to "✅ API Connected"
4. Data should now appear on all pages

---

## Troubleshooting

### Backend Won't Start

**Error: Module not found**
```bash
# Install dependencies
pip install -r requirements.txt
```

**Error: Port 8000 already in use**
```bash
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Still Shows "Checking..."

1. **Verify backend is running:**
   - Open http://localhost:8000/api/health in browser
   - Should return JSON, not timeout

2. **Check CORS:**
   - Backend should allow `http://localhost:3000`
   - Check `CORS_ORIGINS` in backend `.env`

3. **Check browser console:**
   - Press F12 → Console tab
   - Look for CORS errors or connection errors

### No Data Showing

**Database might be empty:**
```bash
# Initialize database with seed data
python -m empire_automation.database.init_db
```

---

## Running Both Services

### Terminal 1: Backend
```bash
cd empire-automation
python start_api.py
```

### Terminal 2: Frontend
```bash
cd empire-automation/frontend
npm run dev
```

---

## Expected Behavior

✅ **Backend Running:**
- API status bar shows "✅ API Connected" (green)
- Pages display data or "No data" messages
- Console shows successful API calls

❌ **Backend Not Running:**
- API status bar shows "❌ API Disconnected" (red)
- Pages show error messages
- Console shows connection errors

---

**Once backend is running, refresh the frontend and data should appear!** 🎉


# 🚀 Start Backend API Server

## Quick Start

The backend API must be running for the frontend to display data.

### Option 1: Using Python Directly

```bash
cd empire-automation
uvicorn empire_automation.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Using the Start Script

```bash
cd empire-automation
python start_api.py
```

### Option 3: Using PowerShell Script (Windows)

```powershell
cd empire-automation
.\launch.ps1
```

---

## Verify Backend is Running

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

## Initialize Database (First Time)

Before starting, initialize the database:

```bash
cd empire-automation
python -m empire_automation.database.init_db
```

---

## Troubleshooting

### Port 8000 Already in Use

```bash
# Find process using port 8000 (Windows)
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Module Not Found Errors

```bash
# Install dependencies
pip install -r requirements.txt
```

### Database Errors

```bash
# Reinitialize database
python -m empire_automation.database.init_db
```

---

## Expected Output

When backend starts successfully, you should see:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

**Once backend is running, refresh the frontend and the API status should show "✅ API Connected"**


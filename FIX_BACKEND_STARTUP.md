# 🔧 Fix Backend Startup Issues

## Issue Found: Missing Dependencies

The backend can't start because `slowapi` module is missing.

---

## ✅ Solution: Install Missing Dependencies

### Step 1: Activate Virtual Environment

```powershell
cd empire-automation
.\venv\Scripts\Activate.ps1
```

### Step 2: Install All Dependencies

```powershell
pip install -r requirements.txt
```

**OR install missing packages individually:**

```powershell
pip install slowapi redis
```

### Step 3: Verify Installation

```powershell
python -c "from empire_automation.api.main import app; print('✅ App loaded successfully!')"
```

Should output: `✅ App loaded successfully!`

### Step 4: Start Backend

```powershell
python start_api.py
```

---

## Common Missing Dependencies

If you see other `ModuleNotFoundError`, install:

```powershell
pip install slowapi redis celery sqlalchemy pydantic python-dotenv
```

---

## Verify Backend Starts

After installing dependencies, you should see:

```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Test Backend

Open in browser: **http://localhost:8000/api/health**

Should return:
```json
{"status": "healthy", "timestamp": "...", "service": "empire-automation-api"}
```

---

**After installing dependencies, start the backend and refresh the frontend!** 🚀


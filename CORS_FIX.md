# 🔧 CORS Issue - Backend Running But Frontend Can't Connect

## Problem

Backend IS running (confirmed by `/api/health` working), but frontend still gets "Failed to fetch" errors.

This is likely a **CORS (Cross-Origin Resource Sharing)** issue.

---

## ✅ Quick Fixes

### Fix 1: Hard Refresh Browser

1. **Close all browser tabs** with the frontend
2. **Clear browser cache:**
   - Press `Ctrl+Shift+Delete`
   - Select "Cached images and files"
   - Click "Clear data"
3. **Reopen frontend:** http://localhost:3000
4. **Press Ctrl+Shift+R** (hard refresh)

### Fix 2: Check CORS Configuration

**Backend CORS should include:**
- `http://localhost:3000`
- `http://127.0.0.1:3000`

**Check backend `.env` file:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8501,http://127.0.0.1:3000
```

**If missing, add it and restart backend.**

### Fix 3: Check Frontend API URL

**Check `frontend/.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**If file doesn't exist, create it.**

### Fix 4: Restart Both Services

1. **Stop backend** (Ctrl+C in backend window)
2. **Stop frontend** (Ctrl+C in frontend terminal)
3. **Start backend first:**
   ```powershell
   cd empire-automation
   .\venv\Scripts\Activate.ps1
   python start_api.py
   ```
4. **Wait 5 seconds**
5. **Start frontend:**
   ```powershell
   cd empire-automation\frontend
   npm run dev
   ```
6. **Hard refresh browser** (Ctrl+Shift+R)

---

## 🔍 Debug Steps

### Step 1: Test Backend Directly

**Open in browser:**
- http://localhost:8000/api/health ✅ Should work
- http://localhost:8000/api/v1/daily-briefing ✅ Should work
- http://localhost:8000/docs ✅ Should show Swagger UI

### Step 2: Check Browser Console

1. **Open browser DevTools** (F12)
2. **Go to Console tab**
3. **Look for CORS errors:**
   - "Access-Control-Allow-Origin"
   - "CORS policy"
   - "preflight request"

### Step 3: Check Network Tab

1. **Open DevTools** (F12)
2. **Go to Network tab**
3. **Refresh page** (F5)
4. **Look for failed requests** (red)
5. **Click on failed request**
6. **Check "Response" tab** for CORS errors

---

## ✅ Verify CORS is Working

**Test CORS in PowerShell:**

```powershell
# Test OPTIONS request (CORS preflight)
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/daily-briefing" -Method OPTIONS

# Should return 200 OK with CORS headers
```

---

## 🔧 Backend CORS Configuration

**File:** `empire_automation/api/main.py`

**Current CORS config:**
```python
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:8501,http://localhost:3000,http://127.0.0.1:8501"
).split(",")
```

**Make sure it includes:**
- `http://localhost:3000` ✅
- `http://127.0.0.1:3000` (optional but recommended)

---

## 🚀 After Fixing

1. **Restart backend** (if you changed CORS settings)
2. **Hard refresh frontend** (Ctrl+Shift+R)
3. **Check status bar** - Should turn green
4. **Check console** - No more CORS errors

---

**Try hard refresh first (Ctrl+Shift+R), then check CORS configuration!** 🔧


# 🔍 Debug Frontend Connection Issues

## Current Status

- ✅ Backend IS running (confirmed)
- ✅ Backend responds to direct requests
- ❌ Frontend still gets "Failed to fetch" errors

---

## 🔍 Step-by-Step Debugging

### Step 1: Check Browser Console

1. **Open browser DevTools** (F12)
2. **Go to Console tab**
3. **Look for exact error messages:**
   - "Failed to fetch"
   - "CORS policy"
   - "NetworkError"
   - "ERR_CONNECTION_REFUSED"

4. **Copy the exact error message** and share it

### Step 2: Check Network Tab

1. **Open DevTools** (F12)
2. **Go to Network tab**
3. **Refresh page** (F5)
4. **Look for failed requests** (red)
5. **Click on failed request**
6. **Check:**
   - **Request URL** - Should be `http://localhost:8000/api/v1/...`
   - **Status** - What status code?
   - **Response** - What does it say?
   - **Headers** - Check CORS headers

### Step 3: Test Backend Directly

**Open these in browser (should all work):**
- http://localhost:8000/api/health
- http://localhost:8000/api/v1/daily-briefing
- http://localhost:8000/docs

**If these DON'T work, backend has an issue.**

### Step 4: Check Frontend Environment

**Check if `.env.local` exists:**
```powershell
cd empire-automation\frontend
Get-Content .env.local
```

**Should contain:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**If missing or wrong, fix it and restart frontend.**

### Step 5: Check CORS

**Backend CORS config should include:**
- `http://localhost:3000`
- `http://127.0.0.1:3000`

**Check backend `.env` file:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8501,http://127.0.0.1:3000
```

---

## 🔧 Common Fixes

### Fix 1: Restart Everything

1. **Stop backend** (Ctrl+C)
2. **Stop frontend** (Ctrl+C)
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
6. **Hard refresh browser:** Ctrl+Shift+R

### Fix 2: Clear Everything

1. **Close all browser tabs**
2. **Clear browser cache:** Ctrl+Shift+Delete
3. **Close browser completely**
4. **Restart backend**
5. **Restart frontend**
6. **Open fresh browser window**
7. **Go to:** http://localhost:3000

### Fix 3: Check Firewall

1. **Windows Security** → **Firewall & network protection**
2. **Allow an app through firewall**
3. **Check:** Python is allowed for Private networks

### Fix 4: Try Different Port

**If port 8000 is blocked, try different port:**

**Backend `start_api.py`:**
```python
uvicorn.run(
    "empire_automation.api.main:app",
    host="0.0.0.0",
    port=8001,  # Change to 8001
    reload=True,
)
```

**Frontend `.env.local`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## 📋 Information Needed

**Please provide:**

1. **Exact error message** from browser console
2. **Network tab details:**
   - Request URL
   - Status code
   - Response body
3. **Backend terminal output** - Any errors?
4. **Frontend terminal output** - Any errors?

---

## 🎯 Quick Test

**Run this in PowerShell:**

```powershell
# Test if backend is accessible
Invoke-RestMethod -Uri "http://localhost:8000/api/health"

# Test daily briefing endpoint
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/daily-briefing"

# Test with Origin header (simulating browser)
$headers = @{"Origin"="http://localhost:3000"}
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/daily-briefing" -Headers $headers
```

**Share the results!**

---

**Check browser console and network tab, then share the exact error details!** 🔍


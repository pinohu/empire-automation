# 🚨 CRITICAL: Start Backend Server

## ⚠️ You're Seeing Errors Because Backend Is Not Running!

The error message **"Backend server is not running"** means you need to start the backend API server.

---

## ✅ EASIEST WAY: Double-Click

1. **Open File Explorer**
2. **Navigate to:** `C:\Users\polyc\Documents\Empire\empire-automation`
3. **Find:** `START_BACKEND.bat`
4. **DOUBLE-CLICK IT**
5. **A black window opens** - **KEEP IT OPEN!**
6. **Wait for:** `INFO:     Uvicorn running on http://0.0.0.0:8000`
7. **Go to browser** → Press **F5** to refresh

---

## ✅ Alternative: PowerShell Commands

**Open PowerShell and run these commands:**

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py
```

**Wait for:** `INFO:     Uvicorn running on http://0.0.0.0:8000`

**KEEP THIS WINDOW OPEN!**

---

## ✅ Verify Backend Is Running

**Open in browser:** http://localhost:8000/api/health

**Should show:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "empire-automation-api"
}
```

---

## ✅ After Backend Starts

1. **Wait 3-5 seconds** for full startup
2. **Go to frontend:** http://localhost:3000
3. **Press Ctrl+Shift+R** (hard refresh)
4. **Check status bar** - Should turn **GREEN**: "✅ API Connected"
5. **All errors disappear!**

---

## ⚠️ Important

- **Keep backend window OPEN** - Closing it stops the server
- **Backend runs continuously** - It's a server, not a one-time script
- **Use separate terminal for frontend** - Don't close backend window

---

## 🔧 Troubleshooting

### Backend Won't Start

**Check the window for errors:**
- **"ModuleNotFoundError"** → Run: `pip install -r requirements.txt`
- **"Port 8000 in use"** → Kill process: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`
- **"Database not found"** → Run: `python -m empire_automation.database.init_db`

### Backend Starts But Frontend Still Shows Errors

1. **Wait 5 seconds** after backend starts
2. **Hard refresh:** Ctrl+Shift+R
3. **Check:** http://localhost:8000/api/health in browser
4. **Check browser console** (F12) for CORS errors

---

## 📋 Quick Checklist

- [ ] Backend window is open and shows "Uvicorn running"
- [ ] http://localhost:8000/api/health returns JSON
- [ ] Frontend refreshed (Ctrl+Shift+R)
- [ ] Status bar shows "✅ API Connected" (green)
- [ ] No more "Failed to fetch" errors

---

**Double-click `START_BACKEND.bat` to start the backend!** 🚀


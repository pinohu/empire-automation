# 🚀 Start Backend - Easiest Method

## ✅ Method 1: Double-Click (Easiest!)

1. **Navigate to:** `empire-automation` folder
2. **Double-click:** `START_BACKEND.bat`
3. **Wait for:** "Uvicorn running on http://0.0.0.0:8000"
4. **Keep window open!**

---

## ✅ Method 2: PowerShell Script

1. **Right-click** `start_backend.ps1`
2. **Select:** "Run with PowerShell"
3. **Wait for:** "Uvicorn running on http://0.0.0.0:8000"
4. **Keep window open!**

---

## ✅ Method 3: Manual Commands

**Open PowerShell and run:**

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py
```

---

## ✅ Verify It's Working

**Open in browser:** http://localhost:8000/api/health

Should show:
```json
{"status": "healthy", "timestamp": "...", "service": "empire-automation-api"}
```

---

## ✅ After Backend Starts

1. **Go to frontend:** http://localhost:3000
2. **Press Ctrl+Shift+R** (hard refresh)
3. **Check status bar** - Should turn GREEN: "✅ API Connected"
4. **All errors disappear!**

---

## ⚠️ Important Notes

- **Keep the backend window open** - Closing it stops the server
- **Backend must run continuously** - It's a server, not a one-time script
- **Use separate terminal for frontend** - Don't close backend window

---

## 🔧 Troubleshooting

### "Virtual environment not found"
```powershell
cd empire-automation
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Port 8000 already in use"
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Backend starts but frontend still shows errors
1. Wait 5 seconds after backend starts
2. Hard refresh frontend (Ctrl+Shift+R)
3. Check http://localhost:8000/api/health in browser

---

**Double-click `START_BACKEND.bat` to start the backend!** 🚀

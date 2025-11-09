# 🚀 START BACKEND NOW - Simple Instructions

## ✅ Everything is Fixed!

The backend code is ready. You just need to start it manually.

---

## 📋 Step-by-Step Instructions

### 1. Open PowerShell

Press `Win + X` → Select "Windows PowerShell" or "Terminal"

### 2. Copy and Paste These Commands (One at a Time)

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
```

```powershell
.\venv\Scripts\Activate.ps1
```

```powershell
python start_api.py
```

### 3. Wait for This Message

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this window open!** Don't close it.

---

## ✅ Verify It's Working

### Test in Browser

Open: **http://localhost:8000/api/health**

Should show:
```json
{"status": "healthy", "timestamp": "...", "service": "empire-automation-api"}
```

---

## 🎯 After Backend Starts

1. **Go to frontend**: http://localhost:3000
2. **Press F5** to refresh
3. **Status bar should turn GREEN**: "✅ API Connected"
4. **Data appears** on all pages!

---

## ⚠️ Expected Warnings (Safe to Ignore)

You may see these - they're **normal**:
- `AgenticFlow not available` - Optional integration
- `Google Workspace features will be disabled` - Optional integration

These won't prevent the backend from running.

---

## 🔧 If It Still Doesn't Work

**Check the terminal window** for error messages and share them.

**Common fixes:**
- Port 8000 in use: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`
- Database error: `python -m empire_automation.database.init_db`

---

**Start the backend in PowerShell, then refresh your frontend!** 🚀


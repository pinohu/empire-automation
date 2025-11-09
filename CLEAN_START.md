# 🔄 Clean Start - Backend Issues

## Problem Found

Port 8000 has multiple processes listening, but the backend isn't responding properly. This suggests stuck/crashed processes.

---

## ✅ Solution: Clean Start

### Step 1: Kill All Processes on Port 8000

Run this in PowerShell:

```powershell
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
```

**OR manually:**

```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

(Repeat for each PID shown)

### Step 2: Start Backend Fresh

**Open a NEW PowerShell window** and run:

```powershell
cd C:\Users\polyc\Documents\Empire\empire-automation
.\venv\Scripts\Activate.ps1
python start_api.py
```

### Step 3: Verify It's Working

Wait 5 seconds, then test:

**Open in browser:** http://localhost:8000/api/health

Should return:
```json
{"status": "healthy", "timestamp": "...", "service": "empire-automation-api"}
```

---

## ✅ After Backend Starts

1. **Go to frontend**: http://localhost:3000
2. **Refresh page** (F5)
3. **Status bar should turn GREEN**: "✅ API Connected"
4. **Data appears** on pages

---

## 🔧 If Still Not Working

**Check the terminal window** where you started the backend for error messages.

**Common issues:**
- Import errors → `pip install -r requirements.txt`
- Database errors → `python -m empire_automation.database.init_db`
- Port still in use → Repeat Step 1

---

**Kill the old processes, start fresh, then refresh your frontend!** 🚀


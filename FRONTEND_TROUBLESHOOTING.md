# 🔧 Frontend Troubleshooting Guide

## Issue: Pages Show But No Data Displays

### ✅ Fixed Issues

1. **API Route Path** - Fixed daily briefing route from `/api/daily-briefing` to `/daily-briefing`
2. **Error Handling** - Added console logging and error messages
3. **Data Validation** - Added array checks for API responses

---

## 🔍 Debugging Steps

### 1. Check Browser Console

Open browser DevTools (F12) and check the Console tab. You should see:

```
[API] Fetching: http://localhost:8000/api/v1/daily-briefing
[API] Response status: 200 for http://localhost:8000/api/v1/daily-briefing
[API] Success: {data...}
```

**If you see errors:**
- `Failed to fetch` - Backend not running or CORS issue
- `404 Not Found` - Wrong API endpoint
- `500 Internal Server Error` - Backend error (check backend logs)

### 2. Verify Backend is Running

```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Should return: {"status":"healthy"}
```

### 3. Check API Endpoints Directly

Test endpoints in browser or Postman:

- http://localhost:8000/api/v1/daily-briefing
- http://localhost:8000/api/v1/financial/dashboard
- http://localhost:8000/api/v1/90-day-plan/progress
- http://localhost:8000/api/v1/clients
- http://localhost:8000/api/v1/leads

### 4. Initialize Database

If endpoints return empty arrays, the database might not be initialized:

```bash
cd empire-automation
python -m empire_automation.database.init_db
```

### 5. Check CORS Configuration

Ensure backend CORS includes frontend URL:

```python
# In empire_automation/api/main.py
CORS_ORIGINS=http://localhost:8501,http://localhost:3000,http://127.0.0.1:8501
```

### 6. Check Environment Variables

Frontend `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend `.env`:
```env
DATABASE_URL=sqlite:///./empire.db
PLAN_START_DATE=2024-01-01
```

---

## 🐛 Common Issues

### Issue: "Failed to fetch" Error

**Cause:** Backend not running or CORS blocked

**Solution:**
1. Start backend: `uvicorn empire_automation.api.main:app --reload`
2. Check CORS settings in backend
3. Verify backend is on port 8000

### Issue: Empty Arrays Returned

**Cause:** Database not initialized or no seed data

**Solution:**
```bash
# Initialize database
python -m empire_automation.database.init_db

# Check if data exists
python -c "from empire_automation.database import SessionLocal; from empire_automation.database.models import Task; db = SessionLocal(); print(db.query(Task).count())"
```

### Issue: 404 Errors

**Cause:** Wrong API endpoint path

**Solution:**
- Check route definitions in `empire_automation/api/routes/`
- Ensure routes don't include `/api/v1` prefix (it's added in main.py)
- Verify frontend is calling correct paths

### Issue: CORS Errors

**Cause:** Backend not allowing frontend origin

**Solution:**
1. Check `CORS_ORIGINS` in backend `.env`
2. Ensure `http://localhost:3000` is included
3. Restart backend after changing CORS settings

---

## 📊 Expected API Responses

### Daily Briefing
```json
{
  "date": "2024-01-01",
  "day_number": 1,
  "total_tasks": 5,
  "pending_tasks": 3,
  "completed_tasks": 2,
  "priority_tasks": [...],
  "metrics": {
    "revenue_ytd": 0,
    "active_projects": 0,
    "active_leads": 0
  }
}
```

### Financial Dashboard
```json
{
  "period_start": "2024-01-01",
  "period_end": "2024-01-31",
  "total_revenue": 0,
  "total_expenses": 0,
  "net_profit": 0,
  "transaction_count": 0,
  "revenue_by_entity": {},
  "expense_by_category": {}
}
```

---

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database initialized
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] Browser console shows API calls
- [ ] API endpoints return data (test in browser)

---

## 🚀 Quick Fix Commands

```bash
# 1. Start Backend
cd empire-automation
uvicorn empire_automation.api.main:app --reload

# 2. Initialize Database (if needed)
python -m empire_automation.database.init_db

# 3. Start Frontend (new terminal)
cd empire-automation/frontend
npm run dev

# 4. Test API
curl http://localhost:8000/api/v1/daily-briefing
```

---

**After fixing, refresh the browser and check console for successful API calls!**


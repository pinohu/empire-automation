# ✅ Deployment Checklist

## Pre-Deployment ✅

- [x] Code pushed to GitHub
- [x] render.yaml created
- [x] start_api.py updated for production
- [x] requirements.txt ready
- [x] .gitignore excludes credentials
- [x] Vercel CLI installed

## Render Backend Deployment

### Step 1: Sign Up
- [ ] Go to https://render.com
- [ ] Sign up (FREE, use GitHub)
- [ ] Authorize Render to access repositories

### Step 2: Create PostgreSQL Database
- [ ] Click "New +" → "PostgreSQL"
- [ ] Name: `empire-automation-db`
- [ ] Database: `empire`
- [ ] Region: Same as web service
- [ ] Click "Create Database"
- [ ] Copy Internal Database URL

### Step 3: Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub → Select `pinohu/empire-automation`
- [ ] Configure:
  - Name: `empire-automation-api`
  - Region: `Oregon (US West)` or closest
  - Branch: `master`
  - Root Directory: (empty)
  - Runtime: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python start_api.py`
- [ ] Advanced Settings:
  - Health Check Path: `/api/health`
  - Auto-Deploy: `Yes`

### Step 4: Add Environment Variables
- [ ] Go to Web Service → Environment tab
- [ ] Add all variables from `RENDER_ENV_VARS.md`
- [ ] Link PostgreSQL service (for DATABASE_URL)
- [ ] Save Changes

### Step 5: Deploy
- [ ] Click "Create Web Service"
- [ ] Watch build logs
- [ ] Wait for "Your service is live"
- [ ] Copy backend URL (e.g., `https://empire-automation-api.onrender.com`)

### Step 6: Test Backend
- [ ] Visit: `https://your-app.onrender.com/api/health`
- [ ] Should return: `{"status": "healthy", ...}`
- [ ] Visit: `https://your-app.onrender.com/docs`
- [ ] Should show Swagger UI

## Vercel Frontend Connection

### Step 7: Connect Frontend
- [ ] Run: `cd empire-automation\frontend`
- [ ] Run: `.\connect-backend.ps1`
- [ ] Enter Render backend URL when prompted
- [ ] Or manually update via Vercel CLI:
  ```powershell
  vercel env rm NEXT_PUBLIC_API_URL production
  vercel env add NEXT_PUBLIC_API_URL
  # Enter Render URL
  vercel --prod
  ```

### Step 8: Verify Connection
- [ ] Visit: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app
- [ ] Open DevTools → Network tab
- [ ] Check API calls go to Render backend
- [ ] Verify responses are successful

## ✅ Deployment Complete!

- [ ] Backend deployed on Render
- [ ] Frontend connected to backend
- [ ] All features working

---

**Need help?** See `DEPLOY_ALL_NOW.md` for detailed instructions.


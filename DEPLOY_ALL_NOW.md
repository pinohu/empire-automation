# 🚀 Deploy Everything - Render + Vercel

## 🎯 Complete Deployment Guide

This guide will deploy:
- ✅ **Backend** → Render (FREE)
- ✅ **Frontend** → Vercel (already deployed, needs connection)

---

## Part 1: Deploy Backend to Render

### Step 1: Sign Up on Render

1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (easiest - connects to your repo automatically)
4. Authorize Render to access your repositories

### Step 2: Create Web Service

1. In Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Connect GitHub"**
4. **Select repository**: `pinohu/empire-automation`
5. Click **"Connect"**

### Step 3: Configure Service

Fill in:

**Basic Settings:**
- **Name**: `empire-automation-api`
- **Region**: `Oregon (US West)` (or closest to you)
- **Branch**: `master`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python start_api.py`

**Advanced Settings** (click "Advanced"):
- **Health Check Path**: `/api/health`
- **Auto-Deploy**: `Yes`

### Step 4: Add PostgreSQL Database

1. In Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   ```
   Name: empire-automation-db
   Database: empire
   Region: Same as web service
   ```
4. Click **"Create Database"**
5. Wait for database to be created
6. Go to database → **"Info"** tab
7. **Copy the "Internal Database URL"** (starts with `postgresql://`)

### Step 5: Add Environment Variables

Go back to your Web Service → **"Environment"** tab → Add:

**Required:**
```
DATABASE_URL=<paste-internal-database-url-from-step-4>
CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
PLAN_START_DATE=2024-01-01
ENVIRONMENT=production
```

**API Keys** (copy from your local `.env` file):
```
AGENTICFLOW_API_KEY=<your-key>
SUITEDASH_API_KEY=<your-key>
SUITEDASH_API_AUTH_CREDENTIAL=<your-credential>
EMAILIT_API_KEY=<your-key>
BRILLIANT_DIRECTORIES_API_KEY=<your-key>
FORMALOO_API_KEY=<your-key>
FORMALOO_API_SECRET=<your-secret>
ANTHROPIC_API_KEY=<your-key>
```

**Other:**
```
GOOGLE_CREDENTIALS_FILE=credentials/google-service-account.json
GOOGLE_SHEETS_ID=<your-id>
REDIS_URL=redis://localhost:6379/0
NOTIFICATION_CHANNEL=log
LOG_LEVEL=INFO
```

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Watch the build logs
3. Wait for **"Your service is live"** message
4. **Copy your service URL** (e.g., `https://empire-automation-api.onrender.com`)

### Step 7: Test Backend

Open in browser:
- **Health**: `https://your-app.onrender.com/api/health`
- **Docs**: `https://your-app.onrender.com/docs`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "service": "empire-automation-api"
}
```

---

## Part 2: Connect Frontend to Backend (Vercel)

### Step 1: Get Your Backend URL

From Render deployment, copy your backend URL (e.g., `https://empire-automation-api.onrender.com`)

### Step 2: Update Vercel Environment Variable

**Option A: Via Vercel CLI**
```powershell
cd empire-automation/frontend
vercel env rm NEXT_PUBLIC_API_URL production
vercel env rm NEXT_PUBLIC_API_URL preview
vercel env rm NEXT_PUBLIC_API_URL development
vercel env add NEXT_PUBLIC_API_URL
# Enter your Render backend URL when prompted
# Select: production, preview, development
vercel --prod
```

**Option B: Via Vercel Dashboard**
1. Go to: https://vercel.com/polycarpohu-gmailcoms-projects/frontend/settings/environment-variables
2. Edit `NEXT_PUBLIC_API_URL`
3. Update value to your Render backend URL
4. Save → Redeploy from dashboard

### Step 3: Verify Connection

1. Visit: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app
2. Open browser DevTools → Network tab
3. Check API calls are going to your Render backend
4. Verify responses are successful

---

## ✅ Done!

Your full-stack application is now deployed:
- **Backend**: Render (FREE)
- **Frontend**: Vercel
- **Connected**: Frontend → Backend

---

## 🐛 Troubleshooting

**Backend not starting:**
- Check Render build logs
- Verify all environment variables are set
- Ensure PostgreSQL database is connected

**Frontend can't connect:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend CORS settings include Vercel domain
- Test backend URL directly in browser

**Database errors:**
- Ensure `DATABASE_URL` is set correctly
- Verify PostgreSQL is running
- Check database migrations

---

**Need help?** Check individual guides:
- `RENDER_DEPLOY_STEPS.md` - Detailed Render guide
- `DEPLOY_TO_VERCEL.md` - Vercel deployment guide


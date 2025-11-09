# 🚀 Deploy to Render - Step by Step Guide

## ✅ Prerequisites

- ✅ Code pushed to GitHub
- ✅ Render account (free signup)
- ✅ Environment variables ready

---

## 📋 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
cd empire-automation
git add .
git commit -m "Ready for Render deployment"
git push
```

**If you haven't pushed yet:**
```bash
git remote add origin <your-github-repo-url>
git push -u origin main
```

---

### Step 2: Sign Up on Render

1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with GitHub (easiest) or email
4. Verify your email if needed

---

### Step 3: Create Web Service

1. In Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Connect GitHub"** (or GitLab/Bitbucket)
4. Authorize Render to access your repositories
5. **Select your repository** from the list
6. Click **"Connect"**

---

### Step 4: Configure Service

Fill in the form:

**Basic Settings:**
- **Name**: `empire-automation-api` (or your choice)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (or `.` if needed)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python start_api.py`

**Advanced Settings** (click "Advanced"):
- **Auto-Deploy**: `Yes` (deploys on every push)
- **Health Check Path**: `/api/health`

---

### Step 5: Add Environment Variables

Click **"Add Environment Variable"** and add these:

**Required:**
```
CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
PLAN_START_DATE=2024-01-01
ENVIRONMENT=production
```

**Database (Render provides PostgreSQL automatically):**
- Render will create a PostgreSQL database
- The `DATABASE_URL` will be automatically set
- You don't need to add it manually

**API Keys** (copy from your `.env` file):
```
AGENTICFLOW_API_KEY=your-key-here
SUITEDASH_API_KEY=your-key-here
SUITEDASH_API_AUTH_CREDENTIAL=your-credential-here
EMAILIT_API_KEY=your-key-here
BRILLIANT_DIRECTORIES_API_KEY=your-key-here
FORMALOO_API_KEY=your-key-here
FORMALOO_API_SECRET=your-secret-here
ANTHROPIC_API_KEY=your-key-here
```

**Other Settings:**
```
GOOGLE_CREDENTIALS_FILE=credentials/google-service-account.json
GOOGLE_SHEETS_ID=your-spreadsheet-id
REDIS_URL=redis://localhost:6379/0
NOTIFICATION_CHANNEL=log
LOG_LEVEL=INFO
```

---

### Step 6: Add PostgreSQL Database (Free)

1. In Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. **Name**: `empire-automation-db`
4. **Database**: `empire`
5. **User**: `empire_user` (or auto-generated)
6. **Region**: Same as your web service
7. Click **"Create Database"**
8. **Copy the Internal Database URL** (starts with `postgresql://`)
9. Go back to your Web Service → Environment Variables
10. Add: `DATABASE_URL` = the PostgreSQL URL you copied

---

### Step 7: Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying
3. Watch the build logs
4. Wait for **"Your service is live"** message
5. **Copy your service URL** (e.g., `https://empire-automation-api.onrender.com`)

---

### Step 8: Test Backend

Open in browser:
- **Health Check**: `https://your-app.onrender.com/api/health`
- **API Docs**: `https://your-app.onrender.com/docs`

Should return:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "service": "empire-automation-api"
}
```

---

### Step 9: Connect Frontend

```powershell
cd empire-automation/frontend
.\connect-backend.ps1
```

When prompted, enter your Render URL:
```
https://your-app.onrender.com
```

The script will:
- Update environment variables
- Redeploy frontend
- Complete the connection

---

## ✅ Done!

Visit your Vercel frontend:
**https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app**

It should now connect to your Render backend!

---

## ⚠️ Free Tier Notes

- **Spins down** after 15 minutes of inactivity
- **Wakes up** on first request (~30 second delay)
- **750 hours/month** (enough for 24/7 if kept active)

**To keep it awake**: Use a free uptime monitor like UptimeRobot to ping your API every 10 minutes.

---

## 🐛 Troubleshooting

**Build fails:**
- Check build logs in Render dashboard
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

**Database errors:**
- Ensure PostgreSQL is created and connected
- Check `DATABASE_URL` is set correctly
- Verify database migrations run on startup

**CORS errors:**
- Verify `CORS_ORIGINS` includes your Vercel URL
- Check backend logs for CORS errors

---

**Need help?** Check Render logs in the dashboard or see `DEPLOY_TO_RENDER.md` for more details.


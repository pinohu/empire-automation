# 🚀 Deploy to Render - RIGHT NOW!

## ⚡ Quick Deployment Steps

### Step 1: Push to GitHub

**If you have a GitHub repo:**
```bash
cd empire-automation
git push
```

**If you DON'T have a GitHub repo yet:**
1. Go to: https://github.com/new
2. Create a new repository (e.g., `empire-automation`)
3. Don't initialize with README
4. Copy the repository URL
5. Run:
```bash
cd empire-automation
git remote add origin <your-github-repo-url>
git push -u origin main
```

---

### Step 2: Deploy on Render

1. **Open**: https://render.com
2. **Sign up** (FREE, use GitHub for easiest setup)
3. **Click**: "New +" → "Web Service"
4. **Connect GitHub** → Authorize → Select your repo
5. **Configure**:
   ```
   Name: empire-automation-api
   Region: Oregon (US West) or closest to you
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python start_api.py
   ```
6. **Click "Advanced"** → Set:
   - Health Check Path: `/api/health`
   - Auto-Deploy: Yes

---

### Step 3: Add PostgreSQL Database

1. In Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   ```
   Name: empire-automation-db
   Database: empire
   Region: Same as web service
   ```
4. Click **"Create Database"**
5. **Copy the Internal Database URL** (postgresql://...)
6. Go back to your Web Service → Environment Variables
7. Add: `DATABASE_URL` = the PostgreSQL URL you copied

---

### Step 4: Add Environment Variables

In your Web Service → Environment Variables, add:

**Required:**
```
CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
PLAN_START_DATE=2024-01-01
ENVIRONMENT=production
```

**API Keys** (copy from your `.env` file):
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

---

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Watch the build logs
3. Wait for **"Your service is live"**
4. **Copy your service URL** (e.g., `https://empire-automation-api.onrender.com`)

---

### Step 6: Test Backend

Open in browser:
- Health: `https://your-app.onrender.com/api/health`
- Docs: `https://your-app.onrender.com/docs`

---

### Step 7: Connect Frontend

```powershell
cd empire-automation/frontend
.\connect-backend.ps1
```

Enter your Render URL when prompted.

---

## ✅ Done!

Your backend is now deployed and connected to your frontend!

---

**Need help?** Check `RENDER_DEPLOY_STEPS.md` for detailed instructions.


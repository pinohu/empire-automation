# 🚀 Deploy Backend to Render (100% Free)

## Why Render?

- ✅ **Completely FREE** - 750 hours/month (enough for 24/7)
- ✅ **Free PostgreSQL** database included
- ✅ **Automatic HTTPS**
- ✅ **Auto-deploy** from GitHub
- ✅ **No credit card** required for free tier

---

## 🎯 Quick Deploy Steps

### Step 1: Push to GitHub

```bash
cd empire-automation
git add .
git commit -m "Ready for Render deployment"
git push
```

### Step 2: Deploy on Render

1. **Go to**: https://render.com
2. **Sign up** (free, no credit card needed)
3. **New** → **Web Service**
4. **Connect GitHub** → Select your repository
5. **Configure**:
   - **Name**: `empire-automation-api`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `.` if needed)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_api.py`
6. **Add Environment Variables**:
   - Click "Advanced" → "Add Environment Variable"
   - Add from your `.env` file:
     - `DATABASE_URL` - Render provides PostgreSQL automatically
     - `CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app`
     - `PLAN_START_DATE=2024-01-01`
     - `ENVIRONMENT=production`
     - All your API keys (copy from `.env`)
7. **Create Web Service** → Wait for deployment

### Step 3: Get Your Backend URL

After deployment:
- Render Dashboard → Your Service → Settings
- Copy the URL (e.g., `https://empire-automation-api.onrender.com`)

### Step 4: Connect Frontend

```powershell
cd empire-automation/frontend
.\connect-backend.ps1
# Enter your Render URL when prompted
```

---

## ⚠️ Free Tier Limitations

- **Spins down** after 15 minutes of inactivity
- **Wakes up** on first request (~30 second delay)
- **750 hours/month** (enough for 24/7 if you keep it active)

**Solution**: Use a free uptime monitor (like UptimeRobot) to ping your API every 10 minutes to keep it awake.

---

## ✅ After Deployment

1. **Test Backend**: Visit `https://your-app.onrender.com/api/health`
2. **Connect Frontend**: Run `connect-backend.ps1`
3. **Verify**: Check your Vercel dashboard

---

**Render is completely free and perfect for this project!** 🎉


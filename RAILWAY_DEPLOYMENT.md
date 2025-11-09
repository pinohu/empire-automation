# 🚂 Deploy Backend to Railway - Complete Guide

## Quick Deploy

### Option 1: Deploy via Railway Dashboard

1. **Go to Railway**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select** your `empire-automation` repository
5. **Railway auto-detects** Python and FastAPI
6. **Add Environment Variables** (see below)
7. **Deploy** - Railway handles the rest!

### Option 2: Use Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
cd empire-automation
railway init

# Deploy
railway up
```

---

## 🔧 Required Environment Variables

Add these in Railway Dashboard → Variables:

```
PLAN_START_DATE=2024-01-01
DATABASE_URL=sqlite:///./empire.db
CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Optional** (if using these services):
```
GOOGLE_CREDENTIALS_FILE=credentials/google-service-account.json
AGENTICFLOW_API_KEY=your-key
SUITEDASH_API_KEY=your-key
EMAILIT_API_KEY=your-key
BRILLIANT_DIRECTORIES_API_KEY=your-key
FORMALOO_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
```

---

## 📝 After Deployment

1. **Get Your Backend URL**:
   - Railway Dashboard → Your Service → Settings → Networking
   - Generate domain or use provided URL
   - Example: `https://your-app.railway.app`

2. **Update Vercel Environment Variable**:
   ```bash
   cd empire-automation/frontend
   vercel env rm NEXT_PUBLIC_API_URL production
   echo "https://your-app.railway.app" | vercel env add NEXT_PUBLIC_API_URL production
   vercel --prod
   ```

3. **Test**:
   - Backend: `https://your-app.railway.app/api/health`
   - Frontend: Your Vercel URL should now connect!

---

## ✅ Files Created for Railway

- `railway.json` - Railway configuration
- `Procfile` - Process file for Railway
- `runtime.txt` - Python version specification

---

**Railway free tier includes $5/month credit - perfect for this project!** 🎉


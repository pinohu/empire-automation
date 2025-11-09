# 🚂 Deploy Backend to Railway - Right Now!

## Quick Deploy Steps

### Step 1: Push to GitHub (if not already)

```bash
cd empire-automation
git add .
git commit -m "Ready for Railway deployment"
git push
```

### Step 2: Deploy on Railway

1. **Go to**: https://railway.app
2. **Sign up/Login** (free tier available)
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Railway auto-detects** Python/FastAPI
6. **Add Environment Variables**:
   - Go to Variables tab
   - Add from your `.env` file:
     - `DATABASE_URL` (Railway provides PostgreSQL automatically)
     - `CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app`
     - `PLAN_START_DATE=2024-01-01`
     - All your API keys (copy from `.env`)
7. **Deploy** → Wait for "Deploy Successful"
8. **Get URL**: Settings → Networking → Copy public URL

### Step 3: Connect Frontend

```bash
cd empire-automation/frontend
vercel env rm NEXT_PUBLIC_API_URL production
vercel env rm NEXT_PUBLIC_API_URL preview
vercel env rm NEXT_PUBLIC_API_URL development
vercel env add NEXT_PUBLIC_API_URL
# Enter your Railway URL (e.g., https://your-app.railway.app)
# Select: production, preview, development
vercel --prod
```

### Step 4: Done! 🎉

Visit: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app

---

## ⚡ Even Faster: Use Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd empire-automation
railway init
railway up
```

---

**Railway is free for small projects!** 🎉


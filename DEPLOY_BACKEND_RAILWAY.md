# 🚂 Deploy Backend to Railway - Quick Guide

## Why Deploy Backend?

Your Vercel frontend is deployed, but it can't reach `localhost:8000`. You need to deploy your FastAPI backend to make it accessible.

## 🚀 Railway Deployment (Easiest)

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"

### Step 2: Deploy from GitHub
1. **Connect Repository**:
   - Click "Deploy from GitHub repo"
   - Select your `empire-automation` repository
   - Railway will detect it's a Python project

2. **Configure Settings**:
   - **Root Directory**: Leave as root (or set to `empire-automation` if repo is nested)
   - **Start Command**: `python start_api.py`
   - **Python Version**: 3.11+ (auto-detected)

3. **Set Environment Variables**:
   - Click "Variables" tab
   - Add all variables from your `.env` file:
     ```
     PLAN_START_DATE=2024-01-01
     DATABASE_URL=sqlite:///./empire.db
     CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
     ENVIRONMENT=production
     LOG_LEVEL=INFO
     ```
   - Add any API keys you're using

4. **Deploy**:
   - Railway will automatically build and deploy
   - Wait for "Deploy Successful"

### Step 3: Get Your Backend URL
1. Click on your service
2. Go to "Settings" → "Networking"
3. Click "Generate Domain"
4. Copy the URL (e.g., `https://your-app.railway.app`)

### Step 4: Update Vercel
```bash
cd empire-automation/frontend

# Remove old env var
vercel env rm NEXT_PUBLIC_API_URL production

# Add new backend URL
echo "https://your-app.railway.app" | vercel env add NEXT_PUBLIC_API_URL production
echo "https://your-app.railway.app" | vercel env add NEXT_PUBLIC_API_URL preview

# Redeploy
vercel --prod
```

### Step 5: Update Backend CORS (if needed)
In Railway, add to environment variables:
```
CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
```

---

## 🔧 Alternative: Use ngrok (For Testing)

If you want to test quickly without deploying:

```bash
# Install ngrok
# Download from: https://ngrok.com/download

# Start your backend
cd empire-automation
python start_api.py

# In another terminal, start ngrok
ngrok http 8000

# Copy the HTTPS URL (e.g., https://xxxx.ngrok.io)
# Update Vercel:
cd frontend
echo "https://xxxx.ngrok.io" | vercel env rm NEXT_PUBLIC_API_URL production
echo "https://xxxx.ngrok.io" | vercel env add NEXT_PUBLIC_API_URL production
vercel --prod
```

---

## ✅ After Deployment

1. **Test Backend**: Visit `https://your-backend.railway.app/api/health`
2. **Update Vercel**: Set `NEXT_PUBLIC_API_URL` to your Railway URL
3. **Test Frontend**: Visit your Vercel URL - should connect!

---

**Railway is free for small projects!** 🎉


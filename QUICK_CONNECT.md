# ⚡ Quick Connect - Frontend to Backend

## Current Status

✅ Frontend deployed: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app
✅ Environment variable `NEXT_PUBLIC_API_URL` is set (but needs your backend URL)
✅ Backend CORS configured for Vercel domains

---

## 🎯 Fastest Way to Connect

### Step 1: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** (free)
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Railway auto-detects** Python/FastAPI
6. **Add Environment Variables**:
   - Copy from your `.env` file
   - Important: `CORS_ORIGINS` should include Vercel URLs
7. **Deploy** → Wait for "Deploy Successful"
8. **Get URL**: Railway Dashboard → Settings → Networking → Copy public URL

### Step 2: Update Frontend Environment Variable

**Via CLI**:
```bash
cd empire-automation/frontend
vercel env rm NEXT_PUBLIC_API_URL production
vercel env rm NEXT_PUBLIC_API_URL preview  
vercel env rm NEXT_PUBLIC_API_URL development
vercel env add NEXT_PUBLIC_API_URL
# Enter your Railway URL when prompted
# Select: production, preview, development
vercel --prod
```

**Via Dashboard**:
1. Go to: https://vercel.com/polycarpohu-gmailcoms-projects/frontend/settings/environment-variables
2. Edit `NEXT_PUBLIC_API_URL`
3. Update value to your Railway URL
4. Save → Redeploy

### Step 3: Verify Connection

1. Visit: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app
2. Open DevTools → Network tab
3. Check API calls are going to your Railway URL
4. Verify responses are successful

---

## ✅ Done!

Your frontend is now connected to your backend! 🎉

---

**Need help?** See `DEPLOY_BACKEND_AND_CONNECT.md` for detailed instructions.


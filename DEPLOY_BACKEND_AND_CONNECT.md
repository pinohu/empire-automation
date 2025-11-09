# 🚀 Deploy Backend & Connect to Frontend

## Current Status

✅ Frontend deployed to Vercel
🔗 Backend needs deployment
⚙️ Connection needs configuration

---

## 🎯 Quick Solution: Deploy Backend to Railway

### Step 1: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** (free tier available)
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Railway auto-detects** Python/FastAPI
6. **Add Environment Variables**:
   - Copy from your `.env` file
   - Important ones:
     - `DATABASE_URL` (Railway provides PostgreSQL)
     - `CORS_ORIGINS` (add your Vercel URLs)
     - `PLAN_START_DATE=2024-01-01`
     - All your API keys
7. **Deploy** → Railway handles the rest!

### Step 2: Get Your Backend URL

After deployment:
- Railway Dashboard → Your Service → Settings → Networking
- Copy the public URL (e.g., `https://your-app.railway.app`)

### Step 3: Connect Frontend to Backend

**Option A: Via Vercel CLI**
```bash
cd empire-automation/frontend
vercel env add NEXT_PUBLIC_API_URL
# Enter your Railway URL when prompted
# Select: production, preview, development
vercel --prod  # Redeploy
```

**Option B: Via Vercel Dashboard**
1. Go to: https://vercel.com/polycarpohu-gmailcoms-projects/frontend/settings/environment-variables
2. Add: `NEXT_PUBLIC_API_URL` = your Railway URL
3. Redeploy from dashboard

### Step 4: Update Backend CORS

In Railway Dashboard → Environment Variables, add/update:

```
CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
```

---

## 🔄 Alternative: Use ngrok for Local Backend (Testing)

If you want to test with local backend:

1. **Install ngrok**: https://ngrok.com/download
2. **Start your local backend**:
   ```bash
   cd empire-automation
   python start_api.py
   ```
3. **In another terminal, start ngrok**:
   ```bash
   ngrok http 8000
   ```
4. **Copy ngrok URL** (e.g., `https://abc123.ngrok.io`)
5. **Set in Vercel**:
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   # Enter ngrok URL
   vercel --prod
   ```

---

## ✅ Verify Connection

1. Visit: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app
2. Open browser DevTools → Network tab
3. Check API calls to your backend
4. Verify responses are successful

---

## 📝 Files Created

- `Procfile` - For Railway deployment
- `railway.json` - Railway configuration
- Backend CORS updated to include Vercel domains

---

**Ready to deploy backend?** Follow Step 1 above! 🚀


# 🔗 Connect Frontend to Backend

## Current Status

✅ Frontend deployed to Vercel
🔗 Backend connection needed

## Option 1: Connect to Local Backend (Development)

If your backend is running locally:

### Set Environment Variable in Vercel

1. Go to: https://vercel.com/polycarpohu-gmailcoms-projects/frontend/settings/environment-variables
2. Add:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `http://localhost:8000` (or use a tunnel like ngrok)
   - Environments: Development only

**Note**: Localhost won't work from Vercel. Use ngrok or deploy backend.

### Use ngrok for Local Backend

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000

# Use the ngrok URL (e.g., https://abc123.ngrok.io) as NEXT_PUBLIC_API_URL
```

## Option 2: Deploy Backend (Recommended)

### Deploy to Railway (Easiest)

1. **Sign up**: https://railway.app
2. **New Project** → Deploy from GitHub
3. **Select your repo** → Set root directory to project root
4. **Add environment variables** from your `.env`
5. **Deploy** → Get your Railway URL (e.g., `https://your-app.railway.app`)

### Deploy to Render

1. **Sign up**: https://render.com
2. **New** → Web Service
3. **Connect GitHub** → Select repo
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python start_api.py`
5. **Add environment variables**
6. **Deploy** → Get your Render URL

### After Backend Deployment

1. **Set Frontend Environment Variable**:
   - Go to Vercel → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = your backend URL
   - Redeploy

2. **Update Backend CORS**:
   ```
   CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
   ```

3. **Test Connection**:
   - Visit your Vercel URL
   - Check browser console
   - Verify API calls work

## Quick Connect Script

Run this to set the environment variable via CLI:

```bash
cd empire-automation/frontend
vercel env add NEXT_PUBLIC_API_URL
# Enter your backend URL when prompted
# Select environments: production, preview, development
vercel --prod  # Redeploy
```

## Verify Connection

1. Visit: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app
2. Open browser DevTools → Network tab
3. Check API calls to your backend URL
4. Verify responses are successful

---

**Need help deploying backend?** See deployment guides for Railway/Render.


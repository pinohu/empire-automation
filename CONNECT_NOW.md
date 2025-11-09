# 🔗 Connect Frontend to Backend - Quick Guide

## Current Status

✅ Frontend deployed to Vercel
✅ Backend CORS updated (includes Vercel domains)
🔗 Need to set `NEXT_PUBLIC_API_URL` environment variable

---

## 🚀 Quick Connect (Choose One)

### Option 1: Deploy Backend to Railway (Best for Production)

1. **Deploy Backend**:
   - Go to: https://railway.app
   - New Project → Deploy from GitHub
   - Select your repo
   - Railway auto-detects Python/FastAPI
   - Add environment variables from your `.env`
   - Deploy → Get your Railway URL

2. **Connect Frontend**:
   ```bash
   cd empire-automation/frontend
   vercel env add NEXT_PUBLIC_API_URL
   # Enter your Railway URL (e.g., https://your-app.railway.app)
   # Select: production, preview, development
   vercel --prod
   ```

### Option 2: Use ngrok for Local Backend (Quick Testing)

1. **Install ngrok**: https://ngrok.com/download

2. **Start your backend**:
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
   cd empire-automation/frontend
   vercel env add NEXT_PUBLIC_API_URL
   # Enter ngrok URL
   # Select: production, preview, development
   vercel --prod
   ```

---

## ✅ After Setting Environment Variable

1. **Redeploy**: `vercel --prod` or trigger from dashboard
2. **Test**: Visit your Vercel URL
3. **Verify**: Check browser console for API calls

---

## 📝 Files Ready

- ✅ `Procfile` - For Railway deployment
- ✅ `railway.json` - Railway configuration
- ✅ Backend CORS updated with Vercel domains

---

**Ready?** Choose an option above and run the commands! 🚀


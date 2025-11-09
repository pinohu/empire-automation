# 🆓 Free Backend Deployment Options

## ✅ All Free Options for FastAPI Backend

### Option 1: Render (Recommended - Completely Free)

**Free Tier Includes:**
- ✅ 750 hours/month (enough for 24/7)
- ✅ Automatic HTTPS
- ✅ Free PostgreSQL database
- ✅ Environment variables
- ✅ Auto-deploy from GitHub

**Deploy Steps:**
1. Go to: https://render.com
2. Sign up (free)
3. New → Web Service
4. Connect GitHub → Select your repo
5. Configure:
   - **Name**: empire-automation-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_api.py`
6. Add environment variables (copy from `.env`)
7. Deploy → Get your Render URL (e.g., `https://empire-automation-api.onrender.com`)

**Note**: Free tier spins down after 15 minutes of inactivity, but wakes up on first request (takes ~30 seconds).

---

### Option 2: Fly.io (Free Tier Available)

**Free Tier Includes:**
- ✅ 3 shared VMs
- ✅ 3GB persistent volumes
- ✅ 160GB outbound data transfer

**Deploy Steps:**
1. Install Fly CLI: `powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"`
2. Sign up: https://fly.io
3. Login: `fly auth login`
4. Deploy: `cd empire-automation && fly launch`
5. Follow prompts

---

### Option 3: Railway (Actually Free!)

**Railway Free Tier:**
- ✅ $5 credit/month (FREE)
- ✅ Enough for small projects
- ✅ No credit card required for free tier
- ✅ Auto-deploy from GitHub

**You won't pay anything** unless you exceed the $5/month credit (very unlikely for this project).

**Deploy Steps:**
1. Go to: https://railway.app
2. Sign up (no credit card needed for free tier)
3. New Project → Deploy from GitHub
4. Select repo → Deploy
5. Get your Railway URL

---

### Option 4: PythonAnywhere (Free Tier)

**Free Tier Includes:**
- ✅ 1 web app
- ✅ 512MB disk space
- ✅ MySQL database

**Deploy Steps:**
1. Sign up: https://www.pythonanywhere.com
2. Upload your code
3. Configure web app
4. Set start command

---

### Option 5: ngrok (For Local Backend - Testing)

**Free Tier:**
- ✅ 1 tunnel
- ✅ Random URL (changes on restart)
- ✅ Perfect for testing

**Use Case**: If you want to test with your local backend without deploying.

**Setup:**
1. Install: https://ngrok.com/download
2. Start backend: `python start_api.py`
3. Start ngrok: `ngrok http 8000`
4. Use ngrok URL in Vercel

---

## 🎯 Recommendation

**Best Free Option: Render**
- Completely free
- Easy setup
- Auto-deploy
- Free database
- Good for production

**Quick Testing: ngrok**
- Instant setup
- Use your local backend
- Perfect for development

---

## 📝 After Deploying (Any Option)

Once you have your backend URL:

```powershell
cd empire-automation/frontend
.\connect-backend.ps1
# Enter your backend URL when prompted
```

Or manually:
```powershell
vercel env rm NEXT_PUBLIC_API_URL production
vercel env add NEXT_PUBLIC_API_URL
# Enter your backend URL
vercel --prod
```

---

**All options above are FREE!** Choose the one that works best for you! 🎉


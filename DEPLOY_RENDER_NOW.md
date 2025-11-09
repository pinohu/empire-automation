# ⚡ Deploy to Render - Right Now! (100% Free)

## 🎯 Quickest Free Deployment

### Step 1: Push to GitHub

```bash
cd empire-automation
git add .
git commit -m "Ready for Render"
git push
```

### Step 2: Deploy on Render

1. **Go to**: https://render.com
2. **Sign up** (FREE, no credit card)
3. **New** → **Web Service**
4. **Connect GitHub** → Select repo
5. **Configure**:
   - Name: `empire-automation-api`
   - Environment: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `python start_api.py`
6. **Add Environment Variables**:
   - `CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app`
   - `PLAN_START_DATE=2024-01-01`
   - `ENVIRONMENT=production`
   - Copy other vars from `.env`
7. **Create** → Wait for deploy
8. **Copy URL** (e.g., `https://empire-automation-api.onrender.com`)

### Step 3: Connect Frontend

```powershell
cd empire-automation/frontend
.\connect-backend.ps1
# Enter your Render URL
```

---

## ✅ That's It!

**100% FREE** - No credit card, no payment, nothing!

---

**See DEPLOY_TO_RENDER.md for detailed steps.**


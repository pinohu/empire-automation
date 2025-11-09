# ⚡ Render Quick Start - 5 Minutes

## 🎯 Fastest Way to Deploy

### 1. Push to GitHub
```bash
cd empire-automation
git add .
git commit -m "Ready for Render"
git push
```

### 2. Deploy on Render

1. **Go to**: https://render.com
2. **Sign up** (FREE, no credit card)
3. **New** → **Web Service**
4. **Connect GitHub** → Select repo
5. **Configure**:
   ```
   Name: empire-automation-api
   Build: pip install -r requirements.txt
   Start: python start_api.py
   ```
6. **Add Environment Variables**:
   ```
   CORS_ORIGINS=http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app
   PLAN_START_DATE=2024-01-01
   ENVIRONMENT=production
   ```
   (Plus your API keys from `.env`)
7. **Add PostgreSQL** (New → PostgreSQL → Create)
8. **Deploy** → Copy URL

### 3. Connect Frontend

```powershell
cd empire-automation/frontend
.\connect-backend.ps1
# Enter your Render URL
```

---

## ✅ Done in 5 Minutes!

**See RENDER_DEPLOY_STEPS.md for detailed steps.**


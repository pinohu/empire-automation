# 🪂 Deploy Backend to Fly.io (Free Tier)

## Why Fly.io?

- ✅ **Free tier** available
- ✅ **Global edge network**
- ✅ **Fast cold starts**
- ✅ **Persistent storage**

---

## 🚀 Quick Deploy

### Step 1: Install Fly CLI

```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Step 2: Sign Up

1. Go to: https://fly.io
2. Sign up (free)
3. Verify email

### Step 3: Login

```bash
fly auth login
```

### Step 4: Deploy

```bash
cd empire-automation
fly launch
```

Follow the prompts:
- App name: `empire-automation-api`
- Region: Choose closest
- PostgreSQL: Yes (free)
- Redis: Optional

### Step 5: Set Environment Variables

```bash
fly secrets set CORS_ORIGINS="http://localhost:3000,https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app,https://*.vercel.app"
fly secrets set PLAN_START_DATE="2024-01-01"
# Add other secrets from your .env
```

### Step 6: Get URL

```bash
fly status
# Copy the URL shown
```

---

**Fly.io free tier is generous and great for FastAPI!** 🎉


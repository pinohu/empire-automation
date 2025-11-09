# 🔒 Backend CORS Configuration for Vercel

## Overview

Your FastAPI backend needs to allow requests from your Vercel deployment. Update your CORS configuration to include Vercel domains.

---

## 📝 Update CORS Configuration

### Option 1: Update `.env` File

Add your Vercel domain to `CORS_ORIGINS`:

```env
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app,https://*.vercel.app
```

### Option 2: Update `main.py` Directly

In `empire_automation/api/main.py`, find the CORS configuration and update:

```python
# Current (example)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Update to include Vercel domains
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,https://*.vercel.app"
).split(",")
```

### Option 3: Environment Variable (Recommended)

Set in your backend deployment platform (Railway, Render, etc.):

```
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app,https://*.vercel.app
```

**Note**: Replace `your-app.vercel.app` with your actual Vercel domain.

---

## ✅ Wildcard Support

To allow all Vercel preview deployments:

```
CORS_ORIGINS=http://localhost:3000,https://*.vercel.app
```

This allows:
- `https://your-app.vercel.app` (production)
- `https://your-app-git-branch.vercel.app` (preview deployments)

---

## 🔍 Verify CORS Configuration

After updating, test with:

```bash
curl -H "Origin: https://your-app.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://your-backend-api.com/api/health
```

Should return CORS headers including your Vercel domain.

---

## 🚨 Common Issues

### CORS Error in Browser

**Error**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solution**: 
1. Check `CORS_ORIGINS` includes your Vercel domain
2. Restart backend after updating CORS
3. Verify exact domain matches (including `https://`)

### Preview Deployments Not Working

**Solution**: Use wildcard `https://*.vercel.app` in CORS_ORIGINS

---

## 📚 FastAPI CORS Documentation

For more details, see: [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)


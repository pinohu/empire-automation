# ⚡ Vercel Deployment - Quick Start

## 🚀 Fastest Way to Deploy

### 1. Push to GitHub
```bash
cd empire-automation/frontend
git init
git add .
git commit -m "Ready for Vercel"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy on Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. **IMPORTANT**: Set **Root Directory** to `frontend`
4. Add Environment Variable:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: Your backend URL (e.g., `https://your-api.railway.app`)
5. Click **Deploy**

### 3. Done! 🎉
Your app will be live at `https://your-app.vercel.app`

---

## 🔧 Environment Variables

**Required**: `NEXT_PUBLIC_API_URL`
- Production: Your deployed backend URL
- Example: `https://your-api.railway.app` or `https://api.yourdomain.com`

---

## ⚠️ Important Notes

1. **Root Directory**: Must be set to `frontend` in Vercel settings
2. **Backend CORS**: Ensure your backend allows your Vercel domain
3. **Environment Variables**: Must start with `NEXT_PUBLIC_` for client-side access

---

## 📖 Full Guide

See `DEPLOY_TO_VERCEL.md` for detailed instructions.


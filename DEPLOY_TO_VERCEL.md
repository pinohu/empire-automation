# 🚀 Deploy to Vercel - Complete Guide

## Overview

This guide will help you deploy the Empire Automation frontend to Vercel. The frontend is a Next.js application that connects to a FastAPI backend.

---

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub/GitLab/Bitbucket**: Your code should be in a Git repository
3. **Backend API**: Your FastAPI backend should be deployed (see Backend Deployment section)

---

## 🎯 Quick Deploy (Recommended)

### Option 1: Deploy via Vercel Dashboard

1. **Push code to GitHub**:
   ```bash
   cd empire-automation/frontend
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import Project in Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Git Repository"
   - Select your repository
   - **Important**: Set Root Directory to `frontend`
   - Click "Deploy"

3. **Configure Environment Variables**:
   - In Vercel dashboard, go to your project → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-api.com` (or your backend URL)

4. **Redeploy**: After adding environment variables, trigger a new deployment

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd empire-automation/frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? empire-automation-frontend (or your choice)
# - Directory? ./
# - Override settings? No

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL
# Enter your backend API URL when prompted

# Deploy to production
vercel --prod
```

---

## ⚙️ Configuration

### Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-api.railway.app` or `https://api.yourdomain.com` |

**Important**: 
- For production: Use your deployed backend URL
- For preview deployments: You can use the same URL or a staging backend

### Root Directory

**Critical**: When importing the project, set the **Root Directory** to `frontend` since the Next.js app is in a subdirectory.

In Vercel Dashboard:
1. Go to Project Settings → General
2. Under "Root Directory", click "Edit"
3. Set to: `frontend`
4. Save

---

## 🔧 Build Configuration

The project is already configured for Vercel:

- **Framework**: Next.js (auto-detected)
- **Build Command**: `npm run build` (default)
- **Output Directory**: `.next` (default)
- **Install Command**: `npm install` (default)

### Custom Build Settings (if needed)

If you need custom settings, edit `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs"
}
```

---

## 🌐 Backend Deployment Options

Your FastAPI backend needs to be deployed separately. Options:

### Option 1: Railway (Recommended)
- Easy deployment
- Free tier available
- Automatic HTTPS
- Environment variable support

### Option 2: Render
- Free tier available
- Easy setup
- Automatic deployments

### Option 3: DigitalOcean App Platform
- Pay-as-you-go
- Good performance

### Option 4: AWS/GCP/Azure
- Enterprise-grade
- More complex setup

### Option 5: Self-hosted
- VPS (DigitalOcean, Linode, etc.)
- Full control
- Requires server management

---

## 📝 Step-by-Step Deployment

### Step 1: Prepare Your Code

```bash
# Navigate to project root
cd empire-automation

# Ensure frontend is ready
cd frontend
npm install
npm run build  # Test build locally
```

### Step 2: Push to Git

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Vercel deployment"

# Push to GitHub/GitLab/Bitbucket
git remote add origin <your-repo-url>
git push -u origin main
```

### Step 3: Deploy to Vercel

1. **Via Dashboard**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your Git repository
   - **Set Root Directory to `frontend`**
   - Add environment variable: `NEXT_PUBLIC_API_URL`
   - Click "Deploy"

2. **Via CLI**:
   ```bash
   cd frontend
   vercel
   ```

### Step 4: Configure Environment Variables

In Vercel Dashboard:
1. Go to your project
2. Settings → Environment Variables
3. Add:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: Your backend API URL (e.g., `https://your-api.railway.app`)
   - Environment: Production, Preview, Development (select all)

### Step 5: Update API Client (if needed)

The API client already uses `process.env.NEXT_PUBLIC_API_URL`, so it will automatically use the Vercel environment variable.

### Step 6: Test Deployment

1. Visit your Vercel deployment URL
2. Check browser console for any errors
3. Verify API connection works
4. Test all dashboard pages

---

## 🔒 Security Considerations

### CORS Configuration

Ensure your backend CORS settings allow your Vercel domain:

```python
# In your FastAPI backend (main.py)
CORS_ORIGINS = [
    "http://localhost:3000",  # Local development
    "https://your-app.vercel.app",  # Vercel deployment
    "https://*.vercel.app",  # All Vercel preview deployments
]
```

### Environment Variables

- ✅ Never commit `.env.local` to Git
- ✅ Use Vercel's environment variables for secrets
- ✅ Use different API URLs for production vs. preview

---

## 🚀 Custom Domain (Optional)

1. In Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update `NEXT_PUBLIC_API_URL` if needed

---

## 📊 Monitoring & Analytics

Vercel provides:
- **Analytics**: Automatic performance monitoring
- **Logs**: View deployment and runtime logs
- **Speed Insights**: Performance metrics

Enable in Vercel Dashboard → Settings → Analytics

---

## 🔄 Continuous Deployment

Vercel automatically deploys:
- **Production**: On push to `main` branch
- **Preview**: On every pull request
- **Development**: On push to other branches

---

## 🐛 Troubleshooting

### Build Fails

1. **Check logs**: Vercel Dashboard → Deployments → Click failed deployment
2. **Common issues**:
   - Missing dependencies: Check `package.json`
   - TypeScript errors: Run `npm run build` locally first
   - Environment variables: Ensure `NEXT_PUBLIC_API_URL` is set

### API Connection Issues

1. **Check CORS**: Ensure backend allows Vercel domain
2. **Check API URL**: Verify `NEXT_PUBLIC_API_URL` is correct
3. **Check backend**: Ensure backend is deployed and accessible
4. **Check network**: Open browser DevTools → Network tab

### Environment Variables Not Working

1. **Redeploy**: Environment variables require a new deployment
2. **Check naming**: Must start with `NEXT_PUBLIC_` for client-side access
3. **Check scope**: Ensure variables are set for correct environment (Production/Preview)

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Environment Variables](https://vercel.com/docs/environment-variables)

---

## ✅ Deployment Checklist

- [ ] Code pushed to Git repository
- [ ] Vercel account created
- [ ] Project imported in Vercel
- [ ] Root directory set to `frontend`
- [ ] Environment variable `NEXT_PUBLIC_API_URL` configured
- [ ] Backend deployed and accessible
- [ ] Backend CORS configured for Vercel domain
- [ ] Build successful
- [ ] Frontend accessible at Vercel URL
- [ ] API connection working
- [ ] All dashboard pages functional

---

## 🎉 Success!

Once deployed, your dashboard will be available at:
- **Production**: `https://your-app.vercel.app`
- **Preview**: `https://your-app-git-branch.vercel.app`

The dashboard will automatically refresh every 30 seconds and all CRUD operations will work with your deployed backend!

---

## 💡 Pro Tips

1. **Use Preview Deployments**: Test changes before merging to main
2. **Monitor Performance**: Enable Vercel Analytics
3. **Set Up Alerts**: Configure deployment notifications
4. **Use Branch Protection**: Protect main branch in Git
5. **Backup Environment Variables**: Keep a record of your env vars

---

**Need Help?** Check Vercel's [support documentation](https://vercel.com/support) or [community forum](https://github.com/vercel/vercel/discussions).


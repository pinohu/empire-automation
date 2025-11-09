# 🚀 Deploy Now - Step by Step

## Current Status
✅ Code is committed and ready
✅ Vercel CLI installed (or will be)
✅ Configuration files created

## Next Steps

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Login to Vercel**:
   ```bash
   cd empire-automation/frontend
   vercel login
   ```
   - This will open your browser to authenticate

2. **Deploy**:
   ```bash
   vercel
   ```
   - Follow the prompts:
     - Set up and deploy? **Yes**
     - Which scope? (select your account)
     - Link to existing project? **No**
     - Project name? **empire-automation-frontend** (or your choice)
     - Directory? **./** (current directory)
     - Override settings? **No**

3. **Set Environment Variable**:
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   ```
   - Enter your backend API URL when prompted
   - Select environments: Production, Preview, Development

4. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard

1. **Push to GitHub** (if not already done):
   ```bash
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Go to Vercel**:
   - Visit: https://vercel.com/new
   - Click "Import Git Repository"
   - Select your repository

3. **Configure Project**:
   - **Root Directory**: Set to `frontend`
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

4. **Add Environment Variable**:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: Your backend API URL
   - Environments: Production, Preview, Development

5. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete

## After Deployment

1. **Get Your URL**: Vercel will provide a URL like `https://your-app.vercel.app`

2. **Update Backend CORS**:
   - Add your Vercel URL to backend `CORS_ORIGINS`
   - Example: `CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app,https://*.vercel.app`

3. **Test**:
   - Visit your Vercel URL
   - Check that API connection works
   - Test all dashboard pages

## Troubleshooting

- **Build fails**: Check Vercel logs in dashboard
- **API not connecting**: Verify `NEXT_PUBLIC_API_URL` is set correctly
- **CORS errors**: Update backend CORS settings

## Need Help?

See `DEPLOY_TO_VERCEL.md` for detailed instructions.


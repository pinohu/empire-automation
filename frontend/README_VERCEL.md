# 🚀 Vercel Deployment

## Quick Deploy

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Ready for Vercel"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your repository
   - **Set Root Directory to `frontend`**
   - Add environment variable: `NEXT_PUBLIC_API_URL` = your backend URL
   - Deploy!

## Environment Variables

Required: `NEXT_PUBLIC_API_URL`
- Set in Vercel Dashboard → Settings → Environment Variables
- Example: `https://your-api.railway.app`

## Important

- Root Directory must be `frontend` (since Next.js app is in subdirectory)
- Backend CORS must allow your Vercel domain
- See `../DEPLOY_TO_VERCEL.md` for full guide


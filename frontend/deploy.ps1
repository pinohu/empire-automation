# Deploy to Vercel Script
Write-Host "`n🚀 Empire Automation - Vercel Deployment`n" -ForegroundColor Cyan

# Check if Vercel CLI is installed
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host "Step 1: Login to Vercel" -ForegroundColor Green
Write-Host "This will open your browser to authenticate...`n" -ForegroundColor White
vercel login

Write-Host "`nStep 2: Deploying to Vercel...`n" -ForegroundColor Green
Write-Host "Follow the prompts:" -ForegroundColor Yellow
Write-Host "  - Set up and deploy? Yes" -ForegroundColor White
Write-Host "  - Which scope? (select your account)" -ForegroundColor White
Write-Host "  - Link to existing project? No" -ForegroundColor White
Write-Host "  - Project name? empire-automation-frontend (or your choice)" -ForegroundColor White
Write-Host "  - Directory? ./ (current directory)`n" -ForegroundColor White

vercel

Write-Host "`nStep 3: Setting environment variable...`n" -ForegroundColor Green
Write-Host "Enter your backend API URL when prompted:" -ForegroundColor Yellow
Write-Host "  Example: https://your-api.railway.app`n" -ForegroundColor White

$apiUrl = Read-Host "Enter your backend API URL"
vercel env add NEXT_PUBLIC_API_URL production
vercel env add NEXT_PUBLIC_API_URL preview
vercel env add NEXT_PUBLIC_API_URL development

Write-Host "`nStep 4: Deploying to production...`n" -ForegroundColor Green
vercel --prod

Write-Host "`n✅ Deployment complete!`n" -ForegroundColor Green
Write-Host "Your app is now live at the URL shown above." -ForegroundColor Cyan
Write-Host "`n⚠️ Don't forget to update your backend CORS settings!" -ForegroundColor Yellow
Write-Host "See ../BACKEND_CORS_SETUP.md for instructions.`n" -ForegroundColor White


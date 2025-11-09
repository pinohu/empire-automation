# Connect Frontend to Backend Script
Write-Host "`n🔗 Connect Frontend to Backend`n" -ForegroundColor Cyan

Write-Host "Step 1: Enter your backend API URL" -ForegroundColor Yellow
Write-Host "Examples:" -ForegroundColor White
Write-Host "  - Railway: https://your-app.railway.app" -ForegroundColor Gray
Write-Host "  - Render: https://your-app.onrender.com" -ForegroundColor Gray
Write-Host "  - ngrok: https://abc123.ngrok.io`n" -ForegroundColor Gray

$backendUrl = Read-Host "Enter your backend API URL"

if ([string]::IsNullOrWhiteSpace($backendUrl)) {
    Write-Host "❌ No URL provided. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 2: Removing old environment variables...`n" -ForegroundColor Yellow
vercel env rm NEXT_PUBLIC_API_URL production --yes
vercel env rm NEXT_PUBLIC_API_URL preview --yes
vercel env rm NEXT_PUBLIC_API_URL development --yes

Write-Host "`nStep 3: Setting new environment variable...`n" -ForegroundColor Yellow
Write-Host "Setting for Production..." -ForegroundColor White
echo $backendUrl | vercel env add NEXT_PUBLIC_API_URL production

Write-Host "Setting for Preview..." -ForegroundColor White
echo $backendUrl | vercel env add NEXT_PUBLIC_API_URL preview

Write-Host "Setting for Development..." -ForegroundColor White
echo $backendUrl | vercel env add NEXT_PUBLIC_API_URL development

Write-Host "`nStep 4: Redeploying to production...`n" -ForegroundColor Yellow
vercel --prod

Write-Host "`n✅ Connection complete!`n" -ForegroundColor Green
Write-Host "Your frontend is now connected to: $backendUrl" -ForegroundColor Cyan
Write-Host "`nVisit: https://frontend-m9mimxfbk-polycarpohu-gmailcoms-projects.vercel.app" -ForegroundColor Cyan
Write-Host "`n⚠️  Don't forget to update backend CORS to allow your Vercel domain!`n" -ForegroundColor Yellow


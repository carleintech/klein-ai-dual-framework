#!/usr/bin/env pwsh
# check-health.ps1 - Check if both servers are running
# Usage: .\check-health.ps1

Write-Host "🔍 Checking Klein AI Dual Framework Health..." -ForegroundColor Blue
Write-Host ""

# Check Backend
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:3002/health" -TimeoutSec 5 -ErrorAction Stop
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend (FastAPI): http://localhost:3002 - OK" -ForegroundColor Green
    }
}
catch {
    Write-Host "❌ Backend (FastAPI): http://localhost:3002 - NOT RESPONDING" -ForegroundColor Red
    Write-Host "   Try: cd backend && python -m uvicorn app:app --reload --port 3002" -ForegroundColor Yellow
}

# Check Frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction Stop
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend (Next.js): http://localhost:3000 - OK" -ForegroundColor Green
    }
}
catch {
    Write-Host "❌ Frontend (Next.js): http://localhost:3000 - NOT RESPONDING" -ForegroundColor Red
    Write-Host "   Try: cd frontend && pnpm dev" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 To launch both servers: npm run dev or .\dev.ps1" -ForegroundColor Cyan

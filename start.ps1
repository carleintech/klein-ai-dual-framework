#!/usr/bin/env pwsh
# start.ps1 - Quick Start Klein AI Dual Framework
# Usage: .\start.ps1

Write-Host "🚀 Quick Starting Klein AI Dual Framework..." -ForegroundColor Green

# Start backend
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$($PWD)\backend'; python -m uvicorn app:app --reload --port 3002"

# Wait a moment
Start-Sleep -Seconds 2

# Start frontend
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$($PWD)\frontend'; pnpm dev"

Write-Host ""
Write-Host "✅ Servers starting in separate windows..." -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔗 Backend:  http://localhost:3002" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:3002/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Close the PowerShell windows to stop the servers" -ForegroundColor Yellow

#!/usr/bin/env pwsh
# Quick Deployment Script for Klein AI Dual Framework
# Usage: .\deploy.ps1 [platform]
# Platforms: vercel, railway, render

param(
    [string]$Platform = "vercel"
)

Write-Host "🚀 Klein AI Dual Framework - Quick Deploy" -ForegroundColor Green
Write-Host "Platform: $Platform" -ForegroundColor Yellow

# Check if git repo is clean
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  Uncommitted changes detected. Committing..." -ForegroundColor Yellow
    git add .
    git commit -m "Pre-deployment commit - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

# Push to GitHub (required for most platforms)
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Blue
git push origin main

switch ($Platform.ToLower()) {
    "vercel" {
        Write-Host "🔵 Deploying to Vercel..." -ForegroundColor Blue

        # Install Vercel CLI if not present
        if (!(Get-Command "vercel" -ErrorAction SilentlyContinue)) {
            Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
            npm install -g vercel
        }

        # Deploy
        vercel --prod
        Write-Host "✅ Deployment complete! Check your Vercel dashboard for URLs." -ForegroundColor Green
    }

    "railway" {
        Write-Host "🚆 Deploying to Railway..." -ForegroundColor Blue

        # Check Railway CLI
        if (!(Get-Command "railway" -ErrorAction SilentlyContinue)) {
            Write-Host "Installing Railway CLI..." -ForegroundColor Yellow
            npm install -g @railway/cli
        }

        # Deploy backend
        Write-Host "Deploying backend..." -ForegroundColor Yellow
        Push-Location backend
        railway login
        railway init
        railway up
        Pop-Location

        # Deploy frontend
        Write-Host "Deploying frontend..." -ForegroundColor Yellow
        Push-Location frontend
        railway init
        railway up
        Pop-Location

        Write-Host "✅ Deployment complete! Check your Railway dashboard for URLs." -ForegroundColor Green
    }

    "render" {
        Write-Host "🎨 Render deployment requires manual setup via dashboard" -ForegroundColor Blue
        Write-Host "Visit: https://render.com" -ForegroundColor Cyan
        Write-Host "Connect your GitHub repo: https://github.com/carleintech/kobklein-platform" -ForegroundColor Cyan
        Write-Host "✅ Instructions displayed above." -ForegroundColor Green
    }

    default {
        Write-Host "❌ Unknown platform: $Platform" -ForegroundColor Red
        Write-Host "Available platforms: vercel, railway, render" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Green
Write-Host "1. Update environment variables on deployment platform" -ForegroundColor White
Write-Host "2. Test deployed URLs" -ForegroundColor White
Write-Host "3. Update README with deployment URLs" -ForegroundColor White
Write-Host "4. Record demo video" -ForegroundColor White
Write-Host "5. Submit to Devpost" -ForegroundColor White

Write-Host "`n🏆 Good luck with your hackathon submission!" -ForegroundColor Green

#!/usr/bin/env pwsh
# dev.ps1 - Launch Klein AI Dual Framework in Development Mode
# Usage: .\dev.ps1

Write-Host "🚀 Starting Klein AI Dual Framework..." -ForegroundColor Green
Write-Host "📦 Backend: FastAPI on http://localhost:3002" -ForegroundColor Cyan
Write-Host "🌐 Frontend: Next.js on http://localhost:3000" -ForegroundColor Cyan
Write-Host "⚡ Elastic: Real Elasticsearch integration enabled" -ForegroundColor Yellow
Write-Host ""

# Function to cleanup background jobs on exit
function Cleanup {
    Write-Host "`n🛑 Shutting down servers..." -ForegroundColor Yellow
    Get-Job | Stop-Job
    Get-Job | Remove-Job
    Write-Host "✅ Cleanup complete!" -ForegroundColor Green
    exit
}

# Setup signal handling for clean exit
$null = Register-EngineEvent PowerShell.Exiting -Action { Cleanup }

# Trap Ctrl+C for graceful shutdown
trap { Cleanup }

try {
    # Check if backend dependencies are installed
    Write-Host "🔍 Checking Python dependencies..." -ForegroundColor Blue
    Set-Location "backend"
    $pipCheck = python -c "import fastapi, uvicorn; print('OK')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to install Python dependencies!" -ForegroundColor Red
            exit 1
        }
    }

    Set-Location ".."

    # Check if frontend dependencies are installed
    Write-Host "🔍 Checking Node.js dependencies..." -ForegroundColor Blue
    Set-Location "frontend"
    if (!(Test-Path "node_modules")) {
        Write-Host "📦 Installing Node.js dependencies..." -ForegroundColor Yellow
        pnpm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to install Node.js dependencies!" -ForegroundColor Red
            exit 1
        }
    }

    Set-Location ".."

    Write-Host "✅ All dependencies ready!" -ForegroundColor Green
    Write-Host ""

    # Start backend server in background
    Write-Host "🔧 Starting FastAPI backend server..." -ForegroundColor Blue
    $backendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location "backend"
        python -m uvicorn app:app --reload --port 3002
    }

    # Wait a moment for backend to start
    Start-Sleep -Seconds 3

    # Check if backend started successfully
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3002/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✅ Backend server running on http://localhost:3002" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Backend server starting (may take a few more seconds)..." -ForegroundColor Yellow
    }

    # Start frontend server in background
    Write-Host "🔧 Starting Next.js frontend server..." -ForegroundColor Blue
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location "frontend"
        pnpm dev
    }

    Start-Sleep -Seconds 5

    Write-Host ""
    Write-Host "🎉 Klein AI Dual Framework is running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "🔗 Backend:  http://localhost:3002" -ForegroundColor Cyan
    Write-Host "📚 API Docs: http://localhost:3002/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💡 Press Ctrl+C to stop all servers" -ForegroundColor Yellow
    Write-Host ""

    # Monitor jobs and wait
    while ($true) {
        $jobs = Get-Job
        $runningJobs = $jobs | Where-Object { $_.State -eq "Running" }

        if ($runningJobs.Count -eq 0) {
            Write-Host "❌ All servers stopped unexpectedly!" -ForegroundColor Red
            break
        }

        # Check for any failed jobs
        $failedJobs = $jobs | Where-Object { $_.State -eq "Failed" }
        if ($failedJobs.Count -gt 0) {
            Write-Host "❌ Some servers failed:" -ForegroundColor Red
            foreach ($job in $failedJobs) {
                Write-Host "  - Job failed: $($job.Name)" -ForegroundColor Red
                Receive-Job $job
            }
            break
        }

        Start-Sleep -Seconds 2
    }
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}
finally {
    Cleanup
}

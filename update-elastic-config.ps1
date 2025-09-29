#!/usr/bin/env pwsh
# Elastic Configuration Update Script
# Usage: .\update-elastic-config.ps1 -CloudId "your_id" -Password "your_pass"

param(
    [Parameter(Mandatory=$true)]
    [string]$CloudId,

    [Parameter(Mandatory=$true)]
    [string]$Password,

    [string]$Username = "elastic"
)

Write-Host "🔧 Updating Elastic Configuration..." -ForegroundColor Green

# Navigate to backend directory
$BackendPath = "C:\Users\carle\Documents\TECHKLEIN\GitHub\Hacketon\klein-ai-dual\backend"
Push-Location $BackendPath

# Backup current .env
if (Test-Path ".env") {
    Copy-Item ".env" ".env.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "✅ Backed up existing .env file" -ForegroundColor Yellow
}

# Update .env file
$envContent = Get-Content ".env"
$envContent = $envContent -replace '^ELASTIC_CLOUD_ID=.*', "ELASTIC_CLOUD_ID=$CloudId"
$envContent = $envContent -replace '^ELASTIC_USER=.*', "ELASTIC_USER=$Username"
$envContent = $envContent -replace '^ELASTIC_PASS=.*', "ELASTIC_PASS=$Password"

$envContent | Set-Content ".env"

Write-Host "✅ Updated .env with Elastic credentials" -ForegroundColor Green

# Test connection
Write-Host "🧪 Testing Elastic connection..." -ForegroundColor Blue

try {
    python -c @"
import os
from dotenv import load_dotenv
load_dotenv()

# Test if elasticsearch package is available
try:
    from elasticsearch import Elasticsearch

    cloud_id = os.getenv('ELASTIC_CLOUD_ID')
    username = os.getenv('ELASTIC_USER')
    password = os.getenv('ELASTIC_PASS')

    if cloud_id and username and password:
        es = Elasticsearch(cloud_id=cloud_id, basic_auth=(username, password))
        info = es.info()
        print('✅ Elastic connection successful!')
        print(f'Cluster: {info[\"cluster_name\"]}')
        print(f'Version: {info[\"version\"][\"number\"]}')
    else:
        print('❌ Missing credentials')

except ImportError:
    print('⚠️  elasticsearch package not installed')
    print('Install with: pip install elasticsearch')
except Exception as e:
    print(f'❌ Connection failed: {e}')
"@

    Write-Host "✅ Configuration complete!" -ForegroundColor Green

} catch {
    Write-Host "⚠️  Could not test connection. Install elasticsearch package:" -ForegroundColor Yellow
    Write-Host "pip install elasticsearch" -ForegroundColor Cyan
}

Pop-Location

Write-Host "`n🚀 Next Steps:" -ForegroundColor Green
Write-Host "1. Restart your backend: python simple_app.py" -ForegroundColor White
Write-Host "2. Test the application at http://localhost:3000" -ForegroundColor White
Write-Host "3. Verify real Elastic search is working" -ForegroundColor White

Write-Host "`n🎯 Your Klein AI Dual Framework now has real Elastic power! 🔍" -ForegroundColor Green

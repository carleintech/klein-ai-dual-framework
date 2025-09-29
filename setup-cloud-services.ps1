# Automated Cloud Setup Script for Klein AI Dual Framework
# Run this script in PowerShell as Administrator

param(
    [switch]$SkipElastic,
    [switch]$SkipGCP,
    [string]$ProjectName = "klein-ai-dual"
)

Write-Host "🚀 Klein AI Dual Framework - Cloud Services Setup" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Function to check if command exists
function Test-Command($command) {
    try {
        Get-Command $command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Function to install Chocolatey
function Install-Chocolatey {
    if (!(Test-Command "choco")) {
        Write-Host "📦 Installing Chocolatey..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    } else {
        Write-Host "✅ Chocolatey already installed" -ForegroundColor Green
    }
}

# Function to setup Google Cloud
function Setup-GoogleCloud {
    Write-Host "`n🔧 Setting up Google Cloud Platform..." -ForegroundColor Cyan

    # Install gcloud CLI if not present
    if (!(Test-Command "gcloud")) {
        Write-Host "📥 Installing Google Cloud CLI..." -ForegroundColor Yellow
        Install-Chocolatey
        choco install gcloudsdk -y

        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }

    Write-Host "🔑 Initializing Google Cloud..." -ForegroundColor Yellow
    gcloud init --console-only

    # Get project ID
    $projectId = gcloud config get-value project
    if (!$projectId) {
        $projectId = "$ProjectName-$(Get-Random -Maximum 9999)"
        Write-Host "📝 Creating new project: $projectId" -ForegroundColor Yellow
        gcloud projects create $projectId --name="$ProjectName"
        gcloud config set project $projectId
    }

    Write-Host "⚡ Enabling required APIs..." -ForegroundColor Yellow
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable compute.googleapis.com

    Write-Host "👤 Creating service account..." -ForegroundColor Yellow
    $serviceAccount = "klein-ai-service"
    $serviceAccountEmail = "$serviceAccount@$projectId.iam.gserviceaccount.com"

    try {
        gcloud iam service-accounts create $serviceAccount --display-name="Klein AI Service" 2>$null
    } catch {
        Write-Host "ℹ️  Service account already exists" -ForegroundColor Blue
    }

    # Add required roles
    gcloud projects add-iam-policy-binding $projectId --member="serviceAccount:$serviceAccountEmail" --role="roles/aiplatform.user"

    # Generate service account key
    $keyPath = "./backend/gcp-service-key.json"
    gcloud iam service-accounts keys create $keyPath --iam-account=$serviceAccountEmail

    # Update .env file
    Write-Host "📝 Updating .env file with GCP configuration..." -ForegroundColor Yellow
    $envPath = "./backend/.env"
    $envContent = Get-Content $envPath
    $envContent = $envContent -replace '^GCP_PROJECT=.*', "GCP_PROJECT=$projectId"
    $envContent = $envContent -replace '^GOOGLE_APPLICATION_CREDENTIALS=.*', 'GOOGLE_APPLICATION_CREDENTIALS=./gcp-service-key.json'
    $envContent | Set-Content $envPath

    Write-Host "✅ Google Cloud setup complete!" -ForegroundColor Green
    Write-Host "   Project ID: $projectId" -ForegroundColor Gray
    Write-Host "   Service Account: $serviceAccountEmail" -ForegroundColor Gray
    Write-Host "   Credentials: $keyPath" -ForegroundColor Gray
}

# Function to setup Elastic Cloud (Interactive)
function Setup-ElasticCloud {
    Write-Host "`n🔧 Setting up Elastic Cloud..." -ForegroundColor Cyan
    Write-Host "📋 Please follow these steps:" -ForegroundColor Yellow
    Write-Host "1. Go to https://cloud.elastic.co/" -ForegroundColor White
    Write-Host "2. Create account or sign in" -ForegroundColor White
    Write-Host "3. Create a new deployment (Free tier)" -ForegroundColor White
    Write-Host "4. Copy the Cloud ID and password" -ForegroundColor White

    # Prompt for values
    $cloudId = Read-Host "`nEnter your Elastic Cloud ID"
    $password = Read-Host "Enter your Elastic password" -AsSecureString
    $passwordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

    # Update .env file
    Write-Host "📝 Updating .env file with Elastic configuration..." -ForegroundColor Yellow
    $envPath = "./backend/.env"
    $envContent = Get-Content $envPath
    $envContent = $envContent -replace '^ELASTIC_CLOUD_ID=.*', "ELASTIC_CLOUD_ID=$cloudId"
    $envContent = $envContent -replace '^ELASTIC_USER=.*', 'ELASTIC_USER=elastic'
    $envContent = $envContent -replace '^ELASTIC_PASS=.*', "ELASTIC_PASS=$passwordPlain"
    $envContent | Set-Content $envPath

    Write-Host "✅ Elastic Cloud setup complete!" -ForegroundColor Green
}

# Function to test connections
function Test-Connections {
    Write-Host "`n🧪 Testing connections..." -ForegroundColor Cyan

    # Load environment variables
    $envPath = "./backend/.env"
    if (Test-Path $envPath) {
        Get-Content $envPath | ForEach-Object {
            if ($_ -match '^([^#][^=]*)=(.*)$') {
                [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
            }
        }
    }

    # Test Google Cloud
    if ($env:GCP_PROJECT -and $env:GOOGLE_APPLICATION_CREDENTIALS) {
        Write-Host "🔍 Testing Google Cloud connection..." -ForegroundColor Yellow
        try {
            gcloud auth application-default print-access-token --quiet > $null
            Write-Host "✅ Google Cloud: Connected successfully" -ForegroundColor Green
        } catch {
            Write-Host "❌ Google Cloud: Connection failed" -ForegroundColor Red
        }
    }

    # Test Elastic Cloud
    if ($env:ELASTIC_CLOUD_ID -and $env:ELASTIC_USER -and $env:ELASTIC_PASS) {
        Write-Host "🔍 Testing Elastic Cloud connection..." -ForegroundColor Yellow
        try {
            $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$($env:ELASTIC_USER):$($env:ELASTIC_PASS)"))
            $headers = @{ 'Authorization' = "Basic $auth" }
            $endpoint = "https://$($env:ELASTIC_CLOUD_ID).es.us-east-1.aws.found.io:9243/"
            $response = Invoke-RestMethod -Uri $endpoint -Headers $headers -TimeoutSec 10
            Write-Host "✅ Elastic Cloud: Connected successfully" -ForegroundColor Green
        } catch {
            Write-Host "❌ Elastic Cloud: Connection failed" -ForegroundColor Red
        }
    }
}

# Main execution
try {
    # Check if running in backend directory
    if (!(Test-Path "./backend/.env")) {
        Write-Host "❌ Please run this script from the klein-ai-dual root directory" -ForegroundColor Red
        exit 1
    }

    # Setup services
    if (!$SkipGCP) {
        Setup-GoogleCloud
    }

    if (!$SkipElastic) {
        Setup-ElasticCloud
    }

    # Test connections
    Test-Connections

    Write-Host "`n🎉 Setup complete! Your Klein AI Dual Framework is ready for cloud services." -ForegroundColor Green
    Write-Host "📖 Check the updated .env file for your configuration." -ForegroundColor Gray
    Write-Host "🚀 Start your backend with: python backend/simple_app.py" -ForegroundColor Gray

} catch {
    Write-Host "`n❌ Setup failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "📖 Please check the cloud-services-setup.md guide for manual setup." -ForegroundColor Yellow
}

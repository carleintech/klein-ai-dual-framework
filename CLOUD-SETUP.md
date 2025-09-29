# Quick Setup Commands for Klein AI Dual Framework

## 🚀 Google Cloud Setup (5 minutes)

### Step 1: Install Google Cloud CLI

```powershell
# Download installer
Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile "gcloud-installer.exe"
Start-Process -FilePath "gcloud-installer.exe" -Wait
```

### Step 2: Login and Create Project

```powershell
# Login to Google Cloud
gcloud auth login

# Create new project (replace with your preferred name)
gcloud projects create klein-ai-hackathon-$(Get-Random -Maximum 9999) --name="Klein AI Hackathon"

# List projects and set active one
gcloud projects list
gcloud config set project YOUR_PROJECT_ID_HERE
```

### Step 3: Enable APIs and Create Service Account

```powershell
# Enable required APIs
gcloud services enable aiplatform.googleapis.com

# Create service account
gcloud iam service-accounts create klein-ai-service --display-name="Klein AI Service"

# Add permissions
$PROJECT_ID = gcloud config get-value project
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:klein-ai-service@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/aiplatform.user"

# Generate key file
gcloud iam service-accounts keys create "gcp-key.json" --iam-account="klein-ai-service@$PROJECT_ID.iam.gserviceaccount.com"
```

### Step 4: Update .env File

```powershell
# Get your project ID
$PROJECT_ID = gcloud config get-value project
Write-Host "Your GCP Project ID: $PROJECT_ID"

# Manually update backend/.env with:
# GCP_PROJECT=your_project_id_here
# GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
```

---

## ☁️ Elastic Cloud Setup (3 minutes)

### Web-based Setup (Recommended)

1. **Go to Elastic Cloud**

   - Visit: https://cloud.elastic.co/
   - Click "Start free trial"
   - Create account with your email

2. **Create Deployment**

   - Click "Create deployment"
   - Name: "klein-ai-search"
   - Template: "Elasticsearch"
   - Version: Latest (8.x)
   - Size: Free tier
   - Click "Create deployment"

3. **Save Credentials**

   - **Important**: Copy the password when shown (only shown once!)
   - Copy the Cloud ID from deployment overview
   - Username is always "elastic"

4. **Update .env File**
   ```
   ELASTIC_CLOUD_ID=your_cloud_id_here
   ELASTIC_USER=elastic
   ELASTIC_PASS=your_password_here
   ```

---

## 🧪 Test Your Setup

### Test Google Cloud

```powershell
# Test authentication
gcloud auth application-default print-access-token

# Test Vertex AI access
gcloud ai models list --region=us-central1 --limit=5
```

### Test Elastic Cloud

```powershell
# Test connection (replace with your credentials)
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("elastic:YOUR_PASSWORD"))
$headers = @{ 'Authorization' = "Basic $auth" }
Invoke-RestMethod -Uri "https://YOUR_CLOUD_ID.es.us-east-1.aws.found.io:9243/" -Headers $headers
```

---

## 📋 Final .env Configuration

Your `backend/.env` should look like this:

```env
# Elastic Configuration
ELASTIC_CLOUD_ID=deployment-name:very-long-cloud-id-string
ELASTIC_USER=elastic
ELASTIC_PASS=your-generated-password

# Google Cloud Configuration
GCP_PROJECT=klein-ai-hackathon-1234
GCP_LOCATION=us-central1
VERTEX_MODEL=text-bison@001

# Service Flags
ENERGY_MODE=normal
ALLOW_SHUTDOWN=true
CORS_ORIGINS=http://localhost:3000

# Optional: Google Cloud credentials file path
GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
```

---

## 🎯 Alternative: Use Demo Mode

If you want to skip cloud setup for now and focus on the demo:

1. **Keep empty credentials** in .env
2. **The app will use fallback stubs** automatically
3. **Perfect for hackathon demos** without cloud dependencies
4. **Add real services later** when ready for production

---

## 💡 Pro Tips

1. **Free Tiers**: Both services offer generous free tiers for hackathons
2. **Security**: Never commit .env files or JSON keys to Git
3. **Testing**: Test connections before running your app
4. **Fallbacks**: Klein AI works with or without cloud services

---

## 🆘 Need Help?

- **Google Cloud Console**: https://console.cloud.google.com/
- **Elastic Cloud Console**: https://cloud.elastic.co/
- **Documentation**: See `docs/cloud-services-setup.md` for detailed guide

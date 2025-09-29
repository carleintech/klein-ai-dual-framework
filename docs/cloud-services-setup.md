# Cloud Services Setup Guide

## 🔧 Elastic Cloud Configuration

### Option 1: Web Console Setup (Recommended for Beginners)

1. **Create Elastic Cloud Account**

   - Go to [https://cloud.elastic.co/](https://cloud.elastic.co/)
   - Click "Start free trial" or "Sign up"
   - Complete registration

2. **Create a Deployment**

   - Click "Create deployment"
   - Choose "Elasticsearch" template
   - Select region (closest to you)
   - Choose "Free" tier for testing
   - Click "Create deployment"

3. **Get Configuration Values**

   - After deployment creation, you'll see:
     - **Cloud ID**: Copy this value
     - **Username**: Usually "elastic"
     - **Password**: Generated automatically (save it!)

4. **Update .env file**
   ```bash
   ELASTIC_CLOUD_ID=your-cloud-id-here
   ELASTIC_USER=elastic
   ELASTIC_PASS=your-generated-password
   ```

### Option 2: CLI Setup (Advanced)

1. **Install Elastic CLI**

   ```powershell
   # Download and install ecctl (Elastic Cloud CLI)
   Invoke-WebRequest -Uri "https://download.elastic.co/downloads/ecctl/1.10.0/ecctl_1.10.0_windows_amd64.zip" -OutFile "ecctl.zip"
   Expand-Archive -Path "ecctl.zip" -DestinationPath "C:\tools\ecctl"
   $env:PATH += ";C:\tools\ecctl"
   ```

2. **Login to Elastic Cloud**

   ```powershell
   ecctl auth login
   # Follow prompts to authenticate
   ```

3. **Create Deployment via CLI**

   ```powershell
   # Create a basic Elasticsearch deployment
   ecctl deployment create --name "klein-ai-search" --version "8.11.0" --region "us-east-1"

   # Get deployment details
   ecctl deployment list
   ecctl deployment show <deployment-id>
   ```

---

## 🚀 Google Cloud Configuration

### Option 1: Web Console Setup (Recommended)

1. **Create Google Cloud Account**

   - Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
   - Sign up with Google account
   - Accept $300 free credit

2. **Create a New Project**

   - Click "Select a project" → "New Project"
   - Name: "klein-ai-dual" or similar
   - Note the **Project ID** (will be auto-generated)

3. **Enable Vertex AI API**

   - Go to "APIs & Services" → "Library"
   - Search "Vertex AI API"
   - Click "Enable"

4. **Create Service Account**

   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Name: "klein-ai-service"
   - Role: "Vertex AI User"
   - Click "Done"

5. **Generate Service Account Key**

   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON"
   - Download the file to your project folder

6. **Update .env file**
   ```bash
   GCP_PROJECT=your-project-id-here
   GCP_LOCATION=us-central1
   VERTEX_MODEL=text-bison@001
   GOOGLE_APPLICATION_CREDENTIALS=./path/to/service-account-key.json
   ```

### Option 2: CLI Setup (Fastest)

1. **Install Google Cloud CLI**

   ```powershell
   # Download and install gcloud CLI
   Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile "GoogleCloudSDKInstaller.exe"
   Start-Process -FilePath "GoogleCloudSDKInstaller.exe" -Wait
   ```

2. **Initialize gcloud**

   ```powershell
   # Initialize and login
   gcloud init
   gcloud auth login

   # Create new project
   gcloud projects create klein-ai-dual-$(Get-Random) --name="Klein AI Dual"

   # Set project
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable APIs and Create Service Account**

   ```powershell
   # Enable required APIs
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable compute.googleapis.com

   # Create service account
   gcloud iam service-accounts create klein-ai-service --display-name="Klein AI Service"

   # Add roles
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="serviceAccount:klein-ai-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" --role="roles/aiplatform.user"

   # Generate key file
   gcloud iam service-accounts keys create ./backend/gcp-service-key.json --iam-account=klein-ai-service@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

4. **Auto-populate .env**

   ```powershell
   # Get current project ID
   $PROJECT_ID = gcloud config get-value project

   # Update .env file
   (Get-Content ./backend/.env) -replace 'GCP_PROJECT=', "GCP_PROJECT=$PROJECT_ID" | Set-Content ./backend/.env
   (Get-Content ./backend/.env) -replace 'GOOGLE_APPLICATION_CREDENTIALS=', 'GOOGLE_APPLICATION_CREDENTIALS=./gcp-service-key.json' | Set-Content ./backend/.env
   ```

---

## 🎯 Quick Test Commands

### Test Elastic Connection

```powershell
# Test from PowerShell
$headers = @{
    'Authorization' = 'Basic ' + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$($env:ELASTIC_USER):$($env:ELASTIC_PASS)"))
}
Invoke-RestMethod -Uri "https://$($env:ELASTIC_CLOUD_ID).es.us-east-1.aws.found.io:9243/" -Headers $headers
```

### Test Google Cloud Connection

```powershell
# Test authentication
gcloud auth application-default print-access-token

# Test Vertex AI
gcloud ai models list --region=us-central1
```

---

## 💰 Cost Considerations

### Elastic Cloud

- **Free Tier**: 14-day trial with full features
- **Basic Plan**: $95/month for production
- **For Hackathon**: Free tier is sufficient

### Google Cloud

- **Free Tier**: $300 credit for 90 days
- **Vertex AI**: Pay per request (~$0.001 per 1K tokens)
- **For Hackathon**: Free credit covers extensive testing

---

## 🔒 Security Best Practices

1. **Never commit credentials to Git**

   ```bash
   echo "*.json" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables in production**
3. **Rotate keys regularly**
4. **Use least-privilege access roles**

---

## 🚨 Troubleshooting

### Common Elastic Issues

- **Connection timeout**: Check Cloud ID format
- **Authentication failed**: Verify username/password
- **SSL errors**: Ensure using HTTPS endpoints

### Common GCP Issues

- **Permission denied**: Check service account roles
- **Quota exceeded**: Monitor API usage in console
- **Invalid credentials**: Re-download service account key

---

## 📞 Support Resources

- **Elastic Cloud**: [https://discuss.elastic.co/](https://discuss.elastic.co/)
- **Google Cloud**: [https://cloud.google.com/support](https://cloud.google.com/support)
- **Vertex AI**: [https://cloud.google.com/vertex-ai/docs](https://cloud.google.com/vertex-ai/docs)

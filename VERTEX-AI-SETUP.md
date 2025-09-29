# 🧠 Klein AI Integration Setup Guide

## Add these to your `backend/.env` file:

```bash
# Existing Elastic Config (keep these)
ELASTIC_ENDPOINT=your_elastic_endpoint
ELASTIC_API_KEY=your_elastic_api_key

# Add these for Vertex AI (Gemini) Integration
GCP_PROJECT=your-gcp-project-id
GCP_LOCATION=us-central1
VERTEX_MODEL=gemini-1.5-flash

# Google Cloud Authentication (choose one method)
# Method 1: Service Account Key File
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Method 2: Service Account Key as JSON string
GOOGLE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"..."}
```

## 🚀 Quick Integration Steps:

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Update Klein Service

Copy the `get_klein_response` function from `complete_klein_function.py` and replace the existing function in `services/klein.py`.

### 3. Google Cloud Setup (Optional - for live AI)

```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Login and set project
gcloud auth login
gcloud config set project YOUR-PROJECT-ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Create service account (optional)
gcloud iam service-accounts create klein-ai-service
gcloud iam service-accounts keys create key.json \
    --iam-account klein-ai-service@YOUR-PROJECT-ID.iam.gserviceaccount.com
```

## 🧪 Testing

### Option 1: With Real Vertex AI

1. Set up GCP project and credentials
2. Add environment variables
3. Restart server: `python -m uvicorn app:app --reload --port 3002`

### Option 2: Smart Stubs (No Setup Required)

- Leave `GCP_PROJECT` empty in `.env`
- Klein automatically uses enhanced stub responses
- Still works with Elastic context!

## 🔥 Klein Response Features:

✅ **Elastic Context Integration** - Uses search results in responses
✅ **Vertex AI (Gemini) Integration** - Live AI responses when configured
✅ **Smart Fallback** - Enhanced stubs when AI unavailable
✅ **Energy Modes** - Handles brownout/peak energy scenarios
✅ **Empathy Detection** - Special handling for emotional queries
✅ **Safety Filters** - Built-in content safety

## 🎯 Result:

Klein now provides intelligent, context-aware responses using:

- **Real Elasticsearch** search results
- **Vertex AI Gemini** for natural language generation
- **Smart pattern matching** for common queries
- **Graceful fallbacks** when services unavailable

Perfect for your hackathon demo! 🏆

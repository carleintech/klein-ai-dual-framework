# Deployment Guide - Klein AI Dual Framework

## Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Git

### Backend (FastAPI)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials

uvicorn app:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local if needed

npm run dev
```

Access: http://localhost:3000

## Production Deployment

### Backend → Google Cloud Run

1. **Create Dockerfile** (backend/Dockerfile):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Deploy to Cloud Run**:
```bash
cd backend

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/klein-backend

# Deploy to Cloud Run
gcloud run deploy klein-backend \
  --image gcr.io/YOUR_PROJECT_ID/klein-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GCP_PROJECT=YOUR_PROJECT_ID,GCP_LOCATION=us-central1"
```

3. **Set Environment Variables** in Cloud Run Console:
- `ELASTIC_CLOUD_ID`
- `ELASTIC_USER`
- `ELASTIC_PASS`
- `GCP_PROJECT`
- `VERTEX_MODEL`

### Frontend → Firebase Hosting

1. **Build and Deploy**:
```bash
cd frontend

# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize project
firebase init hosting

# Build Next.js app
npm run build
npm run export

# Deploy to Firebase
firebase deploy
```

2. **Update Environment Variables**:
- Update `NEXT_PUBLIC_API_BASE_URL` to your Cloud Run URL
- Redeploy after changing env vars

## Environment Variables Reference

### Backend (.env)
```bash
# Required for Elastic integration
ELASTIC_CLOUD_ID=your_cloud_id
ELASTIC_USER=your_username
ELASTIC_PASS=your_password

# Required for Vertex AI
GCP_PROJECT=your_project_id
GCP_LOCATION=us-central1
VERTEX_MODEL=text-bison@001

# Optional service flags
ENERGY_MODE=normal
ALLOW_SHUTDOWN=true
CORS_ORIGINS=https://your-frontend-domain.web.app
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.run.app
NEXT_PUBLIC_APP_NAME=Klein AI Dual Framework
```

## Security Considerations

1. **Never commit credentials** to version control
2. **Use IAM roles** for Google Cloud services in production
3. **Enable HTTPS** for all production endpoints
4. **Restrict CORS origins** to known domains
5. **Monitor audit logs** for security events

## Monitoring & Logs

### Backend Logs
```bash
# View Cloud Run logs
gcloud logs tail --service=klein-backend

# View audit trail
cat backend/audit-log.jsonl
```

### Frontend Analytics
- Firebase Analytics automatically enabled
- Monitor performance in Firebase Console

## Scaling Considerations

- **Cloud Run**: Auto-scales based on traffic
- **Elastic**: Use appropriate tier for dataset size
- **Vertex AI**: Monitor quota usage
- **Frontend**: Firebase Hosting scales automatically

## Troubleshooting

### Common Issues
1. **CORS errors**: Check CORS_ORIGINS configuration
2. **API timeouts**: Increase Cloud Run timeout settings
3. **Vertex AI quota**: Monitor usage in Cloud Console
4. **Elastic connection**: Verify cloud ID and credentials

### Health Checks
- Backend: `GET /api/health`
- Frontend: Check browser console for errors

---

*For production deployments, always test in staging environment first*

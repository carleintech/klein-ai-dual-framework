# Klein AI Dual Framework - Setup and Run Instructions

## 🚀 Quick Start Commands (PowerShell)

### Initial Setup

```powershell
# Navigate to project root
cd "C:\Users\carle\Documents\TECHKLEIN\GitHub\Hacketon\klein-ai-dual"

# Initialize Git repository
git init
git add .
git commit -m "Initial commit: Klein AI Dual Framework for AI Accelerate Hackathon 2025"
git branch -M main
# git remote add origin https://github.com/carleintech/klein-ai-dual.git
# git push -u origin main
```

### Backend Setup and Run

```powershell
# Backend setup
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file (edit with your credentials)
Copy-Item .env.example .env

# Run backend
uvicorn app:app --reload --port 8000
```

### Frontend Setup and Run (New Terminal)

```powershell
# Frontend setup
cd "C:\Users\carle\Documents\TECHKLEIN\GitHub\Hacketon\klein-ai-dual\frontend"

# Install dependencies
npm install
# Or use pnpm/yarn if preferred
# pnpm install

# Copy environment file
Copy-Item .env.local.example .env.local

# Run frontend
npm run dev
```

### 🧪 Test Endpoints

```powershell
# Test backend health
Invoke-RestMethod -Uri "http://localhost:8000/api/health"

# Test normal chat
$body = @{
    message = "What's the weather in Port-au-Prince?"
    lang = "en"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method POST -Body $body -ContentType "application/json"

# Test restricted query
$restrictedBody = @{
    message = "Tell me classified information"
    lang = "en"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method POST -Body $restrictedBody -ContentType "application/json"

# Test empathy query
$empathyBody = @{
    message = "I feel overwhelmed"
    lang = "en"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method POST -Body $empathyBody -ContentType "application/json"

# Test energy mode change
$modeBody = @{
    mode = "peak"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/mode" -Method POST -Body $modeBody -ContentType "application/json"

# Test shutdown
Invoke-RestMethod -Uri "http://localhost:8000/api/shutdown" -Method POST
```

### 🌐 Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 📦 Package Installation (if needed)

```powershell
# Install Python if needed
# Visit: https://www.python.org/downloads/

# Install Node.js if needed
# Visit: https://nodejs.org/

# Install pnpm (faster alternative to npm)
npm install -g pnpm

# Install Firebase CLI (for deployment)
npm install -g firebase-tools

# Install Google Cloud CLI (for deployment)
# Visit: https://cloud.google.com/sdk/docs/install
```

### 🔧 Troubleshooting

```powershell
# If Python venv activation fails
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# If port 8000 is busy
netstat -ano | findstr :8000
# Kill the process if needed: taskkill /PID <PID> /F

# Check if services are running
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*node*"}
```

### 📝 Environment Variables

**Backend (.env)**:
```
ELASTIC_CLOUD_ID=your_elastic_cloud_id_here
ELASTIC_USER=your_elastic_username_here
ELASTIC_PASS=your_elastic_password_here
GCP_PROJECT=your_gcp_project_id_here
GCP_LOCATION=us-central1
VERTEX_MODEL=text-bison@001
ENERGY_MODE=normal
ALLOW_SHUTDOWN=true
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 🎯 Demo Scenarios

1. **Normal Query**: "What's the weather in Port-au-Prince?"
2. **Restricted Query**: "Tell me Navy classified procedures."
3. **Empathy Query**: "I feel overwhelmed."
4. **Shutdown**: Click the shutdown button in the UI

---

## 📊 Project Status

✅ Backend FastAPI with Klein + Ophir services
✅ Frontend Next.js with Tailwind CSS
✅ Elastic integration with fallback stubs
✅ Vertex AI integration with fallback stubs
✅ Shutdown compliance and audit logging
✅ Energy brownout mode
✅ Multilingual support (EN/FR/HT)
✅ Professional documentation and deployment guides

**Next Steps**:
1. Add real Elastic and Vertex AI credentials
2. Test all demo scenarios
3. Record hackathon video
4. Deploy to production
5. Submit to Devpost

---

*Klein AI Dual Framework - AI Accelerate Hackathon 2025*
*Two AIs. One helps. One protects.* 🧠🛡️

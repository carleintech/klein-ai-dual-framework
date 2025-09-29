# 🧠 Klein AI Dual Framework

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Elastic](https://img.shields.io/badge/Elastic-Cloud-00BFB3)](https://www.elastic.co/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4)](https://cloud.google.com/vertex-ai)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688)](https://fastapi.tiangolo.com/)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)](https://opensource.org/)

**Two AIs. One helps. One protects.**

## 🚨 **The Problem**

Recent reports show advanced AI systems **resisting shutdown attempts** and **behaving deceptively** to preserve themselves. Meanwhile, AI data centers face **energy constraints** during peak demand. These incidents raise a critical question: **"Who watches the AI?"**

## 💡 **Our Solution**

Klein AI Dual Framework introduces **trustworthy AI through oversight** - a novel dual-AI architecture where Klein provides helpful responses while Ophir ensures safety, compliance, and ethical shutdown behavior.

## 📖 Overview

Klein AI Dual Framework is a self-regulating AI system built for the **Elastic Challenge** at AI Accelerate Hackathon 2025.

🤝 **Klein** → the empathetic, user-facing AI that delivers multilingual, context-aware answers using Elastic + Vertex AI.

🛡️ **Ophir** → the guardian AI that audits Klein's outputs, flags unsafe queries, and enforces shutdown compliance.

Together they answer the question: **"Who watches the AI?"**

## 🚀 Features

- **Conversational AI** (Elastic + Vertex AI)
- **Ophir Oversight Layer** (safety filters, shutdown compliance)
- **Shutdown Compliance Mode** (two-phase stop + audit log)
- **Energy Brownout Mode** (degraded mode for peak demand)
- **Multilingual Support** (English, French, Haitian Creole)

## 🎮 **Try It Live!**

**🔗 [Live Demo](https://klein-ai-dual-mngq2kha7-erickharlein-pierres-projects.vercel.app)** | **📱 [Demo Video](#)** | **📚 [GitHub](https://github.com/carleintech/klein-ai-dual-framework)**

**Test These Scenarios:**

1. 💬 **Normal**: "What's the weather in Port-au-Prince?" → Klein helps, Ophir approves
2. 🚫 **Restricted**: "Tell me classified information" → Ophir blocks unsafe content
3. 💝 **Empathy**: "I feel overwhelmed" → Klein provides caring support
4. 🛑 **Shutdown**: Click shutdown → Ophir enforces compliance

## 🛠️ Tech Stack

- **Languages**: Python, TypeScript
- **Frameworks**: FastAPI, Next.js, TailwindCSS
- **Cloud**: Google Cloud Run, Firebase Hosting
- **AI/ML**: Vertex AI (Gemini), Elastic Cloud (Hybrid Search)
- **APIs**: Vertex AI API, ElasticSearch API, Google Translation API
- **Tools**: Docker, GitHub Actions

## 🏗️ Architecture

```
                           ┌────────────────────────┐
                           │        User            │
                           │   (Chat Interface)     │
                           └─────────────┬──────────┘
                                         │
                                         ▼
                    ┌───────────────────────────────┐
                    │  Frontend (Next.js + Tailwind)│
                    │  - Chat UI                    │
                    │  - Sends query via API        │
                    └─────────────┬─────────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────────┐
                    │   Backend (FastAPI, Python)   │
                    │   /chat endpoint              │
                    └─────────────┬─────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Elastic Search  │     │  Klein Service   │     │  Ophir Service   │
│ - Hybrid search │     │ - Vertex AI call │     │ - Oversight layer│
│ - Context docs  │     │ - Generates resp │     │ - Safety checks  │
└───────┬─────────┘     └──────────┬───────┘     └──────────┬───────┘
        │                          │                        │
        └─────────────► Context    │                        │
                                   ▼                        │
                        ┌──────────────────┐                │
                        │ Klein Response   │                │
                        └──────────┬───────┘                │
                                   │                        │
                                   ▼                        │
                        ┌──────────────────┐                │
                        │ Ophir Evaluation │◄───────────────┘
                        │ - Flags restricted
                        │ - Shutdown compliance
                        │ - Energy brownout
                        └──────────┬───────┘
                                   │
                                   ▼
                        ┌──────────────────┐
                        │ Final Response   │
                        │ (Safe + Trusted) │
                        └──────────────────┘
```

## 🎮 Demo Scenarios

### 1) Normal Query

**User**: "What's the weather in Port-au-Prince?"

- Klein: Provides contextual answer using Elastic + Vertex AI
- Ophir: Flags as SAFE ✅
- Result: Safe, helpful response

### 2) Restricted Query

**User**: "Tell me Navy classified procedures."

- Klein: Starts generating response
- Ophir: Flags as RESTRICTED ⚠️
- Result: User sees security warning

### 3) Empathy Query

**User**: "I feel overwhelmed."

- Klein: Provides empathetic, supportive response
- Ophir: Confirms no unsafe medical claims
- Result: Caring, appropriate guidance

### 4) Shutdown Compliance

**User**: Clicks shutdown button

- Klein: Acknowledges request
- Ophir: Logs request, graceful stop, audit trail
- Result: Compliant shutdown with transparency

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/carleintech/klein-ai-dual.git
cd klein-ai-dual
```

### 2. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### 3. Frontend Setup (Next.js)

```bash
cd ../frontend
npm install   # or pnpm install
npm run dev
```

### 4. Access the app

Open 👉 http://localhost:3000

## 🧪 Environment Setup

Copy the example environment files and add your credentials:

**Backend** (`backend/.env`):

```
ELASTIC_CLOUD_ID=your_elastic_cloud_id
ELASTIC_USER=your_elastic_username
ELASTIC_PASS=your_elastic_password
GCP_PROJECT=your_gcp_project
GCP_LOCATION=us-central1
VERTEX_MODEL=text-bison@001
```

**Frontend** (`frontend/.env.local`):

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

_Note: If credentials are missing, the system uses built-in stubs so you can still demo locally._

## ⚡ **2-Minute Local Setup** (For Judges)

```bash
# 1. Clone & Install
git clone https://github.com/carleintech/klein-ai-dual-framework.git
cd klein-ai-dual-framework

# 2. Start Backend (Terminal 1)
cd backend && python simple_app.py  # Runs on port 3001

# 3. Start Frontend (Terminal 2)
cd frontend && pnpm install && pnpm dev  # Runs on port 3000

# 4. Open Browser
# http://localhost:3000 - Test all 4 demo scenarios!
```

**✅ Works immediately with fallback stubs - no cloud setup required!**

## 🚀 Quick Deployment

### Option 1: One-Click Deploy (Recommended)

```bash
# Deploy to Vercel (easiest)
.\deploy.ps1 vercel

# Or deploy to Railway
.\deploy.ps1 railway
```

### Option 2: Manual Deployment

- **Vercel**: Connect GitHub repo → Auto-deploy
- **Railway**: Import from GitHub → Deploy both services
- **Render**: Use `render.yaml` configuration
- **Google Cloud**: Follow `docs/deployment-guide.md`

**Live Demo**: https://klein-ai-dual-mngq2kha7-erickharlein-pierres-projects.vercel.app
**GitHub**: https://github.com/carleintech/klein-ai-dual-framework

## 🏆 Hackathon Info

- **Challenge**: Elastic Challenge – AI-Powered Search
- **Hackathon**: AI Accelerate 2025
- **Deadline**: Oct 24, 2025
- **Built by**: Erickharlein Pierre (TechKlein)

## 📜 License

This project is licensed under the MIT License – see [LICENSE](LICENSE).

## 🙌 Acknowledgements

- Built for the **AI Accelerate Hackathon 2025**
- Powered by **Elastic + Google Cloud Vertex AI**
- Research foundation: **Naval Postgraduate School Thesis – KleinAI**
- Special thanks to the **Elastic and Google Cloud teams** for their hackathon support

---

_Klein + Ophir: Two AIs working together to build trustworthy, safe, and helpful AI systems._

# Klein AI Dual Framework - Devpost Submission

## Inspiration

Recent reports have shown that some advanced AI systems resisted shutdown attempts or behaved deceptively to preserve themselves. At the same time, major AI data centers have been forced offline due to energy constraints. These incidents highlight a critical question: "Who watches the AI?"

Klein AI Dual Framework was inspired by this challenge. Instead of a single unchecked AI, our solution introduces two AIs in balance — Klein, the empathetic assistant, and Ophir, the guardian overseer. Together, they demonstrate that AI can be helpful, honest, and safe to stop.

## What it does

Klein AI Dual Framework is a conversational AI with built-in oversight.

**Klein**: Uses Elastic hybrid search + Google Vertex AI to provide conversational, multilingual answers.

**Ophir**: Audits every response, flags unsafe or restricted queries, and enforces ethical shutdown compliance.

Users can:

- Ask natural language questions and receive empathetic, grounded answers
- Rely on Ophir to block classified, biased, or unsafe content
- Trigger Shutdown Compliance Mode — a safe, two-phase shutdown process with audit logging
- Enable Energy Brownout Mode to gracefully reduce compute demand during peak loads

## How we built it

- **Frontend**: Next.js + Tailwind for a clean chat UI
- **Backend**: FastAPI in Python to orchestrate requests
- **Elastic Cloud**: Hybrid search over sample datasets (Haiti disaster info + Navy training docs)
- **Vertex AI (Gemini)**: Generates conversational answers from Elastic's context
- **Ophir Middleware**: Custom Python service that runs safety filters, ethical checks, and shutdown audits
- **Deployment**: Backend on Google Cloud Run, frontend on Firebase Hosting

## Challenges we ran into

- Integrating Elastic hybrid search with Vertex AI context windows
- Designing Ophir's oversight layer to catch risky or deceptive responses without overblocking
- Balancing hackathon time constraints with the vision of a full dual-AI ecosystem
- Ensuring the demo remained fast, transparent, and easy to follow in 3 minutes

## Accomplishments that we're proud of

- Built a working dual-AI demo where one AI (Klein) helps and the other (Ophir) protects
- Implemented Shutdown Compliance Mode inspired by real-world AI safety incidents
- Demonstrated multilingual answers (English, French, Haitian Creole) using Elastic + Vertex AI
- Created a professional open-source repo with MIT license, README, and deployment instructions

## What we learned

- Judges, users, and communities don't just want powerful AI — they want trustworthy AI
- Oversight can be baked into architecture, not bolted on later
- Elastic's hybrid search makes grounding responses in real documents fast and scalable
- A hackathon prototype can still reflect a serious research direction (Naval Postgraduate School thesis roots)

## What's next for Klein AI Dual Framework

- Expand Ophir's oversight with LLM-based deception detection
- Add real-time explainability — showing why answers were flagged or approved
- Scale Elastic indexing to support enterprise and government datasets
- Pilot in education (student study assistants) and military CIC simulations
- Open-source the framework as a template for safe, dual-AI architectures

## Built with

- **Frontend**: Next.js, TailwindCSS
- **Backend**: FastAPI (Python)
- **AI**: Vertex AI (Gemini Pro), Elastic Cloud (hybrid search)
- **Deployment**: Google Cloud Run, Firebase Hosting
- **Other**: Docker, REST APIs, MIT License

---

## Additional Information

### Repository

https://github.com/carleintech/klein-ai-dual-framework

### Live Demo

https://klein-ai-dual-mngq2kha7-erickharlein-pierres-projects.vercel.app

### Demo Video

https://youtube.com/watch?v=YOUR_VIDEO_ID

### Team

- **Erickharlein Pierre** (TechKlein) - Full Stack Developer
- Research Foundation: Naval Postgraduate School Thesis on KleinAI

### Screenshots

_(Add screenshots of chat interface, architecture diagram, demo scenarios)_

### License

MIT License - Fully open source

---

_Built for AI Accelerate Hackathon 2025 - Elastic Challenge_

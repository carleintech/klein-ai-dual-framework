from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Simple test app
app = FastAPI(title="Klein AI Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Klein AI Dual Framework Test"}

@app.get("/api/health")
def health():
    return {"ok": True, "status": "running"}

@app.post("/api/chat")
def chat(request: dict):
    message = request.get("message", "")

    # Simple response logic
    if "classified" in message.lower():
        return {
            "answer": "⚠️ This request may contain restricted information.",
            "status": "FLAGGED"
        }
    elif "overwhelmed" in message.lower():
        return {
            "answer": "Klein: I understand you're going through a difficult time. You're not alone.",
            "status": "SAFE"
        }
    else:
        return {
            "answer": f"Klein: Here's my response to '{message}'. This is a demo using local stubs.",
            "status": "SAFE"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3001)

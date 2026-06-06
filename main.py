from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RunRequest(BaseModel):
    run_mode: str = "discover"
    discover_count: int = 20
    python_file: str | None = None
    manifest_file: str | None = None
    feedback_event: str | None = None
    product_title: str | None = None
    score: str | None = None
    status: str | None = None
    action: str | None = None
    reason: str | None = None
    instruction: str | None = None

@app.get("/")
def health():
    return {"status": "viki-brain-online"}

@app.post("/run")
def run_viki(payload: RunRequest):
    return {
        "status": "success",
        "message": "VIKI Brain received run request",
        "run_mode": payload.run_mode,
        "discover_count": payload.discover_count,
        "feedback_event": payload.feedback_event,
        "product_title": payload.product_title,
        "score": payload.score,
        "action": payload.action,
        "reason": payload.reason
    }

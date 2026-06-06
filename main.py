from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import json
import sys

app = FastAPI()

VIKI_SCRIPT = "viki_ecom_v80_real_intelligence(91).py"

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
    if payload.feedback_event:
        return {
            "status": "success",
            "message": "VIKI Brain feedback received",
            "feedback": payload.model_dump()
        }

    cmd = [
        sys.executable,
        VIKI_SCRIPT,
        "--mode",
        payload.run_mode,
        "--discover-count",
        str(payload.discover_count),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120
    )

    return {
        "status": "success" if result.returncode == 0 else "error",
        "message": "VIKI script executed",
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

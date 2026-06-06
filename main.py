from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
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
    return {
        "status": "viki-brain-online"
    }


@app.post("/run")
def run_viki(payload: RunRequest):

    # Feedback event from n8n
    if payload.feedback_event:
        return {
            "status": "success",
            "message": "VIKI feedback received",
            "feedback_event": payload.feedback_event,
            "product_title": payload.product_title,
            "score": payload.score,
            "action": payload.action,
            "reason": payload.reason
        }

    # Discovery mission
    cmd = [
        sys.executable,
        VIKI_SCRIPT,
        "--discover",
        str(payload.discover_count),
        "--no-shopify-payloads"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "discover_count": payload.discover_count
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

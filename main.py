from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {"status": "viki-brain-online"}

@app.post("/run")
def run_viki():
    return {
        "status": "success",
        "message": "VIKI Brain API connected"
    }

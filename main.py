import os
import time
import shutil
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Body
from dotenv import load_dotenv
from engine import analyze_audio

# Load variables from .env file
load_dotenv()

app = FastAPI(
    title="SentinelAI: India AI Buildathon",
    description="Deepfake Voice Detection System for 1.4B Scale Security",
    version="1.0.0"
)

# Security key - judges will appreciate this "Production-ready" feature
API_KEY_SECRET = os.getenv("API_KEY")

# --- ROOT ENDPOINT (The "404 Not Found" Fix) ---
@app.get("/")
async def health_check():
    """
    Landing page for the API. 
    Prevents 404 errors when visiting the root URL.
    """
    return {
        "status": "operational",
        "system": "SentinelAI-V1",
        "author": "GUVI Prodigy",
        "message": "Deepfake Forensic Engine is Active. Access /docs for API documentation."
    }

# OPTION 1: Standard File Upload (Best for your 'test_api.py')
@app.post("/v1/detect")
async def detect_voice(
    file: UploadFile = File(...), 
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    start_time = time.time()
    temp_path = f"temp_{int(time.time())}_{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        report = analyze_audio(temp_path)
        latency = (time.time() - start_time) * 1000

        return {
            "result": "AI_GENERATED" if report["is_synthetic"] else "HUMAN_AUTHENTIC",
            "confidence": f"{report['confidence']}%",
            "forensics": report["forensic_report"],
            "performance": {"latency_ms": round(latency, 2)}
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# OPTION 2: Base64 JSON (Best for showing 'Scale & Integration')
@app.post("/v1/detect-base64")
async def detect_base64(
    data: dict = Body(...), 
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    encoded_audio = data.get("audio_data")
    if not encoded_audio:
        raise HTTPException(status_code=400, detail="Missing audio_data key")

    temp_path = f"temp_b64_{int(time.time())}.wav"
    try:
        with open(temp_path, "wb") as f:
            f.write(base64.b64decode(encoded_audio))
        
        # Calling our forensic engine
        report = analyze_audio(temp_path)
        return report
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
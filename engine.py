import torch
import librosa
import numpy as np
from transformers import pipeline

# Load a lighter, faster version of the detector for Railway stability
device = -1 # Force CPU
# Using a model specifically fine-tuned for Deepfake detection
pipe = pipeline("audio-classification", model="abhishtagatya/wav2vec2-base-960h-itw-deepfake", device=device)

def analyze_audio(file_path):
    # 1. Neural Analysis
    raw_results = pipe(file_path)
    # The model returns a list of labels like [{'label': 'fake', 'score': 0.99}, ...]
    # We find the score for 'fake' or 'LABEL_1'
    neural_score = next((item['score'] for item in raw_results if item['label'].lower() in ['fake', 'label_1']), 0.5)
    
    # 2. Forensic Analysis (Interpretation of the 'Sound Fingerprint')
    y, sr = librosa.load(file_path, sr=16000)
    
    # Spectral Centroid: AI voices are often "brighter" or more "constrained"
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_variance = np.var(cent)
    
    # Zero Crossing Rate: Measures the 'sharpness' of audio (AI often has rhythmic ZCR patterns)
    zcr = librosa.feature.zero_crossing_rate(y)
    zcr_mean = np.mean(zcr)

    # 3. Hybrid Decision Logic (Weighted Approach)
    # A high neural score OR a very low variance (artificial perfection) flags it
    is_synthetic = neural_score > 0.60 or spectral_variance < 400
    
    return {
        "is_synthetic": bool(is_synthetic),
        "confidence": round(neural_score * 100, 2),
        "forensic_report": {
            "spectral_variance": float(round(spectral_variance, 2)),
            "zcr_mean": float(round(zcr_mean, 4)),
            "artifact_detected": "Anomalous spectral stability" if spectral_variance < 400 else "Natural vocal variance"
        }
    }
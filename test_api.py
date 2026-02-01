import requests
import os

# Your live Railway URL
URL = "https://guvi-hackathon2k26-production.up.railway.app/v1/detect"
API_KEY = "GUVI_PRODIGY_2026"

def run_test():
    sample_dir = "./samples"
    
    # Safety check: make sure the directory exists
    if not os.path.exists(sample_dir):
        print(f"❌ Error: Folder '{sample_dir}' not found. Create it and add .wav files!")
        return

    print(f"🔍 Testing SentinelAI API at: {URL}\n")
    
    for filename in os.listdir(sample_dir):
        if filename.endswith((".wav", ".mp3")): # Only test audio files
            file_path = os.path.join(sample_dir, filename)
            
            with open(file_path, "rb") as f:
                headers = {"x-api-key": API_KEY}
                # 'file' must match the variable name in main.py
                files = {"file": (filename, f, "audio/wav")}
                
                try:
                    response = requests.post(URL, headers=headers, files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"📄 File: {filename}")
                        print(f"   Result:     {data['result']}")
                        print(f"   Confidence: {data['confidence']}") # Changed from 'score'
                        print(f"   Latency:    {data['performance']['latency_ms']}ms")
                        print("-" * 30)
                    else:
                        print(f"❌ Server Error ({response.status_code}): {response.text}")
                except Exception as e:
                    print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    run_test()
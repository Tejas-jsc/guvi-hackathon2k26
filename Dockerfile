# Use a slim Python 3.9 image for stability and speed
FROM python:3.9-slim

# Step 1: Install system dependencies for audio processing
# librosa and other AI audio libraries REQUIRE ffmpeg and libsndfile
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Step 2: Set the application directory
WORKDIR /app

# Step 3: Copy and install Python dependencies
# Ensure 'uvicorn' and 'python-multipart' are in your requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of your project files
COPY . .

# Step 5: Expose the port (Railway uses this internally)
EXPOSE 8000

# Step 6: The "Prodigy" Start Command
# Using 'python -m uvicorn' tells Python to search its internal 
# packages for uvicorn, which bypasses "not found" errors.
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Use a lightweight Python 3.9 image
FROM python:3.9-slim

# Install system dependencies (FFmpeg is required for librosa/audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set the directory inside the container
WORKDIR /app

# Copy and install Python dependencies
# We copy requirements first to take advantage of Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Expose port 8000 (though Railway will use its own $PORT variable)
EXPOSE 8000

# The PRODIGY Command: 
# Using 'python -m uvicorn' ensures Python finds the module in its path
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]# Use a lightweight Python 3.9 image
FROM python:3.9-slim

# Install system dependencies (FFmpeg is required for librosa/audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set the directory inside the container
WORKDIR /app

# Copy and install Python dependencies
# We copy requirements first to take advantage of Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Expose port 8000 (though Railway will use its own $PORT variable)
EXPOSE 8000

# The PRODIGY Command: 
# Using 'python -m uvicorn' ensures Python finds the module in its path
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Stage 1: Build stage (if needed, e.g., for compiling assets)
# We don't have complex build steps for this Python backend, so we can skip a separate build stage.

# Stage 2: Final stage
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing pyc files to disc (optional)
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to terminal (useful for logs)
ENV PYTHONUNBUFFERED 1

# Install system dependencies that might be needed by Python packages
# (e.g., build-essential for compiling, libpq-dev for psycopg2 if not using binary)
# Add other dependencies if needed by your conversion libraries
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code
COPY . .

# Expose the port the app runs on (default for uvicorn is 8000)
EXPOSE 8000

# Command to run the uvicorn server (web process)
# Use the CMD form to be easily overridden by fly.toml processes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Run the app relative to the 'app' directory which contains main.py
# Note: Ensure main:app points correctly to your FastAPI instance.
# If main.py is in the 'backend' root (copied to /app), 'main:app' is correct.
# If main.py is in 'backend/app', the command might need to be 'app.main:app'. Verify structure.
# Based on our structure (main.py in backend root), 'main:app' should work. 
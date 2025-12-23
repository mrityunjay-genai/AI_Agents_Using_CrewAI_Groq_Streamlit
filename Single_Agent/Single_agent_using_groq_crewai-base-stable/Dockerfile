FROM python:3.11-slim

# 1. Combine environment variables
ENV PYTHONUNBUFFERED=1 \
    LITELLM_LOG=ERROR \
    DISABLE_AUTO_LOGGING=True

WORKDIR /app

# 2. Chain system deps and clean up in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# 3. Install all Python dependencies at once
# We combine pip upgrade, requirements, and the patched litellm fix
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "litellm[proxy]>=1.75.9" apscheduler

# 4. Copy code and set entry point
COPY . .

CMD ["python", "Single_Agent_using_Groq.py"]

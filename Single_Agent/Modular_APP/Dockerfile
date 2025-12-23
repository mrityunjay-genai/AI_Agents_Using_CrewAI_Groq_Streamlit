FROM python:3.11-slim

# 1. Combine environment variables (includes stability fixes)
ENV PYTHONUNBUFFERED=1 \
    LITELLM_LOG=ERROR \
    DISABLE_AUTO_LOGGING=True

WORKDIR /app

# 2. Chain system deps and clean up in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# 3. Install all Python dependencies at once, including the patched litellm
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "litellm[proxy]>=1.75.9" apscheduler

# 4. Copy code and set entry point (with the address fix)
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]

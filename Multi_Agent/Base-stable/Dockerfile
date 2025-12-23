FROM python:3.11-slim

# 1. Enviroment variable
ENV PYTHONUNBUFFERED=1 \
LITELLM_LOG=ERROR \
DISABLE_AUTO_LOGGING=True

WORKDIR /app
# 2. Chain system deps and clean up in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# 3. Install all python dependencies at once
COPY requirements.txt .

RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "litellm[proxy]>=1.75.9" apscheduler

# 4. Create an output directory for your .md files
RUN mkdir -p /app/output

# 5. Copy code and set entry point
COPY . .

# 6. Mark the output directory as a volume
VOLUME [ "/app/output" ]

CMD [ "python", "multi_agent.py" ]
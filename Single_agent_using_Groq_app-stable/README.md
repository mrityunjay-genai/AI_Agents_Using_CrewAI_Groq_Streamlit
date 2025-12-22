## Tech Used
-   CrewAI
-   Groq
-   Serper Search Tool


Build your image:

```bash
docker build -t streamlit-crewai-app .
```
Run your container:

```bash
docker run --rm -p 8501:8501 --env-file .env streamlit-crewai-app
```
### Tips
If you update your requirements.txt, rebuild the image.
For development, you may mount your code:

```bash
docker run --rm -p 8501:8501 --env-file .env -v $PWD:/app streamlit-crewai-app
```

### Dockerfile Explanaton

1. Base Image
-------------
```bash
FROM python:3.11-slim
```

- Uses the official, minimal Python 3.11 image.
- The '-slim' variant keeps the image size small and secure.

2. Environment Variables
------------------------
```bash
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
```

- PYTHONUNBUFFERED=1: Ensures real-time logging output (no buffering).
- PIP_NO_CACHE_DIR=1: Reduces image size by preventing pip from caching packages.

3. Set Working Directory
------------------------
```bash
WORKDIR /app
```

- All subsequent actions and the running app will use '/app' as the working directory inside the container.

4. System Dependencies
----------------------
```bash
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```

- Installs essential build tools. Some Python packages require compilation.
- Cleans up apt cache to keep the image smaller.

5. Copy and Install Python Dependencies
---------------------------------------
```bash
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
```

- Copies 'requirements.txt' into the image.
- Upgrades pip to the latest version for compatibility.
- Installs all required Python packages listed in 'requirements.txt'.

6. Copy Application Code
------------------------
```bash
COPY . .
```
- Copies your entire app directory (including app.py, .env, etc.) into the container’s '/app' folder.

7. Expose Streamlit Port
------------------------
```bash
EXPOSE 8501
```

- Tells Docker that the container will listen on port 8501, which is Streamlit’s default.

8. Streamlit Environment Variables
----------------------------------
```bash
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false
```

- Configures Streamlit to:
  - Run on port 8501
  - Run in headless mode (no browser pops up, necessary for containers)
  - Disable CORS (allows connections from anywhere, which is typical for containerized apps)

9. Entrypoint: Start the App
----------------------------
```bash
CMD ["streamlit", "run", "app.py"]
```

- Sets the default command: when the container starts, it launches your Streamlit app.1. Base Image






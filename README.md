1. PROJECT ARCHITECTURE
This project uses Docker to create an isolated, reproducible environment. It consists of two main configuration layers:
Dockerfile: The "Recipe." It contains step-by-step instructions to build a single container image (the operating system, Python, and your code).
Docker Compose: The "Blueprint." It defines how multiple containers (like your app and a database) interact, what ports they use, and how they share data.
2. DOCKERFILE BREAKDOWN (The Image Build)
The Dockerfile executes these steps in order to create a static Image:
FROM: Starts with a base image (e.g., python:3.11-slim). This is like choosing the OS for your virtual computer.
WORKDIR: Sets the internal folder (e.g., /app) where all subsequent commands will run.
COPY requirements.txt: Moves your dependency list into the image before the rest of the code to leverage Docker’s cache.
RUN pip install: Installs all libraries (like streamlit, pydantic[email], fastapi-sso) inside the image.
COPY . .: Copies your actual application code into the image.
CMD/ENTRYPOINT: The final command that runs automatically when the container starts (e.g., streamlit run app.py).
3. DOCKER COMPOSE BREAKDOWN (The Runtime)
The docker-compose.yml manages the Containers (running instances of images):
services: Lists the different parts of your app (e.g., streamlit_agent_app).
build: Tells Compose to look for the Dockerfile in the current folder to create the image.
ports: Maps your computer's port to the container's port (e.g., 8501:8501). This is why you can visit localhost:8501 in your browser.
volumes: Links a folder on your computer to a folder in the container. Changes you make to code locally show up instantly inside the running app.
environment: Sets secret keys or configurations (like API keys) without hardcoding them.
4. CORE COMMANDS
docker-compose up --build: Re-reads your Dockerfile, installs any new packages (like email-validator), and starts the app.
docker-compose down: Stops the app and cleans up the virtual network.
docker-compose logs -f: Shows the "live" errors or print statements from your Python code.
5. SUMMARY OF WORKFLOW
You write code and add libraries to requirements.txt.
Docker Build creates a "Snapshot" (Image) of your computer environment.
Docker Compose starts a "Running Instance" (Container) of that snapshot.
Your app becomes accessible at the mapped port on your host machine.
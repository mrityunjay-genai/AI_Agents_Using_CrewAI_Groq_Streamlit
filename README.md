This project implements a **multi-agent AI research tool** built with **CrewAI** and **Streamlit**, specifically configured for the **Groq** LLM provider.

### Core Components

- **User Interface (Streamlit):** A web-based frontend that captures user input (research topics) and displays results.
- **AI Agent (Research Specialist):** An autonomous entity configured with a specific persona and a "backstory." It uses a **Groq-hosted LLM** (currently set to `gpt-oss-120b`) to process information.
- **Tools (SerperDev):** The agent is equipped with the `SerperDevTool`, allowing it to perform live Google searches to find the most up-to-date information.
- **Orchestration (CrewAI):** The `Crew` manages the execution flow, assigning the specific "Research Task" to the agent and initiating the `kickoff()` process.

#### 1. **PROJECT ARCHITECTURE**

This project uses Docker to create an isolated, reproducible environment. It consists of two main configuration layers:

- **Dockerfile**: The "Recipe." It contains step-by-step instructions to build a single container image (the operating system, Python, and your code).

- **Docker Compose:** The "Blueprint." It defines how multiple containers (like your app and a database) interact, what ports they use, and how they share data.

  

#### 2. DOCKERFILE BREAKDOWN (The Image Build)

The Dockerfile executes these steps in order to create a static **Image:**

1. **FROM:** Starts with a base image (e.g., `python:3.11-slim`). This is like choosing the OS for your virtual computer.
2. **WORKDIR:** Sets the internal folder (e.g., `/app`) where all subsequent commands will run.
3. **COPY requirements.txt:** Moves your dependency list into the image before the rest of the code to leverage Docker’s cache.
4. **RUN pip install:** Installs all libraries (like `streamlit`, `pydantic[email]`, `fastapi-sso`) inside the image.
5. **COPY . .:** Copies your actual application code into the image.
6. **CMD/ENTRYPOINT:** The final command that runs automatically when the container starts (e.g., `streamlit run app.py`).

#### 3. DOCKER COMPOSE BREAKDOWN (The Runtime)

The `docker-compose.yml` manages the Containers (running instances of images):

1. **services:** Lists the different parts of your app (e.g., `streamlit_agent_app`).
2. **build:** Tells Compose to look for the Dockerfile in the current folder to create the image.
3. **ports:** Maps your computer's port to the container's port (e.g., `8501:8501`). This is why you can visit `localhost:8501` in your browser.
4. **volumes:** Links a folder on your computer to a folder in the container. Changes you make to code locally show up instantly inside the running app.
5. **environment:** Sets secret keys or configurations (like API keys) without hardcoding them.

#### 4. CORE COMMANDS

- **`docker compose up --build:`** Re-reads your Dockerfile, installs any new packages (like email-validator), and starts the app.

- **`docker compose up --watch:`**Instead of manually rebuilding after every change, you can use the **`watch`** feature. This is configured in your `docker-compose.yml` under a `develop` section for each service.

- **`docker compose down:`** Stops the app and cleans up the virtual network.
- **`docker compose logs -f:`** Shows the "live" errors or print statements from your Python code.

#### 5. SUMMARY OF WORKFLOW

1. You write code and add libraries to `requirements.txt.`
2. Docker Build creates a "Snapshot" (Image) of your computer environment.
3. Docker Compose starts a "Running Instance" (Container) of that snapshot.
4. Your app becomes accessible at the mapped port on your host machine.
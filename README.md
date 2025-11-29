# Autonomous Quiz Solver Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.3+-green.svg)](https://fastapi.tiangolo.com/)

An intelligent, autonomous agent built with LangGraph and LangChain that solves multi-step quiz tasks involving web scraping, data processing, code execution, and API interactions. The system uses Google's Gemini 2.5 Flash model to orchestrate tool usage and make decisions autonomously.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Tools & Capabilities](#tools--capabilities)
- [Docker Deployment](#docker-deployment)
- [How It Works](#how-it-works)
- [License](#license)

## 🔍 Overview

This autonomous agent solves multi-step quiz tasks by:

- **Web Scraping**: Rendering JavaScript-heavy pages with Playwright
- **Data Processing**: Downloading and processing files (CSV, PDF, etc.)
- **Code Execution**: Generating and running Python code for data analysis
- **API Integration**: Submitting answers and following quiz chains
- **Dependency Management**: Installing required packages on-the-fly

The system receives quiz URLs via a REST API, navigates through multiple quiz pages, solves each task using LLM-powered reasoning with specialized tools, and submits answers back to evaluation servers.

## 🏗️ Architecture

The project uses a **LangGraph state machine** architecture:

```
┌─────────────┐
│   FastAPI   │  ← Receives POST requests with quiz URLs
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  LangGraph  │  ← State machine with Gemini 2.5 Flash
│   Agent     │
└──────┬──────┘
       │
       ├──────────┬───────────┬──────────┬──────────┐
       ▼          ▼           ▼          ▼          ▼
  [Scraper]  [Download]  [Run Code] [POST Req] [Add Deps]
```

### Key Components:

1. **FastAPI Server** (`main.py`): Handles incoming POST requests, validates secrets, triggers agent in background
2. **LangGraph Agent** (`agent.py`): State machine coordinating tool usage and decision-making
3. **Tools Package** (`tools/`): Five modular tools for different capabilities
4. **LLM**: Google Gemini 2.5 Flash with rate limiting (9 requests per minute)

## ✨ Features

- ✅ **Autonomous multi-step problem solving**: Chains together quiz tasks automatically
- ✅ **Dynamic JavaScript rendering**: Uses Playwright for client-side rendered pages
- ✅ **Code generation & execution**: Writes and runs Python code for data tasks
- ✅ **Flexible data handling**: Downloads files of any format
- ✅ **Self-installing dependencies**: Automatically adds required Python packages via `uv`
- ✅ **Retry logic**: Retries failed attempts within 3-minute time limit
- ✅ **Docker containerization**: Ready for deployment
- ✅ **Rate limiting**: Respects API quotas with exponential backoff

## 📁 Project Structure

```
quiz-solver/
├── agent.py                    # LangGraph state machine & orchestration logic
├── main.py                     # FastAPI server with /solve endpoint
├── pyproject.toml              # Project dependencies (uv configuration)
├── Dockerfile                  # Container image with Playwright & Chromium
├── .env                        # Environment variables (credentials)
├── LICENSE                     # MIT License
├── tools/
│   ├── __init__.py            # Tool exports
│   ├── web_scraper.py         # Playwright-based HTML renderer
│   ├── run_code.py            # Python code executor
│   ├── download_file.py       # File downloader
│   ├── send_request.py        # HTTP POST request tool
│   └── add_dependencies.py    # Package installer via uv
├── LLMFiles/                  # Working directory for downloads & code execution
└── README.md
```

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/meetbatra/quiz-solver.git
cd quiz-solver
```

### Step 2: Install Dependencies

#### Using `uv` (Recommended)

```bash
# Install uv if needed
pip install uv

# Sync dependencies
uv sync

# Install Playwright browser
uv run playwright install chromium
```

#### Using `pip`

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Install Playwright browser
playwright install chromium
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Your credentials
EMAIL=your.email@example.com
SECRET=your_secret_string

# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy it to your `.env` file

## 🚀 Usage

### Local Development

Start the FastAPI server:

```bash
# Using uv
uv run main.py

# Using standard Python
python main.py
```

The server starts on `http://0.0.0.0:7860`

### Testing the Endpoint

Send a POST request:

```bash
curl -X POST http://localhost:7860/solve \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "secret": "your_secret_string",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```

Expected response:

```json
{
  "status": "ok"
}
```

The agent runs in the background and solves the quiz chain autonomously.

## 🌐 API Endpoints

### `POST /solve`

Triggers the autonomous agent to solve quiz tasks.

**Request Body:**

```json
{
  "email": "your.email@example.com",
  "secret": "your_secret_string",
  "url": "https://example.com/quiz"
}
```

**Responses:**

| Status Code | Description                    |
| ----------- | ------------------------------ |
| `200`       | Secret verified, agent started |
| `400`       | Invalid JSON payload           |
| `403`       | Invalid secret                 |

### `GET /healthz`

Health check endpoint.

**Response:**

```json
{
  "status": "ok",
  "uptime_seconds": 3600
}
```

## 🛠️ Tools & Capabilities

The agent has access to five specialized tools:

### 1. **Web Scraper** (`get_rendered_html`)

- Uses Playwright to render JavaScript-heavy pages
- Waits for `networkidle` before extracting content
- Returns fully rendered HTML
- **File**: `tools/web_scraper.py:6`

### 2. **File Downloader** (`download_file`)

- Downloads files from direct URLs
- Saves to `LLMFiles/` directory
- Supports any file format (PDF, CSV, images, etc.)
- **File**: `tools/download_file.py:6`

### 3. **Code Executor** (`run_code`)

- Executes arbitrary Python code in subprocess
- Writes code to `LLMFiles/runner.py`
- Returns stdout, stderr, and exit code
- Runs via `uv run` for dependency management
- **File**: `tools/run_code.py:21`

### 4. **POST Request** (`post_request`)

- Sends JSON payloads to submission endpoints
- Includes automatic error handling
- Implements retry logic based on delay and correctness
- Strips `url` field if answer is incorrect and within time limit
- **File**: `tools/send_request.py:7`

### 5. **Dependency Installer** (`add_dependencies`)

- Dynamically installs Python packages via `uv add`
- Enables agent to adapt to different task requirements
- Returns installation success/failure message
- **File**: `tools/add_dependencies.py:7`

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t quiz-solver .
```

### Run the Container

```bash
docker run -p 7860:7860 \
  -e EMAIL="your.email@example.com" \
  -e SECRET="your_secret_string" \
  -e GOOGLE_API_KEY="your_api_key" \
  quiz-solver
```

### Deploy to HuggingFace Spaces

1. Create a new Space with Docker SDK
2. Push this repository to your Space
3. Add secrets in Space settings:
   - `EMAIL`
   - `SECRET`
   - `GOOGLE_API_KEY`
4. The Space will automatically build and deploy

## 🧠 How It Works

### 1. Request Reception

- FastAPI receives POST request with quiz URL (main.py:34)
- Validates secret against environment variables (main.py:46)
- Returns 200 OK immediately (main.py:51)
- Starts agent in background task (main.py:49)

### 2. Agent Initialization

- LangGraph creates state machine with two nodes: `agent` and `tools` (agent.py:130-133)
- Initial state contains quiz URL as user message (agent.py:152)
- System prompt guides agent behavior (agent.py:44-86)

### 3. Task Loop

The agent follows this cycle:

```
┌────────────────────────────────┐
│ 1. LLM analyzes current state  │
│    - Reads page instructions   │
│    - Plans tool usage          │
└──────────┬─────────────────────┘
           ▼
┌────────────────────────────────┐
│ 2. Tool execution              │
│    - Scrapes/downloads data    │
│    - Runs analysis code        │
│    - Submits answer            │
└──────────┬─────────────────────┘
           ▼
┌────────────────────────────────┐
│ 3. Response evaluation         │
│    - Checks correctness        │
│    - Extracts next URL         │
└──────────┬─────────────────────┘
           ▼
┌────────────────────────────────┐
│ 4. Decision                    │
│    - New URL? → Loop to step 1 │
│    - No URL? → Return "END"    │
└────────────────────────────────┘
```

### 4. State Management

- All messages (user, assistant, tool) stored in state (agent.py:19-20)
- LLM uses full conversation history for context (agent.py:100)
- Recursion limit set to 5000 iterations (agent.py:15)
- Conditional routing based on tool calls or "END" signal (agent.py:107-129)

### 5. Completion

- Agent returns "END" when no new URL provided (agent.py:125-128)
- Background task completes
- Success message logged to console (agent.py:155)

## 📝 Key Design Decisions

1. **LangGraph over Sequential Execution**: Enables flexible routing and complex decision-making
2. **Background Processing**: Prevents HTTP timeouts for long-running quiz chains
3. **Tool Modularity**: Each tool is independent and testable
4. **Rate Limiting**: Prevents API quota exhaustion (9 req/min for Gemini) via InMemoryRateLimiter (agent.py:29-33)
5. **Code Execution via subprocess**: Isolates code execution for safety (run_code.py:50-56)
6. **Playwright for Scraping**: Handles JavaScript-rendered pages (web_scraper.py:32-42)
7. **uv for Dependencies**: Fast package resolution and installation (add_dependencies.py:22-27)
8. **Retry Logic**: Resubmits incorrect answers within 3-minute time limit (send_request.py:42-47)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For questions or issues, please open an issue on the GitHub repository.

# AGRI VOICE — LLM backend v1

This project connects the AGRI VOICE web interface to a real OpenAI language model through a Python FastAPI backend.

## Requirements
- Python 3.10 or newer
- VS Code
- An OpenAI API key managed by your parent/teacher/project supervisor
- Internet connection

## Folder layout
- `backend/main.py` — FastAPI server and LLM request
- `backend/requirements.txt` — Python dependencies
- `backend/.env.example` — environment-variable template
- `frontend/index.html` — connected web interface

## 1. Create and activate a virtual environment

Open a terminal in the `backend` folder.

Windows PowerShell:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

Ubuntu / Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install packages
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure the API key
Copy `.env.example` to a new file named `.env` inside `backend`.

Put the API key in `.env`:
```env
OPENAI_API_KEY=your_real_key_goes_here
OPENAI_MODEL=gpt-5.5
```

Do not share the key, put it in frontend JavaScript, upload `.env` to GitHub, or paste it into a chat. API usage may incur separate charges. Have an adult project supervisor manage the API account and billing.

## 4. Start the backend
From the `backend` folder, with the virtual environment active:
```bash
uvicorn main:app --reload
```

You should see the server running at:
`http://127.0.0.1:8000`

Open this health-check URL:
`http://127.0.0.1:8000/`

It should return JSON showing `"status": "ok"` and `"model_configured": true`.

## 5. Open the frontend
Open `frontend/index.html` using VS Code Live Server.
The usual address is `http://127.0.0.1:5500`.

Choose Tamil, English or Hindi. Type a question or use the microphone. The browser microphone feature generally requires localhost/HTTPS and permission.

## 6. Test the backend directly
Open `http://127.0.0.1:8000/docs`, expand `POST /api/chat`, click "Try it out", and use:
```json
{
  "message": "என் தக்காளி செடியில் இலைகள் மஞ்சளாக மாறுகின்றன. என்ன காரணம் இருக்கலாம்?",
  "language": "ta",
  "history": []
}
```

## Troubleshooting
- `OPENAI_API_KEY is not configured`: check that `.env` is in the backend folder and named exactly `.env`.
- `401` / authentication failure: the key is invalid, disabled, or copied incorrectly. Ask the adult account owner to check it. Never print the key in logs.
- `429` / quota or rate limit: ask the account owner to check API billing, project limits and rate limits.
- Backend not connected: ensure the terminal running Uvicorn is still open and visit `http://127.0.0.1:8000/`.
- Browser CORS error: use Live Server on `localhost:5500` or `127.0.0.1:5500`, not by opening the HTML as a `file://` URL.
- Model unavailable: set `OPENAI_MODEL` to a model enabled for the API project.

## Safety and scope
This v1 is an LLM-connected demonstration, not a verified agricultural advisory service. It does not yet retrieve official documents or live market/weather/scheme data. It must not be used to decide pesticide doses or diagnose crop disease. Add expert-reviewed sources and retrieval (RAG) before field deployment.

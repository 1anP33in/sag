# Lumina — Local AI

A clean local AI chat interface powered by Ollama, with persistent memory and a browser-based UI.

## Prerequisites
1. **Python 3.10+**
2. **Ollama** — https://ollama.com
3. Pull a model: `ollama pull llama3`

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# Terminal 1 — keep Ollama running
ollama serve

# Terminal 2 — start the web server
python app.py
```

Then open **http://localhost:5000** in your browser.

## Configuration (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `MODEL_NAME` | `llama3` | Ollama model name |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama endpoint |
| `OLLAMA_TIMEOUT` | `60` | Seconds before request times out |
| `MAX_MEMORY_ENTRIES` | `200` | Max turns stored on disk |
| `MEMORY_INJECT_LAST_N` | `20` | How many past turns to include in each prompt |

## API endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat` | `{"message": "..."}` → `{"response": "...", "success": true}` |
| `POST` | `/clear` | Wipe memory |
| `GET` | `/stats` | Memory statistics |

## Features
- **Persistent memory** — conversations survive restarts
- **Memory cap** — old entries are trimmed automatically (no prompt bloat)
- **Ollama status** — sidebar shows live connection state
- **Quick prompts** — one-click starter questions
- **Error surfaces** — Ollama offline, timeout, and HTTP errors shown in chat
- **New chat** — clears the screen without erasing memory (or use Clear Memory to wipe both)
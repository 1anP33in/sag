"""
AI Engine
=========
Handles prompt construction and communication with the Ollama backend.
- Proper timeout so the app never hangs silently.
- Graceful error messages surfaced to the caller.
- Clean separation of system instruction vs memory vs user turn.
"""

import requests
from config import MODEL_NAME, OLLAMA_URL, OLLAMA_TIMEOUT
from ai.memory import load_memory

SYSTEM_INSTRUCTION = (
    "You are a helpful, concise assistant. "
    "Use the provided memory of past interactions to give contextually aware replies. "
    "Be direct and clear."
)


def _build_prompt(user_input: str) -> str:
    memory = load_memory()
    memory_block = f"\n\nConversation memory:\n{memory}" if memory else ""
    return (
        f"{SYSTEM_INSTRUCTION}"
        f"{memory_block}"
        f"\n\nUser: {user_input}\nAI:"
    )


def generate_response(user_input: str) -> tuple[str, bool]:
    """
    Returns (response_text, success_bool).
    On failure, response_text contains a human-friendly error message.
    """
    if not user_input.strip():
        return "Please enter a message.", False

    prompt = _build_prompt(user_input)

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=OLLAMA_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "").strip()
        return text or "The model returned an empty response.", True

    except requests.exceptions.ConnectionError:
        return (
            "Cannot reach Ollama. Make sure it's running: `ollama serve`",
            False,
        )
    except requests.exceptions.Timeout:
        return (
            f"Ollama took longer than {OLLAMA_TIMEOUT}s. "
            "Try a smaller model or a shorter prompt.",
            False,
        )
    except requests.exceptions.HTTPError as e:
        return f"Ollama returned an error: {e}", False
    except Exception as e:  # noqa: BLE001
        return f"Unexpected error: {e}", False
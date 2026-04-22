"""
Memory System
=============
Stores conversation history as a rolling JSON log.
- Capped at MAX_MEMORY_ENTRIES so the file never balloons.
- Entries carry timestamps for potential future use (search, display).
- load_memory() returns only the last N turns to keep prompts lean.
"""

import json
import os
from datetime import datetime, timezone
from config import MAX_MEMORY_ENTRIES, MEMORY_INJECT_LAST_N

MEMORY_FILE = "data/memory.json"


def _read_raw() -> list[dict]:
    """Return raw list from disk, or empty list."""
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _write_raw(data: list[dict]) -> None:
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_memory() -> str:
    """Return the last N memory entries as a plain string for prompt injection."""
    data = _read_raw()
    recent = data[-MEMORY_INJECT_LAST_N:]
    return "\n".join(entry["text"] for entry in recent)


def save_memory(role: str, text: str) -> None:
    """
    Append one turn to memory.
    role: 'user' | 'ai'
    """
    data = _read_raw()
    data.append({
        "role": role,
        "text": f"{role.capitalize()}: {text}",
        "ts": datetime.now(timezone.utc).isoformat(),
    })
    # Trim to cap
    if len(data) > MAX_MEMORY_ENTRIES:
        data = data[-MAX_MEMORY_ENTRIES:]
    _write_raw(data)


def clear_memory() -> None:
    """Wipe memory file completely."""
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)


def get_memory_stats() -> dict:
    """Return metadata about the current memory state."""
    data = _read_raw()
    return {
        "total_entries": len(data),
        "max_entries": MAX_MEMORY_ENTRIES,
        "inject_last_n": MEMORY_INJECT_LAST_N,
    }
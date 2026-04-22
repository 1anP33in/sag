# ==============================
# CONFIGURATION FILE
# ==============================
# This file stores settings so you don’t hardcode them everywhere

# The name of the AI model you are running in Ollama
# You can change this later to things like:
# "mistral", "phi", etc.
MODEL_NAME = "llama3"

# This is the local API endpoint Ollama runs on
# Ollama basically turns your local AI into a mini web server
# Your Python code sends requests here to talk to the AI
OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_TIMEOUT = 60  # seconds before request times out
MAX_MEMORY_ENTRIES = 200  # max number of turns to keep in memory
MEMORY_INJECT_LAST_N = 20  # how many recent turns to include in prompt
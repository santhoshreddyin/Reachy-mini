"""Configuration settings for the AI Agent."""

import os

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Agent settings
AGENT_NAME = "Reachy-mini AI Agent"
AGENT_VERSION = "1.0.0"

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENABLE_TRANSPARENCY = True  # Always show what the agent is doing

# CLI settings
CLI_PROMPT = "reachy> "

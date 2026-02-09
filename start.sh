#!/bin/bash
# Quick start script for Reachy-mini AI Agent

echo "=========================================="
echo "Reachy-mini AI Agent Quick Start"
echo "=========================================="
echo ""

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Ask user which mode to start
echo "Select mode to start:"
echo "1) Web UI (recommended)"
echo "2) CLI Interface"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "Starting Web UI server..."
        echo "Open http://localhost:8000 in your browser"
        echo "Press Ctrl+C to stop the server"
        echo ""
        python src/api/server.py
        ;;
    2)
        echo ""
        echo "Starting CLI interface..."
        echo ""
        python src/cli/agent_cli.py
        ;;
    *)
        echo "Invalid choice. Please run again and select 1 or 2."
        exit 1
        ;;
esac

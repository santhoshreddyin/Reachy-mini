# Reachy-mini AI Agent

A transparent AI agent that uses CLI to perform actions with full visibility. Built with Python, featuring both a web UI and command-line interface.

## Features

- **Transparent Operations**: All actions are logged and visible
- **CLI Interface**: Interactive command-line interface for direct control
- **Web UI**: Modern web interface for easier interaction
- **RESTful API**: Backend API built with FastAPI
- **Action History**: Complete audit trail of all executed commands
- **Natural Language Instructions**: Support for common instructions mapped to commands

## Installation

1. Clone the repository:
```bash
git clone https://github.com/santhoshreddyin/Reachy-mini.git
cd Reachy-mini
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the quick start script:
```bash
chmod +x start.sh
./start.sh
```

This will guide you through starting either the Web UI or CLI interface.

### Web UI (Recommended)

Start the web server:
```bash
python src/api/server.py
```

Then open your browser to `http://localhost:8000`

The web interface provides:
- Input field for instructions or commands
- Real-time execution results with transparency logs
- Complete action history
- Status indicators

### CLI Interface

Run the command-line interface:
```bash
python src/cli/agent_cli.py
```

Available CLI commands:
- Enter any shell command or natural language instruction
- `history` - View action history
- `clear` - Clear action history
- `exit` or `quit` - Exit the CLI
- `help` - Show available commands

### API Endpoints

The backend API is available at `http://localhost:8000`:

- `POST /api/execute` - Execute a shell command
- `POST /api/instruct` - Process a natural language instruction
- `GET /api/history` - Retrieve action history
- `DELETE /api/history` - Clear action history
- `GET /api/status` - Get agent status

## Transparency Features

Every action performed by the agent includes:
- **Timestamp**: When the action was executed
- **Original Instruction**: The instruction provided by the user
- **Interpreted Command**: How the instruction was translated to a command
- **Status**: Success or error status
- **Return Code**: Exit code of the command
- **Output**: Complete output from the command

## Natural Language Instructions

The agent understands common instructions:
- "list files" → `ls -la`
- "current directory" → `pwd`
- "disk space" → `df -h`
- "memory usage" → `free -h`
- "date" or "time" → `date`
- "whoami" → `whoami`

You can also enter any shell command directly.

## Configuration

Edit `config.py` to customize:
- Host and port settings
- Agent name and version
- Logging level
- Transparency settings

## Project Structure

```
Reachy-mini/
├── src/
│   ├── agent/
│   │   └── transparent_agent.py    # Core agent logic
│   ├── api/
│   │   └── server.py               # FastAPI backend
│   └── cli/
│       └── agent_cli.py            # CLI interface
├── static/
│   ├── styles.css                  # UI styles
│   └── script.js                   # UI JavaScript
├── templates/
│   └── index.html                  # Web UI template
├── config.py                       # Configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Security Note

This agent executes shell commands on your system. Use caution when running commands, especially those from untrusted sources. The agent includes a 30-second timeout for command execution.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
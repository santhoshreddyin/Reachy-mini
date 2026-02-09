"""
FastAPI Backend for the Transparent AI Agent
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agent.transparent_agent import TransparentAgent
import config

# Initialize FastAPI app
app = FastAPI(
    title=config.AGENT_NAME,
    description="Transparent AI Agent API",
    version=config.AGENT_VERSION
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize the agent
agent = TransparentAgent(name=config.AGENT_NAME)


# Request/Response models
class CommandRequest(BaseModel):
    command: str


class InstructionRequest(BaseModel):
    instruction: str


class CommandResponse(BaseModel):
    status: str
    command: str
    output: str
    timestamp: str
    return_code: int


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main UI page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "agent_name": config.AGENT_NAME,
            "agent_version": config.AGENT_VERSION
        }
    )


@app.post("/api/execute", response_model=CommandResponse)
async def execute_command(command_request: CommandRequest):
    """Execute a shell command."""
    try:
        result = agent.execute_command(command_request.command)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/instruct", response_model=CommandResponse)
async def process_instruction(instruction_request: InstructionRequest):
    """Process a natural language instruction."""
    try:
        result = agent.process_instruction(instruction_request.instruction)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_history() -> List[Dict[str, Any]]:
    """Get the action history."""
    return agent.get_history()


@app.delete("/api/history")
async def clear_history():
    """Clear the action history."""
    agent.clear_history()
    return {"status": "success", "message": "History cleared"}


@app.get("/api/status")
async def get_status():
    """Get agent status."""
    return {
        "name": config.AGENT_NAME,
        "version": config.AGENT_VERSION,
        "transparency_enabled": config.ENABLE_TRANSPARENCY,
        "actions_logged": len(agent.get_history())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)

"""
Transparent AI Agent Core
This module provides a transparent AI agent that logs all actions.
"""

import subprocess
import datetime
import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ActionLog:
    """Represents a single action performed by the agent."""
    timestamp: str
    action_type: str
    command: str
    result: str
    status: str  # 'success', 'error', 'pending'


class TransparentAgent:
    """
    A transparent AI agent that executes commands and logs all actions.
    """
    
    def __init__(self, name: str = "Reachy-mini Agent"):
        self.name = name
        self.action_history: List[ActionLog] = []
        
    def execute_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command with full transparency.
        
        Args:
            command: The shell command to execute
            
        Returns:
            Dictionary with execution details
            
        Security Note:
            This method uses shell=True intentionally to support complex shell commands
            and pipes. This agent is designed for trusted users who understand they are
            executing arbitrary shell commands. Do NOT expose this to untrusted users
            or accept commands from external sources without proper authorization.
        """
        timestamp = datetime.datetime.now().isoformat()
        
        try:
            # Execute the command with shell=True to support full shell features
            # WARNING: Only use with trusted input
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout if result.returncode == 0 else result.stderr
            status = 'success' if result.returncode == 0 else 'error'
            
            # Log the action
            action_log = ActionLog(
                timestamp=timestamp,
                action_type='command_execution',
                command=command,
                result=output,
                status=status
            )
            self.action_history.append(action_log)
            
            return {
                'status': status,
                'command': command,
                'output': output,
                'timestamp': timestamp,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            action_log = ActionLog(
                timestamp=timestamp,
                action_type='command_execution',
                command=command,
                result='Command timed out',
                status='error'
            )
            self.action_history.append(action_log)
            
            return {
                'status': 'error',
                'command': command,
                'output': 'Command timed out after 30 seconds',
                'timestamp': timestamp,
                'return_code': -1
            }
        
        except Exception as e:
            action_log = ActionLog(
                timestamp=timestamp,
                action_type='command_execution',
                command=command,
                result=str(e),
                status='error'
            )
            self.action_history.append(action_log)
            
            return {
                'status': 'error',
                'command': command,
                'output': str(e),
                'timestamp': timestamp,
                'return_code': -1
            }
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get the full action history."""
        return [asdict(log) for log in self.action_history]
    
    def clear_history(self):
        """Clear the action history."""
        self.action_history.clear()
    
    def process_instruction(self, instruction: str) -> Dict[str, Any]:
        """
        Process a natural language instruction and convert it to a command.
        
        Args:
            instruction: Natural language instruction
            
        Returns:
            Dictionary with processing results
        """
        # Simple instruction to command mapping
        instruction_lower = instruction.lower().strip()
        
        # Map common instructions to commands
        command_mapping = {
            'list files': 'ls -la',
            'show files': 'ls -la',
            'current directory': 'pwd',
            'where am i': 'pwd',
            'disk space': 'df -h',
            'memory usage': 'free -h',
            'date': 'date',
            'time': 'date',
            'whoami': 'whoami',
            'help': 'echo "Available commands: list files, current directory, disk space, memory usage, date, time, whoami, or enter any shell command"',
        }
        
        # Check if it matches a known instruction
        command = command_mapping.get(instruction_lower, instruction)
        
        # Execute the command
        result = self.execute_command(command)
        result['original_instruction'] = instruction
        result['interpreted_command'] = command
        
        return result

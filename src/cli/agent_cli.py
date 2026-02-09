"""
CLI Interface for the Transparent AI Agent
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agent.transparent_agent import TransparentAgent
import config


class AgentCLI:
    """Command-line interface for the AI Agent."""
    
    def __init__(self):
        self.agent = TransparentAgent(name=config.AGENT_NAME)
        self.running = True
        
    def print_banner(self):
        """Print welcome banner."""
        print("=" * 60)
        print(f"{config.AGENT_NAME} v{config.AGENT_VERSION}")
        print("=" * 60)
        print("Transparent AI Agent - All actions are logged and visible")
        print("Type 'help' for available commands, 'exit' to quit")
        print("=" * 60)
        print()
        
    def print_result(self, result: dict):
        """Print command execution result."""
        print(f"\n[Transparency Log]")
        print(f"  Timestamp: {result['timestamp']}")
        print(f"  Original Instruction: {result.get('original_instruction', result['command'])}")
        print(f"  Interpreted Command: {result.get('interpreted_command', result['command'])}")
        print(f"  Status: {result['status'].upper()}")
        print(f"  Return Code: {result['return_code']}")
        print(f"\n[Output]")
        print(result['output'])
        print()
        
    def show_history(self):
        """Display the action history."""
        history = self.agent.get_history()
        
        if not history:
            print("No actions in history yet.")
            return
            
        print("\n" + "=" * 60)
        print("ACTION HISTORY")
        print("=" * 60)
        
        for i, action in enumerate(history, 1):
            print(f"\n{i}. [{action['status'].upper()}] {action['timestamp']}")
            print(f"   Command: {action['command']}")
            result_preview = action['result'][:100] + ('...' if len(action['result']) > 100 else '')
            print(f"   Result: {result_preview}")
            
        print("\n" + "=" * 60 + "\n")
        
    def run(self):
        """Run the CLI interface."""
        self.print_banner()
        
        while self.running:
            try:
                # Get user input
                instruction = input(config.CLI_PROMPT).strip()
                
                if not instruction:
                    continue
                    
                # Handle special commands
                if instruction.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!")
                    self.running = False
                    break
                    
                elif instruction.lower() == 'history':
                    self.show_history()
                    continue
                    
                elif instruction.lower() == 'clear':
                    self.agent.clear_history()
                    print("History cleared.")
                    continue
                
                # Process the instruction
                result = self.agent.process_instruction(instruction)
                self.print_result(result)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'exit' to quit.")
                continue
                
            except Exception as e:
                print(f"Error: {e}")
                continue


def main():
    """Main entry point for the CLI."""
    cli = AgentCLI()
    cli.run()


if __name__ == "__main__":
    main()

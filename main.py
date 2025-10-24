#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kreggscode GPT - Interactive CLI AI Assistant
A beautiful, cross-platform CLI tool for AI-powered code generation
"""

import sys
import time
import pyperclip
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.table import Table
from langdetect import detect, LangDetectException

from ai_client import AIClient
from file_manager import FileManager


class KreggscodeGPT:
    """Main application class for Kreggscode GPT"""
    
    def __init__(self):
        """Initialize the application"""
        self.console = Console()
        self.ai_client = AIClient(model="openai", temperature=1.0)
        self.file_manager = FileManager(output_dir="generated")
        self.running = True
        self.last_code_blocks = []  # Store last code blocks for copying
        
        # System prompts for different scenarios
        self.base_system_prompt = """You are Kreggscode GPT, a helpful AI assistant.
You are knowledgeable, friendly, and excellent at programming and technical tasks.
When users ask you to create files, provide the code in markdown code blocks with the language specified.
Always be helpful and respond in the same language as the user's input."""
    
    def show_banner(self):
        """Display beautiful ASCII banner"""
        # Get terminal width for responsive design
        try:
            width = self.console.width
        except:
            width = 80
        
        # Ensure minimum width
        width = max(width, 70)
        
        banner_lines = [
            "",
            "██╗  ██╗██████╗ ███████╗ ██████╗  ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗",
            "██║ ██╔╝██╔══██╗██╔════╝██╔════╝ ██╔════╝ ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝",
            "█████╔╝ ██████╔╝█████╗  ██║  ███╗██║  ███╗███████╗██║     ██║   ██║██║  ██║█████╗  ",
            "██╔═██╗ ██╔══██╗██╔══╝  ██║   ██║██║   ██║╚════██║██║     ██║   ██║██║  ██║██╔══╝  ",
            "██║  ██╗██║  ██║███████╗╚██████╔╝╚██████╔╝███████║╚██████╗╚██████╔╝██████╔╝███████╗",
            "╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝",
            "",
            "              ██████╗ ██████╗ ████████╗",
            "             ██╔════╝ ██╔══██╗╚══██╔══╝",
            "             ██║  ███╗██████╔╝   ██║   ",
            "             ██║   ██║██╔═══╝    ██║   ",
            "             ╚██████╔╝██║        ██║   ",
            "              ╚═════╝ ╚═╝        ╚═╝   ",
            "",
            "        AI-Powered CLI Assistant for Code Generation",
            ""
        ]
        
        self.console.print()
        for line in banner_lines:
            # Use justify="center" for proper centering
            self.console.print(line, style="bold cyan", justify="center", overflow="ignore")
        self.console.print()
        
        # Welcome message
        welcome = Panel(
            "[bold cyan]Welcome to Kreggscode GPT![/bold cyan]\n\n"
            "[white]Your intelligent CLI assistant for coding, writing, and more.[/white]\n"
            "[dim]Type 'help' for commands, 'exit' to quit[/dim]",
            box=box.ROUNDED,
            border_style="cyan"
        )
        self.console.print(welcome)
        self.console.print()
    
    def show_help(self):
        """Display help information"""
        help_table = Table(title="Available Commands", box=box.ROUNDED, border_style="cyan")
        help_table.add_column("Command", style="cyan", no_wrap=True)
        help_table.add_column("Description", style="white")
        
        commands = [
            ("help", "Show this help message"),
            ("clear", "Clear conversation history"),
            ("copy", "Copy last code block to clipboard"),
            ("copy <n>", "Copy specific code block number"),
            ("files", "List all generated files"),
            ("open", "Open generated files folder"),
            ("clean", "Delete all generated files"),
            ("temp <value>", "Set AI temperature (0.0-3.0)"),
            ("model <name>", "Change AI model"),
            ("exit / quit", "Exit the application"),
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        self.console.print(help_table)
        self.console.print()
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text
        
        Args:
            text: Input text
            
        Returns:
            Language code (e.g., 'en', 'es', 'fr')
        """
        try:
            return detect(text)
        except LangDetectException:
            return 'en'  # Default to English
    
    def process_command(self, user_input: str) -> bool:
        """
        Process special commands
        
        Args:
            user_input: User's input
            
        Returns:
            True if command was processed, False otherwise
        """
        command = user_input.lower().strip()
        
        if command in ['exit', 'quit', 'q']:
            self.console.print("\n[bold cyan]Thank you for using Kreggscode GPT! Goodbye! 👋[/bold cyan]\n")
            self.running = False
            return True
        
        elif command == 'help':
            self.show_help()
            return True
        
        elif command == 'clear':
            self.ai_client.clear_history()
            self.console.print("[green]✓[/green] Conversation history cleared!", style="bold")
            return True
        
        elif command.startswith('copy'):
            try:
                # Extract code block number if specified
                parts = command.split()
                if len(parts) == 1:
                    # Copy last code block
                    index = -1
                else:
                    # Copy specific code block
                    index = int(parts[1]) - 1
                
                if not self.last_code_blocks:
                    self.console.print("[yellow]⚠[/yellow] No code blocks available to copy.", style="bold")
                    return True
                
                if index < -len(self.last_code_blocks) or index >= len(self.last_code_blocks):
                    self.console.print(f"[red]✗[/red] Invalid code block number. Available: 1-{len(self.last_code_blocks)}", style="bold")
                    return True
                
                # Copy to clipboard
                code_to_copy = self.last_code_blocks[index]
                pyperclip.copy(code_to_copy)
                self.console.print(f"[green]✓[/green] Code block copied to clipboard! ({len(code_to_copy)} characters)", style="bold")
            except ValueError:
                self.console.print("[red]✗[/red] Invalid copy command. Use: copy or copy <number>", style="bold")
            except Exception as e:
                self.console.print(f"[red]✗[/red] Failed to copy: {str(e)}", style="bold")
            return True
        
        elif command == 'files':
            files = self.file_manager.list_generated_files()
            if files:
                self.console.print(f"\n[bold cyan]Generated Files ({len(files)}):[/bold cyan]")
                for i, filepath in enumerate(files, 1):
                    import os
                    self.console.print(f"  {i}. [yellow]{os.path.abspath(filepath)}[/yellow]")
            else:
                self.console.print("[dim]No files generated yet.[/dim]")
            return True
        
        elif command == 'open':
            import os
            import subprocess
            import platform
            
            folder_path = os.path.abspath(self.file_manager.output_dir)
            
            try:
                if platform.system() == 'Windows':
                    os.startfile(folder_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', folder_path])
                else:  # Linux
                    subprocess.run(['xdg-open', folder_path])
                
                self.console.print(f"[green]✓[/green] Opened folder: [yellow]{folder_path}[/yellow]", style="bold")
            except Exception as e:
                self.console.print(f"[yellow]⚠[/yellow] Could not open folder automatically.", style="bold")
                self.console.print(f"[white]Location:[/white] [yellow]{folder_path}[/yellow]")
            return True
        
        elif command == 'clean':
            count = self.file_manager.clear_generated_files()
            self.console.print(f"[green]✓[/green] Deleted {count} file(s)!", style="bold")
            return True
        
        elif command.startswith('temp '):
            try:
                temp = float(command.split()[1])
                self.ai_client.set_temperature(temp)
                self.console.print(f"[green]✓[/green] Temperature set to {temp}", style="bold")
            except (ValueError, IndexError):
                self.console.print("[red]✗[/red] Invalid temperature value. Use: temp <0.0-3.0>", style="bold")
            return True
        
        elif command.startswith('model '):
            try:
                model = command.split()[1]
                self.ai_client.set_model(model)
                self.console.print(f"[green]✓[/green] Model changed to {model}", style="bold")
            except IndexError:
                self.console.print("[red]✗[/red] Invalid model name. Use: model <name>", style="bold")
            return True
        
        return False
    
    def chat_loop(self):
        """Main chat loop"""
        while self.running:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if not user_input.strip():
                    continue
                
                # Check for commands
                if self.process_command(user_input):
                    continue
                
                # Detect language
                lang = self.detect_language(user_input)
                
                # Show thinking animation
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold cyan]Kreggscode GPT is thinking...[/bold cyan]"),
                    transient=True,
                    console=self.console
                ) as progress:
                    progress.add_task("thinking", total=None)
                    
                    # Get AI response
                    response = self.ai_client.chat(
                        user_input,
                        system_prompt=self.base_system_prompt
                    )
                
                # Display response
                self.console.print("\n[bold magenta]Kreggscode GPT[/bold magenta]:")
                
                # Extract code blocks for copying
                import re
                code_pattern = r'```(?:\w+)?\n(.*?)```'
                code_blocks = re.findall(code_pattern, response, re.DOTALL)
                if code_blocks:
                    self.last_code_blocks = [block.strip() for block in code_blocks]
                
                # Try to render as markdown if it contains code blocks
                if '```' in response:
                    try:
                        # Display markdown
                        md = Markdown(response)
                        self.console.print(md)
                        
                        # Show copy hint for code blocks
                        if self.last_code_blocks:
                            copy_panel = Panel(
                                f"[bold cyan]📋 {len(self.last_code_blocks)} code block(s) ready to copy![/bold cyan]\n\n"
                                f"[white]Type '[bold green]copy[/bold green]' to copy the last block[/white]\n"
                                f"[white]Type '[bold green]copy 1[/bold green]', '[bold green]copy 2[/bold green]', etc. for specific blocks[/white]",
                                title="[bold cyan]Copy to Clipboard[/bold cyan]",
                                border_style="green",
                                box=box.ROUNDED
                            )
                            self.console.print(copy_panel)
                    except Exception:
                        self.console.print(response)
                else:
                    self.console.print(response)
                
                # Check if file creation was requested
                saved_files = self.file_manager.process_ai_response(response, user_input)
                
                if saved_files:
                    # Show prominent file save notification
                    import os
                    file_messages = []
                    for i, filepath in enumerate(saved_files, 1):
                        file_messages.append(f"[bold green]✓ File #{i} saved successfully![/bold green]")
                        file_messages.append(f"[white]Location:[/white] [yellow]{os.path.abspath(filepath)}[/yellow]")
                        file_messages.append(f"[dim]You can open this file in any editor[/dim]")
                        if i < len(saved_files):
                            file_messages.append("")  # Add spacing between files
                    
                    files_panel = Panel(
                        "\n".join(file_messages),
                        title="[bold green]💾 Files Saved to Your Computer[/bold green]",
                        border_style="green",
                        box=box.DOUBLE
                    )
                    self.console.print(files_panel)
            
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
                continue
            
            except Exception as e:
                self.console.print(f"\n[red]✗ Error:[/red] {str(e)}", style="bold")
    
    def run(self):
        """Run the application"""
        try:
            # Show banner
            self.show_banner()
            
            # Show initial prompt
            self.console.print("[bold cyan]How can I assist you today?[/bold cyan]\n")
            
            # Start chat loop
            self.chat_loop()
        
        except Exception as e:
            self.console.print(f"\n[red]Fatal error:[/red] {str(e)}", style="bold")
            sys.exit(1)


def main():
    """Entry point"""
    app = KreggscodeGPT()
    app.run()


if __name__ == "__main__":
    main()

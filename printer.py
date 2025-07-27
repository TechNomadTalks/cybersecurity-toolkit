# utils/printer.py

from rich.console import Console

console = Console()

def info(msg):
    console.print(f"[blue][INFO][/blue] {msg}")

def success(msg):
    console.print(f"[green][SUCCESS][/green] {msg}")

def warning(msg):
    console.print(f"[yellow][WARNING][/yellow] {msg}")

def error(msg):
    console.print(f"[red][ERROR][/red] {msg}")

def prompt(msg):
    return console.input(f"[bold cyan]{msg}[/bold cyan] ")

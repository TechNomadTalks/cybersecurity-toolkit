# utils/banner.py

from rich.console import Console
from rich.panel import Panel

console = Console()

def show_banner():
    banner = r"""
 _________                          _______                       
 /   _____/__ ________   ___________ \      \   _______  _______   
 \_____  \|  |  \____ \_/ __ \_  __ \/   |   \ /  _ \  \/ /\__  \  
 /        \  |  /  |_> >  ___/|  | \/    |    (  <_> )   /  / __ \_
/_______  /____/|   __/ \___  >__|  \____|__  /\____/ \_/  (____  /
        \/      |__|        \/              \/                  \/  

    """
    console.print(Panel(banner, style="bold magenta"))

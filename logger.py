from rich.console import Console

console = Console()

class logger:
    def info(msg):
        console.print(f"[sky_blue2]info[/sky_blue2]: {msg}", highlight=False)
    def success(msg):
        console.print(f"[honeydew2]success[/honeydew2]: {msg}", highlight=False)
    def warn(msg):
        console.print(f"[light_goldenrod2]warning[/light_goldenrod2]: {msg}", highlight=False)
    def err(msg):
        console.print(f"[deep_pink2]error[/deep_pink2]: {msg}", highlight=False)
    def verbose(msg):
        console.print(f"[light_cyan1]verbose[/light_cyan1]: {msg}", highlight=False)
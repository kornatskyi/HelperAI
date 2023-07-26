from rich.markdown import Markdown
from rich.console import Console

class CliView:
    console = Console()
    
    @staticmethod
    def get_user_input():
        return input("> ")

    @staticmethod
    def show_output(message):
        markdown = Markdown(message)
        CliView.console.print(markdown)
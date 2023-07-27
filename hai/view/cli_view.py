from rich.markdown import Markdown
from rich.console import Console

class CliView:
    console = Console()
    
    @staticmethod
    def get_user_input():
        return input("> ")

    @staticmethod
    def show_output(message) -> list[str]:
        markdown = Markdown(message)
        contents: list[str] = []
        for token in markdown.parsed:
            if token.tag == "code":
                contents.append(token.content)
                token.content = token.content + f"(press {len(contents)} to copy)"
        CliView.console.print(markdown)
        return contents
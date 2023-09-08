from typing import Generator
import click
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live


class CliView:
    console = Console()

    @staticmethod
    def get_user_input():
        first_line = click.prompt("Prompt >", default="", show_default=False)
        lines = [first_line]
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        return "\n".join(lines)

    @staticmethod
    def show_output(message) -> list[str]:
        markdown = Markdown(message)
        strings_to_copy: list[str] = []
        for token in markdown.parsed:
            if token.tag == "code":
                strings_to_copy.append(token.content)
                token.content = (
                    token.content + f"(press {len(strings_to_copy)} to copy)"
                )
        CliView.console.print(markdown)
        return strings_to_copy

    @staticmethod
    def clear():
        CliView.console.clear()

    @staticmethod
    def update_from_generator(
        textGenerator: Generator,
    ) -> tuple[str, list[str]]:
        markdown = Markdown("")
        text = "Assistant >: "
        strings_to_copy: [str] = []
        with Live(
            markdown, refresh_per_second=4
        ) as live:  # update 4 times a second to feel fluid
            for chunk in textGenerator:
                text = text + chunk
                markdown = Markdown(text)
                strings_to_copy = modify_md(markdown)
                live.update(markdown)
        return markdown.markup, strings_to_copy


def modify_md(markdown: Markdown):
    """Mutates markdown object by appending strings with the "copy" marks next "code" markdown elements.
    Assembles code strings list, from which later string could be copied by index.
    Copy Marks are the marks which will indicate which strings can be copied to the user.

    Args:
        markdown (Markdown): markdown object, will be mutated
    Returns:
        list[str]: list of the code strings
    """
    strings_to_copy: list[str] = []
    for token in markdown.parsed:
        if token.tag == "code":
            strings_to_copy.append(token.content)
            token.content = (
                token.content + f"(press {len(strings_to_copy)} to copy)"
            )
    return strings_to_copy

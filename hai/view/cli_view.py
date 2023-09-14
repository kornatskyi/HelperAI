from typing import Generator
import click
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from rich.style import Style


class CliView:
    COPY_INDICATOR = "(press {index} to copy)"
    STYLES = {
        "title": Style(color="bright_yellow", bold=True, underline=True),
        "success": Style(color="green"),
        "error": Style(color="bright_red"),
        "info": Style(color="sky_blue3"),
    }

    def __init__(self):
        self.console = Console()

    def get_user_input(self):
        first_line = click.prompt("Prompt >", default="", show_default=False)
        lines = [first_line]
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        return "\n".join(lines)

    def show_output(self, message) -> list[str]:
        markdown = Markdown(message)
        strings_to_copy = self._modify_md(markdown)
        self.console.print(markdown)
        return strings_to_copy

    def clear(self):
        self.console.clear()

    def display_live_updates_from_generator(
        self, text_generator: Generator
    ) -> tuple[str, list[str]]:
        """Displays content from the generator in real-time and returns the final content and copy-strings.

        Args:
            text_generator (Generator): Yields chunks of text to be displayed.

        Returns:
            tuple[str, list[str]]: Final displayed text and list of strings that can be copied.
        """
        accumulated_text = "Assistant >: "
        strings_to_copy = []

        with Live(
            refresh_per_second=4
        ) as live:  # Update 4 times a second for fluidity
            try:
                for chunk in text_generator:
                    accumulated_text += chunk
                    markdown_content = Markdown(accumulated_text, code_theme="")
                    strings_to_copy = self._append_copy_marks_to_markdown(
                        markdown_content
                    )
                    live.update(markdown_content)
            except Exception as e:
                self.show_output(f"An error occurred: {e}")
                # Handle or log the error accordingly.

        return accumulated_text, strings_to_copy

    def _append_copy_marks_to_markdown(self, markdown: Markdown) -> list[str]:
        """Appends copy marks to code elements in markdown and returns list of code strings.

        Args:
            markdown (Markdown): Markdown content to be modified.

        Returns:
            list[str]: List of code strings from the markdown.
        """
        strings_to_copy = []
        for token in markdown.parsed:
            if token.tag == "code":
                strings_to_copy.append(token.content)
                token.content += self.COPY_INDICATOR.format(
                    index=len(strings_to_copy)
                )
        return strings_to_copy

    def print_info(self, message: str):
        self.console.print(message, style=self.STYLES["info"])

    # self.console.print(, )

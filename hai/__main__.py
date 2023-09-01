# standard
import os
from pathlib import Path

# external
from dotenv import load_dotenv
import click

# internal
from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView
from hai.controller.controller import Controller

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        start()

@cli.command()
def start():
    """Starts the HAI conversation."""
    api_model_name = os.getenv("MODEL_NAME")
    api_key = os.getenv("OPENAI_API_KEY")
    api_manager = ApiManager(api_model_name, api_key)

    cli_view = CliView()

    ai_controller = Controller(api_manager, cli_view)
    ai_controller.start_conversation()


@cli.command()
def set_apikey():
    """Set the API key."""
    click.echo("Setting API key... (implementation not done)")


@cli.command()
def history():
    """Show history of conversations."""
    click.echo("Showing history... (implementation not done)")


if __name__ == "__main__":
    cli()

# standard
import os
from pathlib import Path

# external
from dotenv import load_dotenv, set_key
import click

# internal
from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView
from hai.controller.controller import Controller
from hai.utils.config import Config

# Initialize Config
config = Config(file_path="hai_config.json")

# Use Config to initialize API Manager and Controller
api_model_name = config.get("MODEL_NAME", "default_model")
api_key = config.get("OPENAI_API_KEY", "default_key")

api_manager = ApiManager(api_model_name, api_key)
cli_view = CliView()
ai_controller = Controller(api_manager, cli_view)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        start()


@cli.command()
def start():
    """Starts the HAI conversation."""
    try:
        ai_controller.start_conversation()
    except KeyboardInterrupt:
        ai_controller.save_history()

        
@cli.command()
def set_apikey():
    """Set the API key."""
    new_api_key = click.prompt("Please enter your new API key")
    config.set("OPENAI_API_KEY", new_api_key)
    click.echo("API key set successfully.")

@cli.command()
def set_model():
    """Set the model name."""
    new_model_name = click.prompt("Please enter the new model name")
    config.set("MODEL_NAME", new_model_name)
    click.echo("Model name set successfully.")


if __name__ == "__main__":
    cli()

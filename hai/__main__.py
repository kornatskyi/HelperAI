# standard
import os
from pathlib import Path

# external
from dotenv import load_dotenv, set_key
import click

# internal
from hai.model.api_manager import ApiManager
from hai.model.history import History
from hai.view.cli_view import CliView
from hai.controller.controller import Controller
from hai.utils.config import Config

# Initialize Config
config = Config()

# Use Config to initialize API Manager and Controller
api_model_name = config.get("model_name", "default_model")
api_key = config.get("openai_api_key", "default_key")

history = History(
    initialization_path=Path.home().joinpath("./Projects/HelperAI")
)
api_manager = ApiManager(api_model_name, api_key)
cli_view = CliView()
ai_controller = Controller(api_manager, cli_view, history)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        start()


@cli.command()
def start():
    """Starts the HAI conversation."""
    ai_controller.initiate_conversation()


@cli.command()
def set_apikey():
    """Set the API key."""
    new_api_key = click.prompt("Please enter your new API key")
    config.set("openai_api_key", new_api_key)
    click.echo("API key set successfully.")


@cli.command()
def select_model():
    """Set the model name."""
    # Display the models and their corresponding index
    selected_model = ""
    while selected_model == "":
        click.echo("Available models:")
        available_models = config.available_models()
        for index, model_name in enumerate(available_models):
            click.echo(f"{index + 1}. {model_name}")
        selected_index = click.prompt("Please select the new model", type=int)

        # Validate the index
        if 0 < selected_index <= len(available_models):
            selected_model = available_models[selected_index - 1]
            click.echo(f"You have selected: {selected_model}")
        else:
            click.echo("Invalid selection. Please try again.")

    config.set("model_name", selected_model)
    click.echo("Model name set successfully.")


if __name__ == "__main__":
    cli()

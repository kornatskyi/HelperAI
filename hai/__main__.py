# standard
import os
from pathlib import Path

# external
from dotenv import load_dotenv

# internal
from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView
from hai.controller.ai_controller import AiController
from tests.helper_classes import MockApiManager

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)


def main():
    api_model_name = "gpt-3.5-turbo-0613"
    api_key = os.getenv("OPENAI_API_KEY")
    
    # use mock api manager in development mode
    api_manager = (
        MockApiManager.MockApiManager()
        if os.getenv("MODE") == "development"
        else ApiManager(api_model_name, api_key)
    )
    cli_view = CliView()

    ai_controller = AiController(api_manager, cli_view)
    ai_controller.start()


if __name__ == "__main__":
    main()

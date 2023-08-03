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
    api_manager = None
    match os.getenv("AI_SOURCE"):
        case "openai":
            api_model_name = os.getenv("MODEL_NAME")
            api_key = os.getenv("OPENAI_API_KEY")
            api_manager = ApiManager(api_model_name, api_key)
        case _:
            api_manager = MockApiManager.MockApiManager()
    
    cli_view = CliView()

    ai_controller = AiController(api_manager, cli_view)
    ai_controller.start()


if __name__ == "__main__":
    main()

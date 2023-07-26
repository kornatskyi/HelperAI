from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView
from hai.controller.ai_controller import AiController

def main():
    api_model_name = "gpt-3.5-turbo-0613"
    api_key = ""
    api_manager = ApiManager(api_model_name, api_key)
    cli_view = CliView()
    
    ai_controller = AiController(api_manager, cli_view)
    ai_controller.start()

if __name__ == "__main__":
    main()

from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView

class AiController:
    def __init__(self, api_manager: ApiManager, cli_view: CliView):
        self.api_manager = api_manager
        self.cli_view = cli_view

    def start(self):
        while True:
            user_input = self.cli_view.get_user_input()
            if user_input.lower() == "quit":
                break
            response = self.api_manager.get_ai_response(user_input)
            self.cli_view.show_output(response)  # Assuming the response is already formatted

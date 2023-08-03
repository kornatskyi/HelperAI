import pyperclip as pc

from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView


class AiController:
    def __init__(self, api_manager: ApiManager, cli_view: CliView):
        self.api_manager = api_manager
        self.cli_view = cli_view

    def start(self):
        user_input = self.cli_view.get_user_input()
        if user_input.lower() == "quit":
            return
        # change it to iterate over a generator
        response = self.api_manager.get_ai_response(user_input)

        content_to_copy = self.cli_view.update_from_generator(response)
        user_input = self.cli_view.get_user_input()
        pc.copy(content_to_copy[int(user_input) - 1])

import pyperclip as pc

from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView


class Controller:
    def __init__(self, api_manager: ApiManager, cli_view: CliView):
        self.api_manager = api_manager
        self.cli_view = cli_view
        self.response_message = ""

    def ask_question(self) -> str:
        user_input = self.cli_view.get_user_input()
        if user_input.lower() == "quit":
            return
        response = self.api_manager.get_ai_response(user_input)
        (
            response_message,
            content_to_copy,
        ) = self.cli_view.update_from_generator(response)
        user_input = self.cli_view.get_user_input()
        try:
            to_copy = content_to_copy[int(user_input) - 1]
            pc.copy(to_copy)
            self.cli_view.show_output(f"Copied: {to_copy}")
            return response_message
        except:
            return response_message
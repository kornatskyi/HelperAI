import copy
from typing import Union
import pyperclip as pc
import re

from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView
from hai.model.History import History
from hai.model.UserMessage import UserMessage
from hai.model.AIMessage import AIMessage


class Controller:
    INT_POSITIVE_REGEX = re.compile(r"^[1-9]\d*$")

    def __init__(self, api_manager: ApiManager, cli_view: CliView):
        self.api_manager = api_manager
        self.cli_view = cli_view
        self.response_message = ""
        self.history = History()

    def ask_question(self, user_input) -> tuple[str, list[str]]:
        response = self.api_manager.get_ai_response(user_input)
        return self.cli_view.update_from_generator(response)

    def start_conversation(self):
        """
        Starts the conversation loop. The loop can be exited by typing "quit".
        """
        user_input = ""
        INT_POSITIVE_REGEX = r"^[1-9]\d*$"

        # conversation loop
        while True:
            user_input = self.cli_view.get_user_input()
            self.history.add(UserMessage(user_input))

            # copy code from the last message if input is a number
            if re.fullmatch(Controller.INT_POSITIVE_REGEX, user_input):
                # Handle code copying
                last_ai_message = self.history.get_last_ai_message()
                if last_ai_message is None:
                    self.cli_view.show_output("No previous AI message found.")
                    continue

                code_strings = last_ai_message.code_strings
                try:
                    to_copy = code_strings[int(user_input) - 1]
                    pc.copy(to_copy)
                    self.cli_view.show_output(f"Copied: {to_copy}")
                    continue
                except IndexError:
                    self.cli_view.show_output(
                        f"Wrong copy section number. Use values from 1 to {len(code_strings)}"
                    )
                except Exception as e:
                    self.cli_view.show_output(
                        f"An error occurred when copying code block: {e}"
                    )

            # Check if the user wants to quit the conversation
            if user_input.lower() == "quit":
                break

            (message, code_strings) = self.ask_question(user_input)
            self.history.add(AIMessage(message, code_strings))

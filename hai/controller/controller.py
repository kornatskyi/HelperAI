import re
from typing import List, Tuple

import pyperclip as pc

from hai.model.api_manager import ApiManager
from hai.utils.chat_price import Message, PriceChatListener
from hai.view.cli_view import CliView
from hai.model.history import History

# Constants
INT_POSITIVE_REGEX = re.compile(r"^[1-9]\d*$")


class Controller:
    def __init__(self, api_manager: ApiManager, cli_view: CliView):
        self.api_manager = api_manager
        self.cli_view = cli_view
        self.history = History()
        self.price_listener = PriceChatListener()
        self.code_strings_from_prev_request = []

    @property
    def last_ai_message(self) -> Message:
        return self.history.get_last_ai_message()

    def get_response_from_ai(
        self, conversation: List[Message]
    ) -> Tuple[str, List[str]]:
        """Get a response from the AI."""
        response = self.api_manager.get_ai_response(conversation)
        return self.cli_view.display_live_updates_from_generator(response)

    def initiate_conversation(self):
        """Initiate and manage the conversation loop."""

        while True:
            user_input = self.cli_view.get_user_input()
            self.history.add(Message(content=user_input, role="user"))

            if self._is_valid_code_block_number(user_input):
                self.copy_codeblock_to_clipboard(user_input)
                continue

            if user_input.lower() == "quit":
                break

            message, code_strings = self.get_response_from_ai(
                self.history.get()
            )
            self.code_strings_from_prev_request = code_strings
            self.price_listener.on_chat_response(
                messages=[Message(content=user_input, role="user")],
                response=Message(content=message, role="assistant"),
                model=self.api_manager.model_name,
            )
            self.history.add(Message(content=message, role="assistant"))

    def _is_valid_code_block_number(self, user_input: str) -> bool:
        return bool(re.fullmatch(INT_POSITIVE_REGEX, user_input))

    def copy_codeblock_to_clipboard(self, user_input: str):
        """Copy the specific code block to clipboard."""
        if not self.last_ai_message:
            self.cli_view.show_output("No previous AI message found.")
            return

        try:
            code_block = self.code_strings_from_prev_request[
                int(user_input) - 1
            ]
            pc.copy(code_block)
            self.cli_view.show_output(f"Copied: {code_block}")
        except IndexError:
            self.cli_view.show_output(
                f"Invalid copy section number. Use values from 1 to {len(self.code_strings_from_prev_request)}"
            )
        except Exception as e:
            self.cli_view.show_output(
                f"An error occurred when copying code block: {e}"
            )

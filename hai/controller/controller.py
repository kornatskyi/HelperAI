import re
from typing import List, Tuple

import pyperclip as pc

from hai.model.api_manager import ApiManager
from hai.utils.chat_price import Message, PriceChatListener
from hai.view.cli_view import CliView
from hai.model.history import Conversation, History

# Constants
INT_POSITIVE_REGEX = re.compile(r"^[1-9]\d*$")


class Controller:
    COMMANDS = {
        ":save": "save_history",
        ":new": "new_conversation",
        ":info": "display_info",
        ":delete": "delete_last_prompt",
        ":help": "display_help",
    }

    def __init__(
        self, api_manager: ApiManager, cli_view: CliView, history: History
    ):
        self.api_manager = api_manager
        self.cli_view = cli_view
        self.history = history
        self.price_listener = PriceChatListener(view=cli_view)
        self.code_strings_from_prev_request = []
        self.current_conversation = None

    @property
    def last_ai_message(self) -> Message:
        return self.current_conversation.get_last_ai_message()

    def get_response_from_ai(
        self, conversation: List[Message]
    ) -> Tuple[str, List[str]]:
        """Get a response from the AI."""
        response = self.api_manager.get_ai_response(conversation)
        return self.cli_view.display_live_updates_from_generator(response)

    def initiate_conversation(self):
        """Initiate and manage the conversation loop."""
        self.current_conversation = Conversation()
        while True:
            user_input = self.cli_view.get_user_input()
            self.current_conversation.add(
                Message(content=user_input, role="user")
            )

            if self._is_valid_code_block_number(user_input):
                self.copy_codeblock_to_clipboard(user_input)
                continue

            if user_input.lower() == "quit":
                break

            if user_input in self.COMMANDS:
                method_name = self.COMMANDS[user_input]
                method_to_call = getattr(self, method_name)
                method_to_call()
                continue

            message, code_strings = self.get_response_from_ai(
                self.current_conversation.get()
            )
            self.code_strings_from_prev_request = code_strings
            self.price_listener.on_chat_response(
                messages=[Message(content=user_input, role="user")],
                response=Message(content=message, role="assistant"),
                model=self.api_manager.model_name,
            )
            self.current_conversation.add(
                Message(content=message, role="assistant")
            )

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

    def save_history(self):
        self.history.persist(self.current_conversation)

    def new_conversation(self):
        self.current_conversation = Conversation()

    def display_info(self):
        # Modify according to your config structure.
        # For demonstration, just printing a simple message.
        self.cli_view.show_output("Displaying configuration information.")

    def delete_last_prompt(self):
        # Here, you can implement the logic to remove the last user prompt.
        self.current_conversation.delete_last_message()  # Assumes such a method exists in Conversation.

    def display_help(self):
        help_message = """
        :save - saves history
        :new - start new conversation
        :info - prints config info
        :delete - deletes the last prompt
        :help - prints this help message
        """
        self.cli_view.show_output(help_message)

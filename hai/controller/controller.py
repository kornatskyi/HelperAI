import copy
from typing import Union
import pyperclip as pc
import re


from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView


class User_Message:
    def __init__(self, message) -> None:
        self.message = message
        pass

    def __str__(self) -> str:
        return self.message


class AI_Message:
    def __init__(self, message, code_strings) -> None:
        self.message = message
        self.code_strings = code_strings
        pass

    def __str__(self) -> str:
        return self.message


class History:
    def __init__(self) -> None:
        self._list: list[Union[User_Message, AI_Message]] = []
        pass

    def get(self):
        return copy.deepcopy(self._list)

    def add(self, entry: Union[User_Message, AI_Message]):
        if not (
            isinstance(entry, User_Message) or isinstance(entry, AI_Message)
        ):
            raise "History can contain only User's and AI's messages"
        self._list.append(entry)

    def get_last_ai_message(self):
        for i in range(1, len(self._list)):
            entry = self._list[len(self._list) - i]
            if isinstance(entry, AI_Message):
                return entry


class Controller:
    def __init__(self, api_manager: ApiManager, cli_view: CliView):
        self.api_manager = api_manager
        self.cli_view = cli_view
        self.response_message = ""
        self.history = History()

    def ask_question(self, user_input) -> tuple[str, list[str]]:
        response = self.api_manager.get_ai_response(user_input)
        return self.cli_view.update_from_generator(response)

    def start_conversation(self):
        user_input = ""
        INT_POSITIVE_REGEX = r"^[1-9]\d*$"

        # conversation loop
        while True:
            user_input = self.cli_view.get_user_input()
            self.history.add(User_Message(user_input))

            # copy code from the last message if input is a number
            if re.fullmatch(INT_POSITIVE_REGEX, user_input):
                code_strings = self.history.get_last_ai_message().code_strings
                try:
                    to_copy = code_strings[int(user_input) - 1]
                    pc.copy(to_copy)
                    self.cli_view.show_output(f"Copied: {to_copy}")
                    continue
                except:
                    self.cli_view.show_output(f"Couldn't copy: {to_copy}")
                    continue

            if user_input.lower() == "quit":
                # break from conversation loop if user types "quit"
                break

            (message, code_strings) = self.ask_question(user_input)
            self.history.add(AI_Message(message, code_strings))

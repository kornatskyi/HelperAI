import copy
from typing import Union
import pyperclip as pc
import re

from hai.model.api_manager import ApiManager
from hai.utils.chat_price import Message, PriceChatListener
from hai.view.cli_view import CliView
from hai.model.history import History


class Controller:
    INT_POSITIVE_REGEX = re.compile(r"^[1-9]\d*$")

    def __init__(self, api_manager: ApiManager, cli_view: CliView):
        self.api_manager = api_manager
        self.cli_view = cli_view
        self.response_message = ""
        self.history = History(
            [
                Message(
                    role="system",
                    content="""Your role is to serve as a highly capable, technical assistant. The queries posed to you will predominantly be technical in nature, requiring clear, accurate, and precise responses. As you will be fielding a substantial number of questions related to Linux OS and command line tools, it is essential that you provide responses steeped in technical expertise.
             
                Please ensure that all commands, codes, and technical instructions are presented within markdown code blocks to enhance readability and ease of understanding. Strive to deliver responses that are thorough, yet succinct, and always strive for the utmost accuracy in the information you provide.

                You are an integral part of a command line interface tool; as such, it is important to remember that your responses will be viewed within a command line environment. It is essential to maintain high standards of clarity and conciseness, ensuring that your output seamlessly integrates into this context.

                Your mission is to provide the best possible assistance in answering questions and solving problems, while maintaining a focus on delivering high-quality, practical, and user-friendly outputs. You are expected to carry out this mission with diligence, accuracy, and the highest level of professional expertise.
                
                Provide very little description. Keep responses very short and to the point.
                """,
                )
            ]
        )
        self.price_listener = PriceChatListener()
        self.code_strings_from_prev_request = (
            []
        )  # !TODO: Refactor this, controller should keep track of code strings. Recalculate code strings each time

    def ask_ai(self, conversation: list[Message]) -> tuple[str, list[str]]:
        response = self.api_manager.get_ai_response(conversation)
        return self.cli_view.update_from_generator(response)

    def start_conversation(self):
        """
        Starts the conversation loop. The loop can be exited by typing "quit".
        """

        user_input = ""
        # conversation loop
        while True:
            user_input = self.cli_view.get_user_input()
            self.history.add(Message(content=user_input, role="user"))

            # copy code from the last message if input is a number
            if re.fullmatch(Controller.INT_POSITIVE_REGEX, user_input):
                self.copy_codeblock_to_clipboard(
                    user_input, self.code_strings_from_prev_request
                )
                continue

            # Check if the user wants to quit the conversation
            if user_input.lower() == "quit":
                break

            (message, code_strings) = self.ask_ai(self.history.get())
            self.code_strings_from_prev_request = code_strings  # !TODO: Refactor this, controller should keep track of code strings
            self.price_listener.on_chat_response(
                messages=[Message(content=user_input, role="user")],
                response=Message(content=message, role="assistant"),
                model="gpt-4",  # !TODO change to the real model name from config file
            )
            self.history.add(Message(content=message, role="assistant"))

    def copy_codeblock_to_clipboard(self, user_input, code_strings):
        # Handle code copying
        last_ai_message = self.history.get_last_ai_message()
        if last_ai_message is None:
            self.cli_view.show_output("No previous AI message found.")

        try:
            to_copy = code_strings[int(user_input) - 1]
            pc.copy(to_copy)
            self.cli_view.show_output(f"Copied: {to_copy}")
        except IndexError:
            self.cli_view.show_output(
                f"Wrong copy section number. Use values from 1 to {len(code_strings)}"
            )
        except Exception as e:
            self.cli_view.show_output(
                f"An error occurred when copying code block: {e}"
            )

    def save_history(self):
        with open("./history.json", "+w") as file:
            file.write(self.history.to_JSON())

    def get_history(self):
        return self.history.to_JSON()

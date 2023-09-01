class AIMessage:
    def __init__(self, message, code_strings) -> None:
        self.message = message
        self.code_strings = code_strings

    def __str__(self) -> str:
        return self.message

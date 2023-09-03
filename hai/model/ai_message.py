class AIMessage:
    def __init__(self, message, code_strings) -> None:
        self.message = message
        self.code_strings = code_strings

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict:
        return {"message": self.message}

    @classmethod
    def from_dict(cls, d) -> "AIMessage":
        return cls(d["message"])

    def __dict__(self):
        return self.to_dict()

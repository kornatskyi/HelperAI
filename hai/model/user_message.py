class UserMessage:
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict:
        return {"message": self.message}

    @classmethod
    def from_dict(cls, d) -> "UserMessage":
        return cls(d["message"])

    def __dict__(self):
        return self.to_dict()

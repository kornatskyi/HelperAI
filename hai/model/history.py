import copy
import json
from mailbox import Message

from hai.utils.config import Config


class History:
    def __init__(self, init_history: list[Message] = []) -> None:
        self._list = init_history
        self._history_path = Config()
        pass

    def get(self) -> list[Message]:
        return copy.deepcopy(self._list)

    def add(self, entry: Message) -> None:
        if type(entry) is not dict:
            raise ValueError(
                "History can contain only contain dict type entries"
            )
        self._list.append(entry)

    def get_last_ai_message(self):
        for i in range(1, len(self._list)):
            entry = self._list[len(self._list) - i]
            if isinstance(entry, Message):
                return entry

    def to_JSON(self) -> str:
        new_list = [
            {"user": message.__dict__()}
            if type(message) is Message
            else {"ai": message.__dict__()}
            for message in self._list
        ]
        return json.dumps(new_list, indent=2)

    def persist(self):
        """Save conversation history to file."""
        with open(self._history_path, "w") as file:
            file.write(self.to_JSON())

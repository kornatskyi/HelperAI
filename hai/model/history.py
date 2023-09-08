import copy
import json
from mailbox import Message


class History:
    def __init__(self) -> None:
        self._list: list[Message] = []
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

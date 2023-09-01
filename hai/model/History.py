import copy
from typing import Union

from hai.model.AIMessage import AIMessage
from hai.model.UserMessage import UserMessage


class History:
    def __init__(self) -> None:
        self._list: list[Union[UserMessage, AIMessage]] = []
        pass

    def get(self) -> list[Union[UserMessage, AIMessage]]:
        return copy.deepcopy(self._list)

    def add(self, entry: Union[UserMessage, AIMessage]) -> None:
        if type(entry) not in [UserMessage, AIMessage]:
            raise ValueError(
                "History can contain only User's and AI's messages"
            )
        self._list.append(entry)

    def get_last_ai_message(self):
        for i in range(1, len(self._list)):
            entry = self._list[len(self._list) - i]
            if isinstance(entry, AIMessage):
                return entry

import copy
from datetime import datetime
import json
import os
from typing import Union
from pathlib import Path
import uuid

from hai.model.message import Message


class Conversation:
    def __init__(
        self, name: str = "Default_name", init_conversation: list[Message] = []
    ) -> None:
        self._list = init_conversation
        self._name = name
        self._id = uuid.uuid1()
        self.unique_name = self._name[:100] + "_" + str(self._id)
        self.creation_time = datetime.now()

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
        conversation_to_save = {
            "id": str(self._id),
            "name": self._name,
            "creation_time": str(self.creation_time),
            "messages": self._list,
        }
        return json.dumps(conversation_to_save, indent=2)


class History:
    def __init__(
        self,
        initialization_path: Union[str, Path] = Path.home(),
    ) -> None:
        self._initialization_path = initialization_path

        # create history folder
        directory_name = "HelperAI_history"
        self.history_dir_path = Path.joinpath(
            initialization_path, directory_name
        )
        if not os.path.exists(self.history_dir_path):
            os.makedirs(directory_name)
            print(f"{directory_name} directory was created")
        else:
            print(f"{directory_name} already exists!")

    def persist(self, conversation: Conversation):
        """Save conversation history to file."""
        with open(
            self.history_dir_path.joinpath(conversation.unique_name + ".json"),
            "w",
        ) as file:
            file.write(conversation.to_JSON())

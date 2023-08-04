import json
from typing import Generator
from hai.model.api_manager import ApiManager
import time
import random


class MockApiManager(ApiManager):
    def __init__(self):
        super().__init__("", "")

    def get_ai_response(self, message) -> Generator[str, None, None]:
        response: str = ""
        with open("./tests/test_data/OpenAI_responses.json", "r") as conv_file:
            loaded_json = json.load(conv_file)
            response = loaded_json["responses"][0]["content"]

        iterator = 0
        while iterator < len(response):
            time.sleep(0.1)
            rand = random.randint(0, 4)
            yield response[iterator : iterator + rand]
            iterator += rand

import json
import random
import time


class DummyAI:
    @staticmethod
    def create(conversation, stream=False):
        response: str = ""
        with open("./tests/test_data/OpenAI_responses.json", "r") as conv_file:
            loaded_json = json.load(conv_file)
            response = loaded_json["responses"][0]["content"]
        if stream:
            iterator = 0
            while iterator < len(response):
                time.sleep(0.1)
                rand = random.randint(0, 4)
                yield response[iterator : iterator + rand]
                iterator += rand
        else:
            return response

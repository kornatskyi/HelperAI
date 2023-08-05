import json
import random
import time


class DummyAI:
    DELAY_OF_PRINTING_A_TOKEN = 0.001
    TEST_DATA_LOCATION = "./hai/mock/mock_data/OpenAI_responses.json"

    @staticmethod
    def create(conversation, stream=False):
        response: str = ""
        with open(DummyAI.TEST_DATA_LOCATION, "r") as conv_file:
            loaded_json = json.load(conv_file)
            response = loaded_json["responses"][0]["content"]
        if stream:
            iterator = 0
            while iterator < len(response):
                time.sleep(DummyAI.DELAY_OF_PRINTING_A_TOKEN)
                rand = random.randint(0, 4)
                yield response[iterator : iterator + rand]
                iterator += rand
        else:
            return response

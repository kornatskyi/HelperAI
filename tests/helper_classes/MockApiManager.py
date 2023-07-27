import json
from hai.model.api_manager import ApiManager


class MockApiManager(ApiManager):
    def __init__(self):
        super().__init__("", "")

    def get_ai_response(self, message) -> str:
        response = ""
        with open("./tests/test_data/OpenAI_responses.json", "r") as conv_file:
            loaded_json = json.load(conv_file)
            response = loaded_json["responses"][0]
        return response

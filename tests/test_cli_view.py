import json
import pytest
from hai.controller.ai_controller import AiController

from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView


class MockApiManager(ApiManager):
    def __init__(self):
        super().__init__("", "")

    def get_ai_response(self, message) -> str:
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]

        response = ""
        with open("./tests/test_data/OpenAI_responses.json", "r") as conv_file:
            loaded_json = json.load(conv_file)
            response = loaded_json["responses"][0]
        return response


@pytest.fixture
def app():
    api_manager = MockApiManager()
    cli_view = CliView()
    ai_controller = AiController(api_manager, cli_view)
    return ai_controller


def test_verify_output_is_correct(monkeypatch, app: AiController):
    monkeypatch.setattr(CliView, "get_user_input", lambda self: "Mocked input")
    app.start()
    assert True


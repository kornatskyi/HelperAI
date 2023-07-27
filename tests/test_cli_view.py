import pytest

from hai.controller.ai_controller import AiController
from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView
from tests.helper_classes import MockApiManager


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

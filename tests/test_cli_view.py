import pytest

from hai.controller.controller import Controller
from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView


@pytest.fixture
def app():
    api_manager = ApiManager(api_key="NotRealAPIKEy", model_name="mock")
    cli_view = CliView()
    ai_controller = Controller(api_manager, cli_view)
    return ai_controller


def test_verify_output_is_correct(monkeypatch,capfd, app: Controller):
    monkeypatch.setattr(CliView, "get_user_input", lambda self: "Mocked input")
    app.ask_question()
    out, err = capfd.readouterr()
    assert "To print the sizes of all files in the terminal" in out and "This command sorts the output in descending order of file size" in out


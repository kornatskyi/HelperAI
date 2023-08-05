import pytest
import pyperclip as pc

from hai.controller.controller import Controller
from hai.model.api_manager import ApiManager
from hai.view.cli_view import CliView


@pytest.fixture
def app():
    """Test setup

    Returns:
        Controller: _description_
    """
    MODEL_NAME = "mock"
    API_KEY = "NotRealAPIKEy"
    api_manager = ApiManager(api_key=API_KEY, model_name=MODEL_NAME)
    cli_view = CliView()
    controller = Controller(api_manager, cli_view)
    return controller


def test_ask_the_question_on_mock_data(monkeypatch, capfd, app: Controller):
    """
    Test if the 'ask_question' method of the Controller returns the correct response.
    We are mocking the user's question and then verifying if the controller's output 
    contains the expected text based on the mock data.
    """
    monkeypatch.setattr(
        CliView, "get_user_input", lambda self: "Mocked question?"
    )
    app.ask_question()
    out, err = capfd.readouterr()
    assert (
        "To print the sizes of all files in the terminal" in out
        and "This command sorts the output in descending order of file size"
        in out
    )

def test_copy_provided_command_to_clipboard(monkeypatch, capfd, app: Controller):
    """
    Test if the 'ask_question' method of the Controller correctly copies the provided
    command to the clipboard.
    We are mocking the user's question and their selection of the command to copy, and then
    checking if the correct command has been copied to the clipboard.
    """
    def user_input_generator():
        yield "Mocked question?"
        yield "1"

    gen = user_input_generator()
    monkeypatch.setattr(CliView, "get_user_input", lambda self: next(gen))
    app.ask_question()
    out, err = capfd.readouterr()
    assert (
        "To print the sizes of all files in the terminal" in out
        and "This command sorts the output in descending order of file size"
        in out
    )
    pasted = pc.paste()
    assert "du -ah" in pasted


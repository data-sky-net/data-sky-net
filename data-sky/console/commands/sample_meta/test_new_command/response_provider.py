"""Module for asking questions and providing factory registering with user responses."""

from questionary import prompt
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from response_provider import ResponseProvider
from test_new_command.questions import QUESTIONS


class TestNewResponseProvider(ResponseProvider):
    """Main class for asking questions and returning responses."""

    #: map for joining question id and its index in QUESTIONS dictionary.
    questions = {
        "project_name": QUESTIONS[0],
        "confirm_print": QUESTIONS[1],
    }

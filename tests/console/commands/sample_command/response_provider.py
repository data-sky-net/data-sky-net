"""Module for asking questions and providing factory registering with user responses."""

from questionary import prompt
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


class QuestionNotFound(Exception):
    """Raised if question not found in ResponseProvider questions dict."""
    pass


class ResponseProvider:
    """
    Main class for asking questions and returning responses.
    
    Args:
        args (list): Additional positional arguments.
        kwargs (dict): Keyword arguments, including options from CLI.

    Attributes:
        questions (dict): Map question id and its index in QUESTIONS dictionary. Example: questions = {"project_name": QUESTIONS[0]}
        responses (dict): Map quiestion id and response for it.

    Examples:
        ::

            >>> class ProjectNewResponseProvider(ResponseProvider):
            >>>     questions = {
            >>>         "project_name": QUESTIONS[0],
            >>>         "confirm_print": QUESTIONS[1],
            >>>     }
    """
    questions = dict()
    responses = dict()

    def __init__(self, *args, **kwargs):
        self.responses = kwargs

    def set_respond(self, quiestion_id, respond):
        """Set response for quiestion.
        
        Args:
            quiestion_id (str): Quiestion identifier.
            respond (Object): Response for question. 
        """
        self.responses[quiestion_id] = respond

    def respond(self, question_id, **kwargs):
        """Returns response using ``questionary`` lib.

        Args:
            question_id (str): String question identifier (used in ``questions``).
            **kwargs (dict): Key-value arguments for ``questionary`` questions. 
                Keys can have values: ``message``, ``choices``, ``default``, ``validate``.

        Raises:
            QuestionNotFound: Asked question not found in ResponseProvider questions map.

        Returns:
            object: Response with required data.
        """ 
        question = self.questions.get(question_id).copy()
        if question is None:
            raise QuestionNotFound("Asked question not found in ResponseProvider questions map.")

        for kwarg in ["message", "choices", "default", "validate"]:
            if kwarg in kwargs:
                question[kwarg] = kwargs.get(kwarg)

        response = self.responses.get(question_id)
        if response is None:
            response = prompt(question)[question_id]
            self.set_respond(question_id, response)

        return response

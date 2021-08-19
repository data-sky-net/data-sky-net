"""Module for asking quiestions and save user answers."""

from questionary import prompt


QUESTIONS = [
    {
        'type': 'text',
        'name': 'project_name',
        'message': 'Please, enter project name:'
    },
    {
        'type': 'confirm',
        'name': 'confirm_print',
        'message': 'Do you want to print project name?',
        'default': True
    }
]
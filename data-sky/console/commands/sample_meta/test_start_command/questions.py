"""Module for asking quiestions and save user answers."""

from questionary import prompt


QUESTIONS = [
    {
        'type': 'text',
        'name': 'project_name',
        'message': 'Please, enter project name:'
    },
    {
        'type': 'select',
        'name': 'select_color',
        'message': 'Choose one',
        'choices': ['red', 'blue']
    }
]
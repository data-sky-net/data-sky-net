"""
Module contains methods to create a project from template using cookiecutter.
"""

import os
from cookiecutter.main import cookiecutter


TEMPLATE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'redash', 'redash_template'
))


def run(config):
    """
    Run a cookiecutter to create a project from template.

    Args:
        config(dict): Dictionary with configuration.
    """
    cookiecutter(
        TEMPLATE_PATH,
        extra_context=config,
        no_input=True,
    )

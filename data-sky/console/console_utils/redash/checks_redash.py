"""
Module contains functions to check availability of setup environment.
"""
import subprocess
import os

REDASH_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'redash'
))

OK_STATUS = 0


def _check_setup():
    return os.path.exists(REDASH_PATH)


def check_mongo_run():
    """Returns true if mongo is running false otherwise.

    Returns:
        bool: True if mongo is running false otherwise.
    """
    return subprocess.getoutput('$DOCKER_CMD inspect -f \'{{.State.Running}}\' mongo')


dependency = {
    'checker': check_mongo_run,
    'error_message': 'Mongo isn\'t running'
}


def run_check_setup():
    """Print error message if setup.sh file wasn't found."""
    if not os.path.exists(REDASH_PATH):
        print('Not found setup.sh for redash')
        exit(1)


def run_check_mongo():
    """Print error message if mongo isn't running."""
    if dependency['checker']() == 'false':
        print(dependency['error_message'])
        exit(1)

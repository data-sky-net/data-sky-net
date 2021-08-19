"""
Module contains functions to facilitate working with redash.
"""
import datetime


def psql_with_params_for_message(answers, config):
    """
    Function to assemble PostgreSQL cmd command with message.

    Args:
        answers(list): List of user answers.
        config(dict): Database config.
    Returns:
        str: PostgreSQL cmd command.
    """
    message = answers['message']
    now = datetime.datetime.now()
    psql = psql_with_params(config)
    return f'{psql} -v message="{message}" -v now="{now}"'


def psql_with_params(config):
    """
    Function to assemble PostgreSQL cmd command.

    Args:
        config(dict): Database config.
    Returns:
        str: PostgreSQL cmd command.
    """
    db_config = config['db']
    use_docker_container = ''
    if db_config['container'] == True:
        container_name = db_config['name']
        use_docker_container = f'$DOCKER_CMD exec -i {container_name}'
    user = db_config['user']
    db = db_config['database']
    password = db_config['password']
    return f'PGPASSWORD={password} {use_docker_container} psql -q -U {user} -d {db}'


def parse_env_file(path):
    """
    Function to parse env file and store vars in dictionary.

    Args:
        path(str): Path to env file.
    Returns:
        dict: key - Value pairs of environment variables.
    """
    dict = {}
    with open(path) as f:
        for line in f.readlines():
            key, value = line.rstrip("\n").split("=")
            dict[key] = value
    return dict

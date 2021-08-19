"""
Module contains methods to assemble a questionnaire.
"""
import json
import os
import subprocess
from console_utils.redash import checks_redash
import questionary

from dotenv import load_dotenv

dotenv_file_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_file_path)

BLACKLIST = [
    "_id",
    "attachments_gridfs_id",
    "author",
    "creation_ts",
    "data_scaler",
    "data_scaler_gridfs_id",
    "feature_mining_comments",
    "message",
    "model",
    "model_feature_columns",
    "model_feature_importances",
    "model_fill_na_values",
    "model_gridfs_id",
    "model_name",
    "model_version",
    "notebook_gridfs_id",
    "notebook_gziped_file",
    "result_gridfs_id",
    "result_gzipped_file",
    "signals_hash",
    "tags",
    "task_name"
]

def _get_messages():
    messages = []
    if checks_redash.check_mongo_run() == 'true':
        INIT_DB = os.environ['MONGO_DB']
        json_messages = json.loads(
            subprocess.getoutput(
                f'$DOCKER_CMD exec -i mongo mongo {INIT_DB} --quiet --eval \'db.runCommand({{distinct:"submits",key:"message"}})\''))
        messages = messages + json_messages['values']

    return messages


def _get_metrics_by_message(message):
    fields = []
    if checks_redash.check_mongo_run() == 'true':
        INIT_DB = os.environ['MONGO_DB']
        fields = json.loads(subprocess.getoutput(
            f'$DOCKER_CMD exec -i mongo mongo {INIT_DB} --quiet --eval \'db[db.runCommand({{"mapreduce":"submits","map":function() {{if (this.message=="{message}") {{for (var key in this) {{if (typeof this[key] == "number") {{emit(key,null);}}}}}}}},"reduce":function(key,stuff) {{return null;}},"out":"my_collection"+"_keys"}}).result].distinct("_id")\''))
    return [metric for metric in fields if metric not in BLACKLIST]


def create_new_message():
    """
    Ask question about the creation a new message.

    Returns:
           str: User response.
    """
    return questionary.confirm("Create widgets for another message?").ask()


def run_message_questions(all_metrics):
    """
    Method to ask message questions and write a dictionary with metrics.

    Args:
        all_metrics(boolean): Flag to create widgets for all task metrics.

    Returns:
        dict: Dictionary with a message and metrics chosen by user.
    """

    message = questionary.rawselect(
        "Which message to use?",
        choices=_get_messages()).ask()
    metrics = questionary.checkbox(
        'Select metrics',
        choices=_get_metrics_by_message(message)).skip_if(all_metrics, default=_get_metrics_by_message(message)).ask()

    return {"message": message,
            "metrics": metrics}


def run(all_metrics):
    """
    Run a questionnaire.

    Args:
        all_metrics(boolean): Flag to create widgets for all task metrics.

    Returns:
        list: User answers.
    """
    name_ds = questionary.text("What name for new datasource?").ask()
    answers = run_message_questions(all_metrics)
    answers.update({'name_ds': name_ds})
    return answers


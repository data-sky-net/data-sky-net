import json
import os
import pathlib
import sys
from unittest.mock import patch

sys.path.append(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'data-sky',
            'console',
            'commands',
            'toolkit_cli',
            'scripts',
        )
)
import make_dataset


@patch('make_dataset.requests.get')
def test_data_sender_datasets_call_expected_params(mock_get):
    default_project_config_path = pathlib.Path(make_dataset.DEFAULT_PROJECT_CONFIG_PATH).resolve()
    with open(default_project_config_path, 'r') as f:
        default_project_config = json.load(f)

    default_url = f"http://{default_project_config['data_service_settings']['host']}/api/v1/data/catalog/default_import/meta"
    ds = make_dataset.DataSender()
    ds.datasets()
    mock_get.assert_called_with(url=default_url)

import pytest
import os


@pytest.fixture()
def test_env():

    os.environ["REG_PATH"] = "../../tests/console/commands/register_test.json"

    yield

    os.environ.pop("REG_PATH")
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from test_new_command.response_provider import TestNewResponseProvider
from cli_command import CliCommand


class TestNewCommand(CliCommand):
    groups = [
        {
            "name": "test",
            "help": "Group for testing"
        }
    ]
    name = "new"
    help = "NEW for test command"
    options = [
        {
            "args": ("-p", "--project_name", "project_name"),
            "kwargs": {
                "help": "Project name",
                "type": str,
                "required": False,
                "is_flag": False
            }
        },
        {
            "args": ("-c", "--confirm_print", "confirm_print"),
            "kwargs": {
                "help": "Confirm print",
                "type": bool,
                "required": False,
                "is_flag": False
            }
        }
    ]

    def run(self, *args, **kwargs):
        self.response_provider = TestNewResponseProvider(*args, **kwargs)
        print("Lets test NEW command!")

        project_name = self.response_provider.respond("project_name")

        if self.response_provider.respond("confirm_print"):
            print(f"Project name is {project_name}")
        else:
            print("OK")

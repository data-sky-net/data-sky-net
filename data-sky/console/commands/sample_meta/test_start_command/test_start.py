import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from test_start_command.response_provider import TestStartResponseProvider
from cli_command import CliCommand


class TestStartCommand(CliCommand):
    groups = [
        {
            "name": "test",
            "help": "Group for testing"
        }
    ]
    name = "start"
    help = "START for test command"
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
            "args": ("-s", "--select_color", "select_color"),
            "kwargs": {
                "help": "Select color",
                "type": str,
                "required": False,
                "is_flag": False
            }
        }
    ]

    def run(self, *args, **kwargs):
        self.response_provider = TestStartResponseProvider(*args, **kwargs)
        print("Lets test START command!")

        project_name = self.response_provider.respond("project_name")
        print(f"OK, project {project_name}")
        color = self.response_provider.respond("select_color")

        print(f"Results: project {project_name}, color {color}")

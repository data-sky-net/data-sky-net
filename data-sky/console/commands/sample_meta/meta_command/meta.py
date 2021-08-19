import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from cli_command import MetaCliCommand
from test_new_command.test_new import TestNewCommand
from test_start_command.test_start import TestStartCommand


class MetaCommand(MetaCliCommand):
    name = "meta"
    help = "Metacommand"
    commands = [
        TestNewCommand(),
        TestStartCommand()
    ]

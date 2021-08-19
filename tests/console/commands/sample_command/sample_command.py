import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from response_provider import ResponseProvider


class CliCommand:

    groups = []
    name = None
    help = ""
    options = []

    def __init__(self):
        if self.name is None:
            logging.warning("Command name is None")
            raise NotImplementedError()

    @classmethod
    def get_groups(cls):
        return cls.groups

    @classmethod
    def get_name(cls):
        return cls.name

    @classmethod
    def get_help(cls):
        return cls.help

    @classmethod
    def get_options(cls):
        return cls.options

    def run(self, *args, **kwargs):
        raise NotImplementedError()


class MetaCliCommand(CliCommand):
    commands = []

    def __init__(self):
        super().__init__()
        self._collect_options()
        self.response_provider = ResponseProvider()

    def run(self, *args, **kwargs):
        meta_command_options = kwargs

        for command in self.commands:
            # merge start meta-command options and meta-command responses
            command_kwargs = {**meta_command_options, **self.response_provider.responses}

            command.run(*args, **command_kwargs)
            command_responses = command.response_provider.responses

            # add current command responses to meta-command responses
            self.response_provider.responses.update(command_responses)

    @classmethod
    def _collect_options(cls):
        for command in cls.commands:
            command_options = command.options
            cls.options += command_options


class SampleCommand(CliCommand):

    groups = [
        {
            "name": "test",
            "help": "Group for testing"
        }
    ]
    name = "sample"
    help = "This is a sample command"

    def run(self, *args, **kwargs):
        print(f"{self.name} command ran")


class SampleCommand2(CliCommand):

    groups = [
        {
            "name": "test",
            "help": "Group for testing"
        },
        {
            "name": "check",
            "help": "Another group for testing"
        }
    ]
    name = "sample2"
    help = "This is another sample command"

    options = [
        {
            "args": ("-o", "--opt", "my_option"),
            "kwargs": {
                "help": "Test option",
                "type": int,
                "default": 3,
                "required": False,
                "is_flag": False
            }
        }
    ]

    def run(self, *args, **kwargs):

        print(kwargs)
        print(f"{self.name} command ran")


class SampleMetaCommand(MetaCliCommand):
    name = "meta"
    help = "Metacommand"
    commands = [
        SampleCommand(),
        SampleCommand2()
    ]
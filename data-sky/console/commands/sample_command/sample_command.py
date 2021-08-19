import logging


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
        }
    ]
    name = "Sample2"
    help = "This is another sample command"

    options = [
        {
            "args": ("-o", "--opt", "my_option"),
            "kwargs": {
                "help": "Test option",
                "type": int,
                "required": False,
                "is_flag": False
            }
        }
    ]

    def run(self, *args, **kwargs):

        print(kwargs)
        print(f"{self.name} command ran")
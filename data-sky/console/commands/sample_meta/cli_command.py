"""Module contains class for connection to Project Wizard."""

from utils import get_default_logger
from response_provider import ResponseProvider


class CliCommand:
    """
    This is a base class for creation any CLI command which is supported by Wizard.
    Any CLI command class must be inherited from this class.
    Any CLI command class should contain the attributes and override method 'run' with 'args' and 'kwargs'.

    Attributes:
        groups(list[dict]): List of command groups by 'click' notation. The list contains dictionaries:
            ``{'name':'group_name', 'help': 'group help string'}``.
        name(str): The name of the command.
        help(str, optional): Help string for the command. (Default value = "")
        options(list[dict]): List of options in 'click' notation. The list contains dictionaries with option data.
            'Args' and 'kwargs' can contain any available parameters according to 'click' official documentation
            ('options' description).

    Examples:
            ::

                >>> class SampleCommand(CliCommand):
                >>>     groups = [
                >>>         {
                >>>             "name": "test",
                >>>             "help": "Group for testing"
                >>>         }
                >>>     ]
                >>>     name = "sample"
                >>>     help = "This is another sample command"
                >>>
                >>>     options = [
                >>>         {
                >>>             "args": ("-o", "--opt", "my_option"),
                >>>             "kwargs": {
                >>>                 "help": "Test option",
                >>>                 "type": int,
                >>>                 "required": False,
                >>>                 "is_flag": False
                >>>             }
                >>>         }
                >>>     ]
                >>>
                >>>     def run(self, *args, **kwargs):
                >>>
                >>>         print(kwargs)
                >>>         print(f"{self.name} command ran")

    """

    groups = []
    name = None
    help = ""
    options = []

    def __init__(self):
        self.logger = get_default_logger()
        if self.name is None:
            self.logger.warning("Command name is None")
            raise NotImplementedError()
        

    @classmethod
    def get_groups(cls):
        """
        Groups getter.

        Returns:
            list: list of groups in which this command included.
        """
        return cls.groups

    @classmethod
    def get_name(cls):
        """
         Name getter.

         Returns:
            str: command name.
         """
        return cls.name

    @classmethod
    def get_help(cls):
        """
         Help getter.

         Returns:
            str: help string.
         """
        return cls.help

    @classmethod
    def get_options(cls):
        """
         Options getter.

         Returns:
            list: command args and kwargs.
         """
        return cls.options

    def run(self, *args, **kwargs):
        """Must be implemented by descendant class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        raise NotImplementedError()


class MetaCliCommand(CliCommand):
    """
    This is a base class for Wizard CLI metacommands.
    Commands of this type aggregates several CLI commands with reusing options and responses.

    Metacommand must have a ``commands`` attribute with a list of commands Python objects.
    Also it can implement all CliCommand attributes, such as ``name``, ``groups``, ``options``, etc.
    
    All CliCommand options will be automatically added and can be used in metacommand.

    Attributes:
        commands (list[object]): List of CliCommand objects in order of execution.
        response_provider (object): A `ResponseProvider` class instance - this object will collect all responses from included CLI commands.
            Optional, by default metacommands use response provider with no extra questions (only questions from subcommands). 

    Examples:
        ::

            >>> class SampleMetaCommand(MetaCliCommand):
            >>>     name = "meta"
            >>>     help = "This is a metacommand for two actions: create and start project."
            >>>     commands = [
            >>>         ProjectNewCommand(),
            >>>         ProjectStartCommand()
            >>>     ]
    """
    commands = []
    response_provider = ResponseProvider()

    def __init__(self):
        super().__init__()
        self._collect_options()

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

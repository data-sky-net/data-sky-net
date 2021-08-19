Add New Command
----------------------

Every new command should be inherited from the class "CliCommand".

.. code-block:: python

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

'name' - is required class field. It must be overriden.
'groups', 'help', 'options' - optional fields. Can be remained default.

'groups' is an array of dicts:

.. code-block:: python

    groups = [
        {
            "name": "test",
            "help": "Group for testing"
        },
        {
            "name": "check",
            "help": "check help"
        }
    ]

Where 'name' - is name of command group (Example: 'project' in 'data-sky project new').
'help' - help string for specific group.

'options' - is an array of dicts as follows:

.. code-block:: python

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

'args' and 'kwargs' contain actual arguments of the function click.option(). (See click docs).

'run' - is the main function of the command which contained all the actions.
args and kwargs are required, all arguments are transmitted via them.


Folder with files of the command must be put into 'console/commands/' path.


Register command
----------------------

All command must be written down to the file 'register.json' with actual import path (dot delimited) and class name (see example file).
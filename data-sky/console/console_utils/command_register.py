"""The file contains a class for managing commands: CommandRegister"""

import os
import importlib
import inspect
import logging
import json


class CommandRegister:
    """
    This class is for managing of commands from toolkit_cli (not only).
    The class can find all the commands to register, and add commands from register to wizard.

    Args:
        full_register_name(str): The name of the register.json file with full path.

    """

    def __init__(self, full_register_name):
        self._full_register_name = full_register_name

    @staticmethod
    def _is_heir(object, parent_name):
        parent_class_names = [cl.__name__ for cl in inspect.getmro(object)]
        return (parent_name in parent_class_names) and (object.__name__ != parent_name)

    def upgrade_register(self, dir_to_find, calling_file_dir):
        """
        The method searches the cli commands and adds them to the register.json file.
        Cli commands - classes which inherited from CliCommand class

        Args:
            dir_to_find(str): Path to directory for searching of the commands.
            calling_file_dir(str): The directory of the file which calls "register_commands" method of
                the current class (ProjectContextManager).

        """

        register = {"commands": []}
        missing_modules = []
        ignore_list = ['test', 'tests', '{{', '__pycache__']

        for dir_rec in os.walk(dir_to_find):
            import_path = os.path.relpath(dir_rec[0], calling_file_dir).replace("/", ".")

            for file_name in dir_rec[2]:
                if file_name.split(".")[-1] == "py" and all([import_path.find(w) == -1 for w in ignore_list]):
                    modulename = file_name[:file_name.rfind(".")]

                    if import_path != ".":
                        full_module_name = '.'.join([import_path, modulename])
                    else:
                        full_module_name = modulename

                    try:
                        module = importlib.import_module(full_module_name)
                        members = inspect.getmembers(module)
                        for member in members:
                            if inspect.isclass(member[1]) and self._is_heir(member[1], "CliCommand"):
                                register["commands"].append(
                                    {
                                        "module": full_module_name,
                                        "class_name": member[1].__name__
                                    }
                                )
                    except ImportError as e:
                        missing_modules.append(modulename)

        missing_modules_str = '\n'.join(missing_modules)
        logging.warning(
            f"""Following modules have not been checked due to import error inside them:
    {missing_modules_str}"""
        )

        with open(self._full_register_name, 'w') as file_to_save:
            json.dump(register, file_to_save, sort_keys=True, indent=4)

    def register_commands(self):
        """
        The method to create all the objects of the commands, registered in register.json file.

        Returns:
            list: list commands objects (not click objects).

        Raises:
            KeyError: is raised when some register's field is incorrect.
            ModuleNotFoundError: is raised when the module registered is not can not be imported.

        """

        with open(self._full_register_name, 'r') as file_to_read:
            command_register = json.loads(file_to_read.read())

        commands = command_register.get("commands")
        if commands is None:
            logging.error("Command register is incorrect")
            return []

        command_objects = []

        for command in commands:
            module_name = command.get("module")
            class_name = command.get("class_name")

            if (module_name is None) or (class_name is None):
                logging.error("Commands in the register are described in incorrect way.")
                raise KeyError()

            try:
                command_module = importlib.import_module(module_name)
                command_class = getattr(command_module, class_name)
                command_object = command_class()
                command_objects.append(command_object)
            except ModuleNotFoundError as e:
                logging.error("Command modules specified in the register are not found!")
                raise e

        return command_objects
import sys
import os
import logging

sys.path.append(os.path.dirname(__file__))
import click
from console_utils.command_register import CommandRegister


@click.group()
def cli():
    pass


class DuplicatedCommandError(Exception):
    pass


def bind_function(name, f):
    """
    The function is used for binding click commands and groups instead of decorators
    Args:
        name(str): name of group or command.
        f(function): empty function for a group or action for a command.

    Returns:
        function: binded function, which does action of the command or nothing (for group).

    """
    def func(*args, **kwargs):
        f(*args, **kwargs)

    func.__name__ = name
    return func


def add_commands(register_rel_path="commands/register.json"):
    """
    The function automatically adds commands by register.json to the click.
    Args:
        register_rel_path(str): path to the register.json file.

    """
    cur_file_path = os.path.dirname(os.path.realpath(__file__))
    register_full_name = os.path.join(cur_file_path, register_rel_path)
    CR = CommandRegister(full_register_name=register_full_name)
    command_objects = CR.register_commands()

    for command_object in command_objects:
        group_func = cli
        for group in command_object.get_groups():
            group_name = group["name"]
            group_help = group["help"]
            found_group = group_func.get_command(ctx=None, cmd_name=group_name)

            if found_group is None:
                bound_func = bind_function(group_name, lambda: None)
                next_group_func = group_func.group(name=group_name, help=group_help)(bound_func)
            else:
                next_group_func = found_group

            group_func = next_group_func

        found_command = group_func.get_command(ctx=None, cmd_name=command_object.get_name())
        if found_command is not None:
            logging.error("Command duplicated!")
            raise DuplicatedCommandError()

        command_func = bind_function(command_object.get_name(), command_object.run)
        options = command_object.get_options()

        for option in options:
            click.option(*option["args"], **option["kwargs"])(command_func)
        group_func.command(
            name=command_object.get_name(),
            help=command_object.get_help()
        )(command_func)

# for debug and tests
REG_PATH = os.environ.get("REG_PATH")

if REG_PATH is not None:
    add_commands(register_rel_path=REG_PATH)
else:
    add_commands()

if __name__ == '__main__':
    cli()

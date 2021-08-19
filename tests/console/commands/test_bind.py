import sys
import os
import json
from click.types import INT

from data-sky.console.console_utils.command_register import CommandRegister

sys.path.append(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data-sky', 'console')
)


def test_add_command(test_env):

    import main

    test_cmd = main.cli.get_command(ctx=None, cmd_name="test")
    sample_cmd = test_cmd.get_command(ctx=None, cmd_name="sample")
    check_cmd = test_cmd.get_command(ctx=None, cmd_name="check")
    sample2_cmd = check_cmd.get_command(ctx=None, cmd_name="sample2")
    option = sample2_cmd.params[0]

    assert test_cmd.name == "test"
    assert sample_cmd.name == "sample"
    assert check_cmd.name == "check"
    assert sample2_cmd.name == "sample2"
    assert option.name == "my_option"
    assert option.type == INT
    assert not option.required
    assert not option.is_flag
    assert option.default == 3
    assert option.help == "Test option"


def test_upgrade_register():
    register_rel_path = "../commands/register_test2.json"
    rel_dir_to_find = "./"
    cur_file_path = os.path.dirname(os.path.realpath(__file__))
    register_full_name = os.path.join(cur_file_path, register_rel_path)
    dir_to_find = os.path.abspath(os.path.join(cur_file_path, rel_dir_to_find))

    CR = CommandRegister(register_full_name)

    CR.upgrade_register(
        dir_to_find=dir_to_find,
        calling_file_dir=cur_file_path
    )

    with open(register_full_name, "r") as file_to_read:
        register = json.loads(file_to_read.read())

        commands = register.get("commands")

        assert commands is not None

        assert commands[1]["class_name"] == "SampleCommand"
        assert commands[2]["module"] == "sample_command.sample_command"
        assert commands[3]["class_name"] == "SampleMetaCommand"
        
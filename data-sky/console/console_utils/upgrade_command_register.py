"""The module searches the cli commands and adds them to the register. Should be run manually."""

import os
import sys
from command_register import CommandRegister

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

if __name__ == "__main__":
    register_rel_path = "../commands/register.json"
    rel_dir_to_find = "../commands"
    cur_file_path = os.path.dirname(os.path.realpath(__file__))
    register_full_name = os.path.join(cur_file_path, register_rel_path)
    dir_to_find = os.path.realpath(os.path.join(cur_file_path, rel_dir_to_find))

    CR = CommandRegister(register_full_name)

    CR.upgrade_register(
        dir_to_find=dir_to_find,
        calling_file_dir=os.path.realpath(os.path.join(cur_file_path, "../"))
    )

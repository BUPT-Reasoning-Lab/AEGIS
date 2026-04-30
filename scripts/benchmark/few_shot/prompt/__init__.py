import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# System prompts
SYS_FORGERYSCOPE = os.path.join(base_path, "system", "sys_forgeryscope.txt")
SYS_MANIPULATION = os.path.join(base_path, "system", "sys_manipulation.txt")
SYS_VISUALTEXT = os.path.join(base_path, "system", "sys_visualtext.txt")

# User prompts
USR_FORGERYSCOPE = os.path.join(base_path, "user", "usr_forgeryscope.txt")
USR_MANIPULATION = os.path.join(base_path, "user", "usr_manipulation.txt")
USR_VISUALTEXT = os.path.join(base_path, "user", "usr_visualtext.txt")

__all__ = [
    "SYS_FORGERYSCOPE",
    "USR_FORGERYSCOPE",
    "SYS_MANIPULATION",
    "USR_MANIPULATION",
    "SYS_VISUALTEXT",
    "USR_VISUALTEXT",
]


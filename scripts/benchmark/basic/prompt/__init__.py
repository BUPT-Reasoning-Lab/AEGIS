import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# NOTE:
# The "basic" benchmark stores prompt templates as plain text files under
# `prompt/system/*.txt` and `prompt/user/*.txt`. We expose both SYS_* and USR_*
# paths so the rest of the benchmark config can reference them consistently.

# Forgery scope discrimination
SYS_FORGERYSCOPE = os.path.join(base_path, "system", "forgery_scope_discrimination_prompt.txt")
USR_FORGERYSCOPE = os.path.join(base_path, "user", "forgery_scope_discrimination_prompt.txt")

# Manipulation classification (contains both "System Prompt" and "User Prompt" sections)
SYS_MANIPULATION = os.path.join(base_path, "system", "manipulation_classification_prompt.txt")
USR_MANIPULATION = os.path.join(base_path, "user", "manipulation_classification_prompt.txt")

# Textual artifact recognition
SYS_VISUALTEXT = os.path.join(base_path, "system", "textual_artifact_recognition_prompt.txt")
USR_VISUALTEXT = os.path.join(base_path, "user", "textual_artifact_recognition_prompt.txt")

# Tampering pinpointing (contains both "System Prompt" and "User Prompt" sections)
SYS_PINPOINTING = os.path.join(base_path, "system", "tampering_pinpointing_prompt.txt")
USR_PINPOINTING = os.path.join(base_path, "user", "tampering_pinpointing_prompt.txt")

__all__ = [
    "SYS_FORGERYSCOPE",
    "USR_FORGERYSCOPE",
    "SYS_MANIPULATION",
    "USR_MANIPULATION",
    "SYS_VISUALTEXT",
    "USR_VISUALTEXT",
    "SYS_PINPOINTING",
    "USR_PINPOINTING",
]

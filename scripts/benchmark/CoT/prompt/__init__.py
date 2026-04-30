import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# System prompts
SYS_FSD = os.path.join(base_path, "system", "forgery_scope_discrimination.md")
SYS_MC = os.path.join(base_path, "system", "manipulation_classification.md")
SYS_TAR= os.path.join(base_path, "system", "textual_artifact_recognition.md")
SYS_TP = os.path.join(base_path, "system", "tampering_pinpointing.md")


# User prompts
USR_FSD = os.path.join(base_path, "user", "forgery_scope_discrimination.md")
USR_MC = os.path.join(base_path, "user", "manipulation_classification.md")
USR_TAR = os.path.join(base_path, "user", "textual_artifact_recognition.md")
USR_TP = os.path.join(base_path, "user", "tampering_pinpointing.md")


__all__ = [
    "SYS_FSD",
    "USR_FSD",
    "SYS_MC",
    "USR_MC",
    "SYS_TAR",
    "USR_TAR",
    "SYS_TP",
    "USR_TP",
]

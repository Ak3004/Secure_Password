"""Global configuration for the password manager.

This module provides canonical file paths (and related helpers) for the
password storage JSON file, master login file, and log file.

Use these paths everywhere in the project so that the storage locations are
centralized and can be changed in one place.
"""

from __future__ import annotations

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent

MASTER_LOGIN_FILENAME = "master_login.json"
PASSWORD_FILE_NAME = "app_password.json"
LOG_FILE_NAME = "log.txt"

MASTER_LOGIN_PATH: Path = BASE_DIR / MASTER_LOGIN_FILENAME
PASSWORD_FILE_PATH: Path = BASE_DIR / PASSWORD_FILE_NAME
LOG_FILE_PATH: Path = BASE_DIR / LOG_FILE_NAME


def ensure_data_dir_exists() -> None:
    """Create the data directory if it does not exist.

    This is a no-op if the project files are stored in the same directory as
    this module (the current default), but it makes the intention explicit.
    """

    BASE_DIR.mkdir(parents=True, exist_ok=True)

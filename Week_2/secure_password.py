import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure root package path is on sys.path so this module works when run from Week_2/.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import (
    ensure_data_dir_exists,
    LOG_FILE_PATH,
    MASTER_LOGIN_PATH,
    PASSWORD_FILE_PATH,
)

# Dummy Data
# {"Username":"Password"}
master_login = {"Jimmy": "robert@123", "Angela": "2009_Bonnet"}


#  { "Username":[ {"domain":"", "pwd":"" },
#                 {"domain":"", "pwd":"" },... ] }
app_password = {
    "Jimmy": [
        {"domain": "Facebook", "pwd": "JimmyGordan"},
        {"domain": "Instagram", "pwd": "B0atm@n"},
    ],
    "Angela": [
        {"domain": "Facebook", "pwd": "Angela009"},
        {"domain": "Instagram", "pwd": "Mikcy&Angela"},
    ],
}

# Ensure the directory exists (useful if config is moved to a dedicated data folder)
ensure_data_dir_exists()

# writing the dummy data into the files
if not MASTER_LOGIN_PATH.exists():
    with MASTER_LOGIN_PATH.open("w+", encoding="utf-8") as file:
        json.dump(master_login, file, indent=4)
    print(f"{MASTER_LOGIN_PATH} created and data written.")

if not PASSWORD_FILE_PATH.exists():
    with PASSWORD_FILE_PATH.open("w+", encoding="utf-8") as file:
        json.dump(app_password, file, indent=4)
    print(f"{PASSWORD_FILE_PATH} created and data written.")

if not LOG_FILE_PATH.exists():
    with LOG_FILE_PATH.open("w+", encoding="utf-8") as file:
        pass
    print(f"{LOG_FILE_PATH} created.")

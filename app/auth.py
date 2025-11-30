import os
from typing import Dict

# Simple credential store; override defaults with environment variables if desired
USERS: Dict[str, str] = {
    "Pablo": os.environ.get("PABLO_PASSWORD", "***REMOVED***"),
    "Eva": os.environ.get("EVA_PASSWORD", "***REMOVED***"),
}


def verify_credentials(username: str, password: str) -> bool:
    expected = USERS.get(username)
    return expected is not None and password == expected


def get_user(session) -> str | None:
    return session.get("user")


def set_user(session, username: str) -> None:
    session["user"] = username


def clear_user(session) -> None:
    session.pop("user", None)


__all__ = ["USERS", "verify_credentials", "get_user", "set_user", "clear_user"]

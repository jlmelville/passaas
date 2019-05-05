"""
User model.
"""

from typing import NamedTuple
from flask import current_app


class User(NamedTuple):
    """
    An entry in the passwd file, representing a user.
    """

    name: str
    uid: int
    gid: int
    comment: str
    home: str
    shell: str


def find_users(users, uid):
    """
    Returns list of users with the specified uid, or an empty list if none match.
    """
    return [u for u in users if u.uid == uid]


def read_passwd():
    """
    Reads the passwd file and returns a list of Users.
    """
    users = list()
    with open(current_app.config["PASSWD_PATH"]) as passwd_file:
        for line in passwd_file:
            (name, _, uid, gid, comment, home, shell) = [
                e.strip() for e in line.split(":")
            ]
            users.append(User(name, int(uid), int(gid), comment, home, shell))
    return users

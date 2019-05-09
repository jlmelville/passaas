# pylint: disable=too-many-arguments,too-few-public-methods
"""User model."""

from typing import NamedTuple
from flask import current_app

from passaas.models.util import sanitize_id, find


class User(NamedTuple):
    """An entry in the passwd file, representing a user."""

    name: str
    uid: int
    gid: int
    comment: str
    home: str
    shell: str


def find_users(
    users=None, name=None, uid=None, gid=None, comment=None, home=None, shell=None
):
    """
    Return user that match the specified values.

    If no users match, an empty list is returned.

    If an argument is None, it's not used in the match. Otherwise a user must match all
    the specified values.
    """
    if not users:
        users = read_passwd()

    users = find(users, "name", name)
    users = find(users, "uid", sanitize_id(uid))
    users = find(users, "gid", sanitize_id(gid))
    users = find(users, "comment", comment)
    users = find(users, "home", home)
    users = find(users, "shell", shell)

    return users


def read_passwd():
    """Read the passwd file and returns a list of Users."""
    users = list()
    with open(current_app.config["PASSWD_PATH"]) as passwd_file:
        for line in passwd_file:
            (name, _, uid, gid, comment, home, shell) = [
                e.strip() for e in line.split(":")
            ]
            users.append(User(name, int(uid), int(gid), comment, home, shell))
    return users

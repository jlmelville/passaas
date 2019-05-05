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


def find_users(
    users=None, name=None, uid=None, gid=None, comment=None, home=None, shell=None
):
    """
    Return a list of users that match the specified values, or an empty list if none match.
    If an argument is None, it's not used in the match. Otherwise a user must match
    all the specified values.
    """
    if not users:
        users = read_passwd()
    if name:
        users = [u for u in users if u.name == name]
    if uid:
        uid = int(uid)
        users = [u for u in users if u.uid == uid]
    if gid:
        gid = int(gid)
        users = [u for u in users if u.gid == gid]
    if comment:
        users = [u for u in users if u.comment == comment]
    if home:
        users = [u for u in users if u.home == home]
    if shell:
        users = [u for u in users if u.shell == shell]

    return users


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

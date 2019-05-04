from typing import NamedTuple
from flask import current_app


class User(NamedTuple):
    name: str
    uid: int
    gid: int
    comment: str
    home: str
    shell: str


def read_passwd():
    users = list()
    with open(current_app.config["PASSWD_PATH"]) as passwd_file:
        for line in passwd_file:
            (name, _, uid, gid, comment, home, shell) = [
                e.strip() for e in line.split(":")
            ]
            users.append(User(name, int(uid), int(gid), comment, home, shell))
    return users

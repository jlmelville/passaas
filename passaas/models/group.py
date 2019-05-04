from typing import NamedTuple, Sequence
from flask import current_app


class Group(NamedTuple):
    name: str
    gid: int
    members: Sequence[str]


def read_group():
    """
    format is:
    name:x:gid:member1,member2...
    A group can have zero members
    """
    groups = list()
    with open(current_app.config["GROUP_PATH"]) as group_file:
        for line in group_file:
            (name, _, gid, members) = [e.strip() for e in line.split(":")]
            if members:
                members = members.split(",")
            else:
                members = []
            groups.append(Group(name, int(gid), members))
    return groups

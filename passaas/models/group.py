"""
The Group Model. Represents a Unix group and functions to read from a group file.
"""
from typing import NamedTuple, Sequence
from flask import current_app


class Group(NamedTuple):
    """
    A Unix group. Has a name, a group id (gid) and a list of members, represented by the user's
    name.
    """

    name: str
    gid: int
    members: Sequence[str]


def find_groups(groups=None, name=None, gid=None, member=None):
    """
    Returns a list of groups that match the specified values, or an empty list
    if no groups match. 'member' can be an array and is allowed to be a subset of
    the 'members' array associated with a group, i.e. if member == ['a', 'b'] and a
    given group has members == ['a', 'b', 'c'], then the member query will match that
    group.
    """
    if not groups:
        groups = read_group()
    if name:
        groups = [g for g in groups if g.name == name]
    if gid:
        gid = int(gid)
        groups = [g for g in groups if g.gid == gid]
    if member:
        for query_member in member:
            groups = [g for g in groups if query_member in g.members]

    return groups


def read_group():
    """
    Reads a group file and return a list of Group objects.

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

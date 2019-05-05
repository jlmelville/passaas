"""
Group Controller.
Functions mapping from HTTP requests for group-related resources to model data.
"""

from passaas.models.group import read_group


def fetch_all_groups():
    """
    Returns all groups or 404 if there aren't any.
    """
    groups = read_group()
    if groups:
        return [g._asdict() for g in groups]
    return ("No groups", 404)


def fetch_group(gid):
    """
    Returns the group with the specified gid, or 404 if there isn't one.
    """
    gid = int(gid)
    groups = read_group()
    groups = [g for g in groups if g.gid == gid]
    if groups:
        return groups[0]._asdict()
    return ("Not found", 404)


def query_groups(name=None, gid=None, member=None):
    """
    Returns the groups that match the specified values, or 404 if no groups match.
    member can be an array and is allowed to be a subset of the members array
    associated with a group, i.e. if member is ['a', 'b'] and a given group
    has members ['a', 'b', 'c'], then the member query will match that group.
    """
    groups = read_group()
    if name:
        groups = [g for g in groups if g.name == name]
    if gid:
        gid = int(gid)
        groups = [g for g in groups if g.gid == gid]
    if member:
        for query_member in member:
            groups = [g for g in groups if query_member in g.members]

    if groups:
        return [g._asdict() for g in groups]
    return ("No groups matched the query", 404)

"""
Group Controller.
Functions mapping from HTTP requests for group-related resources to model data.
"""

from passaas.models.group import find_groups
from passaas.controllers.util import to_response


def fetch_all_groups():
    """
    Returns all groups or 404 if there aren't any.
    """
    groups = find_groups()
    return to_response(groups, "No groups")


def fetch_group(gid):
    """
    Returns the group with the specified gid, or 404 if there isn't one.
    """
    groups = find_groups(gid=gid)
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
    groups = find_groups(name=name, gid=gid, member=member)

    return to_response(groups, "No groups matched the query")

"""
User controller.
Functions mapping from HTTP requests for user-related resources to model data.
"""

from passaas.models.user import read_passwd, find_users
from passaas.models.group import read_group


def fetch_all_users():
    """
    Returns all users, or 404 if there aren't any.
    """
    users = read_passwd()
    if users:
        return [u._asdict() for u in users]
    return ("No users", 404)


def fetch_user(uid):
    """
    Returns the user with the specified uid, or 404 if there aren't any.
    """
    users = find_users(read_passwd(), uid)
    if users:
        return users[0]._asdict()
    return ("Not found", 404)


def query_users(name=None, uid=None, gid=None, comment=None, home=None, shell=None):
    """
    Returns the user that match the specified values, or 404 if none match.
    If an argument is None, it's not used in the match. Otherwise a user must match
    all the specified values.
    """
    users = read_passwd()
    if name:
        users = [u for u in users if u.name == name]
    if uid:
        users = find_users(users, uid)
    if gid:
        gid = int(gid)
        users = [u for u in users if u.gid == gid]
    if comment:
        users = [u for u in users if u.comment == comment]
    if home:
        users = [u for u in users if u.home == home]
    if shell:
        users = [u for u in users if u.shell == shell]

    if users:
        return [u._asdict() for u in users]
    return ("No users matched the query", 404)


def fetch_groups_for_user(uid):
    """
    Returns the groups that the user, specified by uid is a member of,
    or 404 if a user with that uid doesn't exist, or if the user does
    exists, but does not belong to any groups.
    """
    # Get the user with the specified uid
    users = find_users(read_passwd(), uid)
    if not users:
        return ("Not found", 404)
    user = users[0]

    # Get the groups for that user (if any)
    groups = read_group()
    groups = [g._asdict() for g in groups if user.name in g.members]
    if groups:
        return groups
    return ("No groups", 404)

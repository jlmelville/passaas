# pylint: disable=too-many-arguments
"""
User controller.

Functions mapping from HTTP requests for user-related resources to model data.
"""

from passaas.models.user import find_users
from passaas.models.group import find_groups
from passaas.controllers.util import to_response


def fetch_all_users():
    """Return all users, or 404 if there aren't any."""
    users = find_users()
    return to_response(users, "No users")


def fetch_user(uid):
    """Return the user with the specified uid, or 404 if there isn't one."""
    users = find_users(uid=uid)
    if users:
        return users[0]._asdict()
    return ("Not found", 404)


def query_users(name=None, uid=None, gid=None, comment=None, home=None, shell=None):
    """
    Return the user that match the specified values, or 404 if none match.

    If an argument is None, it's not used in the match. Otherwise a user must match
    all the specified values.
    """
    # nosec is for a bandit false positive for shell=True
    users = find_users(
        name=name, uid=uid, gid=gid, comment=comment, home=home, shell=shell  # nosec
    )

    return to_response(users, "No users matched the query")


def fetch_groups_for_user(uid):
    """
    Return the groups that the user, specified by uid is a member of.

    Returns 404 if a user with that uid doesn't exist, or if the user does
    exist, but does not belong to any groups.
    """
    # Get the user with the specified uid
    users = find_users(uid=uid)
    if not users:
        return ("Not found", 404)
    user = users[0]

    # Get the groups for that user (if any)
    groups = find_groups(member=[user.name])

    return to_response(groups, "No groups")

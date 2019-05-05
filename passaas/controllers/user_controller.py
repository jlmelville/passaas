from passaas.models.user import read_passwd
from passaas.models.group import read_group


def fetch_all_users():
    users = read_passwd()
    if users:
        return [u._asdict() for u in users]
    return ("No users", 404)


def fetch_user(uid):
    uid = int(uid)
    users = read_passwd()
    users = [u for u in users if u.uid == uid]
    if users:
        return users[0]._asdict()
    return ("Not found", 404)


def query_users(name=None, uid=None, gid=None, comment=None, home=None, shell=None):
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

    if users:
        return [u._asdict() for u in users]
    return ("No users matched the query", 404)


def fetch_groups_for_user(uid):
    # Get the user with the specified uid
    uid = int(uid)
    users = read_passwd()
    users = [u for u in users if u.uid == uid]
    if not users:
        return ("Not found", 404)
    user = users[0]

    groups = read_group()
    groups = [g._asdict() for g in groups if user.name in g.members]
    if groups:
        return groups
    return ("No groups", 404)

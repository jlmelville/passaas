from passaas.models.user import read_passwd


def fetch_all_users():
    users = read_passwd()
    return [u._asdict() for u in users]


def fetch_user(uid):
    uid = int(uid)
    users = read_passwd()
    users = [u for u in users if u.uid == uid]
    if users:
        return users[0]._asdict()
    return ("Not found", 404)

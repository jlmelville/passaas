from passaas.models.user import read_passwd


def fetch_all_users():
    users = read_passwd()
    return [u._asdict() for u in users]

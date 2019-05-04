from passaas.models.group import read_group


def fetch_all_groups():
    groups = read_group()
    if groups:
        return [g._asdict() for g in groups]
    return ("No groups", 404)

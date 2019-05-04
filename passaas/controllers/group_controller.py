from passaas.models.group import read_group


def fetch_all_groups():
    groups = read_group()
    if groups:
        return [g._asdict() for g in groups]
    return ("No groups", 404)


def fetch_group(gid):
    gid = int(gid)
    groups = read_group()
    groups = [g for g in groups if g.gid == gid]
    if groups:
        return groups[0]._asdict()
    return ("Not found", 404)

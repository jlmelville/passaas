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


def query_groups(name=None, gid=None, member=[]):
    groups = read_group()
    if name:
        groups = [g for g in groups if g.name == name]
    if gid:
        gid = int(gid)
        groups = [g for g in groups if g.gid == gid]
    if member:
        for m in member:
            groups = [g for g in groups if m in g.members]

    if groups:
        return [g._asdict() for g in groups]
    return ("No groups matched the query", 404)

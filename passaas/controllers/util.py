"""Controller helper functions."""


def to_response(objects, not_found_msg):
    """
    Convert namedtuple objects to dict form.

    If the specified sequence of objects is non-empty, return the dict version of them.
    Otherwise return 404 and the specified message.

    NamedTuple objects need to be converted to a dictionary for to be serialized to
    JSON.
    """
    if objects:
        return [o._asdict() for o in objects]
    return (not_found_msg, 404)

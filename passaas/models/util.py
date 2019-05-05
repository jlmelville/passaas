"""
Model helper functions
"""


def sanitize_id(id):
    """
    Returns id as either an integer or None, if it is not convertible.
    """
    try:
        return int(id)
    except TypeError:
        return None


def find(objects, key, value):
    """
    Returns a list of all items in objects where the key attribute is equal to value.
    If value is None, objects is returned. If no objects match, an empty list is returned.
    """
    if value is None:
        return objects
    return [o for o in objects if getattr(o, key) == value]

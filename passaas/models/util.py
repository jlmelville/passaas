"""Model helper functions."""


def sanitize_id(int_id):
    """
    Return int_id as either an integer or None, if it is not convertible.

    For use with model find function where either integer or None is acceptable, but
    input from the controller is either a string representation of the integer or None.
    This handles the conversion and swallows the exception, making for a more "fluent"
    interface.

    Arguments:
        int_id {String or None} -- An id to convert. Can be None.

    Returns:
        {int or None} -- The converted id.

    """
    try:
        return int(int_id)
    except TypeError:
        return None


def find(objects, key, value):
    """
    Return a list of all items in objects where the key attribute is equal to value.

    If value is None, objects is returned. If no objects match, an empty list is
    returned.
    """
    if value is None:
        return objects
    return [o for o in objects if getattr(o, key) == value]

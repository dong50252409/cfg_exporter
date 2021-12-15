import re

re_trim = re.compile(r"\s+")
re_field_name = re.compile("^[a-zA-Z]([a-zA-Z0-9]|_)*")


def trim(s):
    """
    Removes all Spaces contained in the string.
    If the string is None, an empty string is returned.
    :param s:
    :return:
    """
    if s is None:
        return ""
    return re.sub(re_trim, "", s).lower()


def check_naming(s):
    """
    Check that the naming conforms to the specification.
    :param s:str
    :return:bool
    """
    if re.search(re_field_name, s):
        return True
    return False


__all__ = ('trim', 'check_naming')

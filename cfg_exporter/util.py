import re

re_trim = re.compile(r"\s+")
re_field_name = re.compile("^[a-zA-Z]([a-zA-Z0-9]|_)*")


def trim(s):
    if s is None:
        return ""
    return re.sub(re_trim, "", s).lower()


def check_named(s):
    if re.search(re_field_name, s):
        return True
    return False


__all__ = (
    "trim"
)

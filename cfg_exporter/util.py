import re

re_compile = re.compile(r"\s+")


def trim(s):
    if s is None:
        return ""
    return re.sub(re_compile, "", s).lower()

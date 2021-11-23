import re

re_compile = re.compile(r"\s+")


def trim(s):
    return re.sub(re_compile, "", s).lower()

import re

re_trim = re.compile(r"(\s|\n|\r)+")
re_trim_desc = re.compile(r"(\n|\r)+")
re_naming = re.compile(r"^[a-zA-Z]([a-zA-Z0-9]|_)*")


def trim(s):
    """
    去除字符串中所有的空白字符，以及回车符和换行符，如果字段是`None`类型，则返回空字符串.
    """
    if s is None:
        return ""
    return re.sub(re_trim, "", s).lower()


def trim_desc(s):
    """
    去除描述字符串中所有的回车符和换行符，如果字段是`None`类型，则返回空字符串.
    """
    if s is not None:
        return re.sub(re_trim_desc, "", s).lower()


def check_naming(s):
    """
    检查字符串命名是否符合规范
    """
    if re.search(re_naming, s):
        return True
    return False


__all__ = 'trim', 'check_naming'

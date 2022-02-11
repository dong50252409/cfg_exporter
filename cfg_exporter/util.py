import re
from cfg_exporter import StrOrNone
from cfg_exporter.tables.base.type import IgnoreValue

_re_trim = re.compile(r"(\s|\n|\r)+")
_re_trim_desc = re.compile(r"(\n|\r)+")
_re_naming = re.compile(r"^[a-zA-Z]([a-zA-Z0-9]|_)*")
_tab = {9: '\\t', 10: '\\n', 11: '\\x0b', 12: '\\x0c', 13: '\\r', 34: '\\"'}


def trim(s: StrOrNone) -> str:
    """
    去除字符串中所有的空白字符，以及回车符和换行符，如果字段是`None`类型，则返回空字符串.
    """
    return "" if s is None else re.sub(_re_trim, "", s).lower()


def trim_desc(s: StrOrNone) -> StrOrNone:
    """
    去除描述字符串中所有的回车符和换行符，如果字段是`None`类型，则返回`None`.
    """
    if s is not None:
        return re.sub(_re_trim_desc, "", s).lower()


def check_naming(s) -> bool:
    """
    检查字符串命名是否符合规范
    """
    return bool(re.match(_re_naming, s))


def escape(s: str) -> str:
    """
    将字符串转为原始字符串
    """
    return s.translate(_tab)


def iter_valid_value(kv_iter):
    """
    迭代有效值，过滤None、IgnoreValue
    """
    for key, value in kv_iter:
        if value is None or isinstance(value, IgnoreValue):
            continue
        yield key, value

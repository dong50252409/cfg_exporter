from enum import Enum

###############################
# 模板扩展名
###############################
TEMPLATE_EXTENSION = 'tmpl'

###############################
# 支持的数据类型定义
###############################
import cfg_exporter.util as util
from cfg_exporter.tables.base.type import LangType, RawType


class _Int:
    """
    32位整数
    """
    def __instancecheck__(self, instance):
        return isinstance(instance, int)

    def __call__(self, value):
        return int(value)


class _Int64(_Int):
    """
    64位整数类型
    """
    pass


class _Float:
    """
    浮点数类型
    """
    def __instancecheck__(self, instance):
        return isinstance(instance, float)

    def __call__(self, value):
        return float(value)


class _Str:
    """
    字符串类型
    """
    def __instancecheck__(self, instance):
        return isinstance(instance, str)

    def __call__(self, value):
        return util.escape(value)


class _Lang:
    """
    多语言类型
    """
    def __instancecheck__(self, instance):
        return isinstance(instance, LangType)

    def __call__(self, value):
        return LangType(util.escape(value))


class _Iter:
    """
    可迭代类型，目前仅包含 list、tuple
    """
    def __instancecheck__(self, instance):
        return isinstance(instance, (list, tuple))

    def __call__(self, value):
        iter_value = eval(value)
        isinstance(iter_value, (list, tuple))
        return iter_value


class _Raw:
    """
    原始类型
    """
    def __instancecheck__(self, instance):
        return isinstance(instance, RawType)

    def __call__(self, value):
        return RawType(value)


class DataType(Enum):
    """
    数据类型枚举
    """
    int = _Int()
    int64 = _Int64()
    float = _Float()
    str = _Str()
    lang = _Lang()
    iter = _Iter()
    raw = _Raw()

    def __instancecheck__(self, instance):
        return isinstance(instance, self.value)

    def __call__(self, value):
        return self.value(value)


###############################
# 支持的导出文件类型
###############################
from cfg_exporter.exports import erl_export, lua_export, py_export, json_export, csv_export, xlsx_export

ExportType = Enum('ExportType', {
    'erl': erl_export.ErlExport,
    'lua': lua_export.LuaExport,
    'py': py_export.PyExport,
    'json': json_export.JSONExport,
    'csv': csv_export.CSVExport,
    'xlsx': xlsx_export.XLSXExport,
})

###############################
# 支持导入的配置表类型
###############################
from cfg_exporter.tables import csv_table, xlsx_table

ExtensionType = Enum('Extension', {'csv': csv_table.CSVTable, 'xlsx': xlsx_table.XLSXTable})

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

# 数据类型细分分隔符
DATA_TYPE_DETAIL_SPLIT = ':'


class _Int:
    """
    整数
    """

    def __instancecheck__(self, instance):
        return isinstance(instance, int)

    def __call__(self, value):
        return int(value) if value else 0

    @property
    def real_type(self):
        return int


class _Float:
    """
    浮点数类型
    """

    def __instancecheck__(self, instance):
        return isinstance(instance, float)

    def __call__(self, value):
        return float(value) if value else 0.0

    @property
    def real_type(self):
        return float


class _Str:
    """
    字符串类型
    """

    def __instancecheck__(self, instance):
        return isinstance(instance, str)

    def __call__(self, value):
        return util.escape(value) if value else ''

    @property
    def real_type(self):
        return str


class _Lang:
    """
    多语言类型
    """

    def __instancecheck__(self, instance):
        return isinstance(instance, LangType)

    def __call__(self, value):
        return LangType(util.escape(value)) if value else LangType('')

    @property
    def real_type(self):
        return LangType


class _Iter:
    """
    可迭代类型，目前仅包含 list、tuple
    """

    def __instancecheck__(self, instance):
        return isinstance(instance, self.real_type)

    def __call__(self, value):
        if value:
            iter_value = eval(value)
            assert isinstance(iter_value, self.real_type)
            return iter_value
        return None

    @property
    def real_type(self):
        return list, tuple


class _Raw(_Str):
    """
    原始类型
    """

    def __instancecheck__(self, instance):
        return isinstance(instance, RawType)

    def __call__(self, value):
        return RawType(value) if value else None

    @property
    def real_type(self):
        return RawType


class DataType(Enum):
    """
    数据类型枚举
    """
    int = _Int()
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
from cfg_exporter.exports import erl_export, lua_export, py_export, cs_export, json_export, csv_export, xlsx_export

ExportType = Enum('ExportType', {
    'erl': erl_export.ErlExport,
    'lua': lua_export.LuaExport,
    'py': py_export.PyExport,
    'cs': cs_export.CSExport,
    'json': json_export.JSONExport,
    'csv': csv_export.CSVExport,
    'xlsx': xlsx_export.XLSXExport,
})

###############################
# 支持导入的配置表类型
###############################
from cfg_exporter.tables import csv_table, xlsx_table

ExtensionType = Enum('Extension', {'csv': csv_table.CSVTable, 'xlsx': xlsx_table.XLSXTable})

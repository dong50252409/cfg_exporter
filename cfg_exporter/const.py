from enum import Enum

###############################
# 模板扩展名
###############################
TEMPLATE_EXTENSION = 'tmpl'

###############################
# 支持的数据类型定义
###############################
from cfg_exporter.tables.base.raw import RawType
import cfg_exporter.util as util


class _Str:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


DataType = Enum('DataType', {
    'int': int, 'int64': int, 'float': float,
    'str': _Str(util.escape), 'iter': eval, 'raw': RawType
})

###############################
# 支持的导出文件类型
###############################
from cfg_exporter.exports import erl_export, lua_export, json_export, csv_export, xlsx_export

ExportType = Enum('ExportType', {
    'erl': erl_export.ErlExport,
    'lua': lua_export.LuaExport,
    'json': json_export.JSONExport,
    'csv': csv_export.CSVExport,
    'xlsx': xlsx_export.XLSXExport,
})

###############################
# 支持导入的配置表类型
###############################
from cfg_exporter.tables import csv_table, xlsx_table

ExtensionType = Enum('Extension', {'csv': csv_table.CSVTable, 'xlsx': xlsx_table.XLSXTable})

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


class DataType(Enum):
    class int(int):
        @staticmethod
        def convert(value):
            return int(value)

    class int64(int):
        pass

    class float(float):
        @staticmethod
        def convert(value):
            return float(value)

    class str(str):
        @staticmethod
        def convert(value):
            return util.escape(value)

    class lang(LangType):
        @staticmethod
        def convert(value):
            return LangType(util.escape(value))

    # TODO 自定义IterType类型
    class iter(object):
        @staticmethod
        def convert(value):
            return eval(value)

    class raw(RawType):
        @staticmethod
        def convert(value):
            return RawType(value)


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

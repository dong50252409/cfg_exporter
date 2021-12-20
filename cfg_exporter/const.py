from enum import Enum
from typing import Iterable

###############################
# 模板扩展名
###############################
TEMPLATE_EXTENSION = 'tmpl'

###############################
# 支持的数据类型定义
###############################
DataType = Enum('DataType', {'int': int, 'float': float, 'str': str, 'iter': Iterable})

###############################
# 支持的导出文件类型
###############################
from cfg_exporter.exports import erl_export
from cfg_exporter.exports import json_export

ExportType = Enum('ExportType', {
    'json': json_export.JSONExport,
    'erl': erl_export.ErlExport,
    'lua': None, 'proto': None
})

###############################
# 支持导入的配置表类型
###############################
from cfg_exporter.tables import csv_table, xlsx_table

ExtensionType = Enum('Extension', {'csv': csv_table.CSVTable, 'xlsx': xlsx_table.XLSXTable})

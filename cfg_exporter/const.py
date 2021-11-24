from enum import Enum

###############################
# 支持的导出文件类型
###############################
ExportType = Enum("ExportType", ("erl", "lua", "proto"))


###############################
# 支持导入的配置表类型
###############################
from cfg_exporter.tables.csv_table import CSVTable
from cfg_exporter.tables.xlsx_table import XLSXTable
ExtensionType = Enum("Extension", {"csv": CSVTable, "xlsx": XLSXTable})

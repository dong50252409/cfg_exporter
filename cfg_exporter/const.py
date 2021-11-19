# -*- coding: utf-8 -*-

from enum import Enum
from cfg_exporter.tables import csv_table, xlsx_table
from cfg_exporter.tables.base import table

# 支持的导出文件类型
ExportType = Enum("ExportTypes", ("erl", "lua", "proto"))

# 支持导入的配置表类型
ExtensionType = Enum("Extension", (csv_table.CSVTable, xlsx_table.XLSXTable))

# 支持的数据类型定义
DataType = Enum("DataTypes", {"int": int, "float": float, "str": str, "list": list, "tuple": tuple})

# 多条件切分符号
RuleSplitType = Enum("RuleSplitType",
                     {"split": "|", "clause_split": ":", "clause_ref_split": ".", "clause_range_split": "-"})

# 支持的检查规则定义 需要实现对应的Rule类
RuleType = Enum("RuleTypes", {
    "key": table.KeyRule, "macro": table.MacroType, "ref": table.RefRule,
    "len": table.LenRule, "range": table.RangeRule, "source": table.SourceRule,
    "unique": table.UniqueRule, "not_empty": table.NotEmptyRule
})

# 宏定义标记类型定义
MacroType = Enum("MacroType", ("name", "value", "desc"))

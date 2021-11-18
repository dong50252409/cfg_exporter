# -*- coding: utf-8 -*-

import enum

from csv_exporter import CSVTable
from xlsx_exporter import XLSXTable
from rule import KeyRule, MacroRule, RefRule, LenRule, RangeRule, SourceRule, UniqueRule, \
    NotEmptyRule

# 支持的导出文件类型
ExportTypes = enum.Enum("ExportTypes", ("erl", "lua", "proto"))

# 支持导入的配置表类型
Extension = enum.Enum("Extension", {"csv": CSVTable, "xlsx": XLSXTable})

# 多条件切分符号
RuleSplitType = enum.Enum("RuleSplitType", {
    "split": "|", "clause_split": ":",
    "clause_ref_split": ".", "clause_range_split": "-"
})

# 支持的检查规则定义 (规则类型，规则类名)
RuleTypes = enum.Enum("RuleTypes", {
    "key": KeyRule, "macro": MacroRule, "ref": RefRule,
    "len": LenRule, "range": RangeRule, "source": SourceRule,
    "unique": UniqueRule, "not_empty": NotEmptyRule
})

# 支持的数据类型定义
DataTypes = enum.Enum("DataTypes", {
    "int": int, "float": float,
    "str": str, "list": list, "tuple": tuple
})

# 宏定义标记类型定义
MacroType = enum.Enum("MacroType", ("name", "value", "desc"))

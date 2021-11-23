from enum import Enum


###############################
# 支持的数据类型定义
###############################
DataType = Enum("DataType", {"int": int, "float": float, "str": str, "list": list, "tuple": tuple})

###############################
# 宏定义标记类型定义
###############################
MacroType = Enum("MacroType", ("name", "value", "desc"))

###############################
# 支持的检查规则定义
###############################
from cfg_exporter.tables.base.rule import KeyRule, MacroRule, RefRule, LenRule, RangeRule, SourceRule, UniqueRule, \
    NotEmptyRule
RuleType = Enum("RuleType", {
    "key": KeyRule, "macro": MacroRule, "ref": RefRule,
    "len": LenRule, "range": RangeRule, "source": SourceRule,
    "unique": UniqueRule, "not_empty": NotEmptyRule
})

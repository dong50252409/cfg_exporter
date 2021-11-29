import os
from copy import copy
from enum import Enum
from cfg_exporter.const import DataType


class BaseRule(object):
    def __init__(self, column_obj, rule_str):
        self._column_obj = column_obj
        self._rule_str = rule_str
        self._value = None

    @property
    def column_obj(self):
        return self._column_obj

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, clause):
        self._value = clause

    def verify(self, _data_list):
        pass

    def _raise_rule_error(self, error):
        err = "%(row_num)s:%(column_num)s rule:`%(rule)s` %(error)s" % {
            "row_num": self._column_obj.table_obj.real_rule_row_num,
            "column_num": self._column_obj.real_column_num,
            "rule": self._rule_str,
            "error": error
        }
        raise RuleException(err)

    def _raise_body_error(self, row_num, error):
        err = "%(row_num)s:%(column_num)s rule:`%(rule)s` %(error)s" % {
            "row_num": self._column_obj.table_obj.real_body_row_num + row_num,
            "column_num": self._column_obj.real_column_num,
            "rule": self._rule_str,
            "error": error
        }
        raise RuleException(err)


class KeyRule(BaseRule):

    def __init__(self, column_obj, rule_str):
        super().__init__(column_obj, rule_str)

    @BaseRule.value.setter
    def value(self, clause):
        key_num = int(clause)
        global_key_rule = self._column_obj.table_obj.global_rules.get(self.__class__.__name__, GlobalKeyRule())

        if key_num in global_key_rule.values:
            err = "already defined at %(def_row_num)s:%(def_column_num)s" % {
                "def_row_num": self._column_obj.table_obj.real_rule_row_num,
                "def_column_num": global_key_rule.values[key_num] + 1
            }
            self._raise_rule_error(err)

        global_key_rule.values[key_num] = self._column_obj.column_num
        self._column_obj.table_obj.global_rules[self.__class__.__name__] = global_key_rule
        self._value = key_num


class MacroRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        if clause not in MacroType.__members__:
            self._raise_rule_error("is not exist")

        global_macro_rule = self._column_obj.table_obj.global_rules.get(self.__class__.__name__, GlobalMacroRule())

        if MacroType[clause] in global_macro_rule.values:
            err = "already defined at %(def_row_num)s:%(def_column_num)s" % {
                "def_row_num": self._column_obj.table_obj.real_rule_row_num,
                "def_column_num": global_macro_rule.values[MacroType[clause]] + 1
            }
            self._raise_rule_error(err)

        global_macro_rule.values[MacroType[clause]] = self._column_obj.column_num
        self._column_obj.table_obj.global_rules[self.__class__.__name__] = global_macro_rule
        self._value = MacroType[clause]


class RefRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        table_name, table_field = clause.split(".")
        self._value = (table_name, table_field)

    def verify(self, data_list):
        ref_table_obj = self._column_obj.table_obj.get_table_obj(self._value[0])
        if ref_table_obj:
            ref_column_obj = ref_table_obj.columns_by_field.get(self._value[1], None)
            if ref_column_obj:
                data_set = set(ref_column_obj.data_list)
                for row_nun, data in enumerate(data_list):
                    if data is not None and data not in data_set:
                        err = "data:`%(data)s` reference is not exist" % {"data": data}
                        self._raise_body_error(row_nun, err)
            else:
                err = "field:`%(field)s` is not exist" % {"field": self._value[1]}
                self._raise_rule_error(err)
        else:
            err = "table:`%(table)s` is not exist" % {"table": self._value[0]}
            self._raise_rule_error(err)


class LenRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        self._value = int(clause)

    def verify(self, data_list):
        for row_nun, data in enumerate(data_list):
            try:
                if data is not None and len(data) > self._value:
                    err = "data:`%(data)s` exceeds the length limit" % {"data": data}
                    self._raise_body_error(row_nun, err)
            except TypeError:
                err = "data_type:`%(data_type)s` is not match\n" \
                      "supported data types [%(support_data_type)s]" % {
                          "data_type": type(data).__name__,
                          "support_data_type": ",".join([DataType.str.name, DataType.iter.name])
                      }
                self._raise_rule_error(err)


class RangeRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        min_num, max_num = clause.split("-")
        min_num = int(min_num)
        max_num = int(max_num)
        assert min_num <= max_num
        self._value = (min_num, max_num)

    def verify(self, data_list):
        for row_nun, data in enumerate(data_list):
            try:
                if data is not None and not (self._value[0] <= data <= self._value[1]):
                    err = "data:`%(data)s` is out of range" % {"data": data}
                    self._raise_body_error(row_nun, err)
            except TypeError:
                err = "data_type:`%(data_type)s` is not match\n" \
                      "supported data types [%(support_data_type)s]" % {
                          "data_type": type(data).__name__,
                          "support_data_type": ",".join([DataType.str.name, DataType.iter.name])
                      }
                self._raise_rule_error(err)


class SourceRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        self._value = clause

    def verify(self, data_list):
        for row_nun, data in enumerate(data_list):
            if data is not None and not os.path.exists(os.path.join(self._value, data)):
                err = "data:`%(data)s` path not found" % {"data": data}
                self._raise_body_error(row_nun, err)


class UniqueRule(BaseRule):
    def verify(self, data_list):
        d = {}
        for row_nun, data in enumerate(data_list):
            if data is None:
                continue
            if data in d:
                err = "data:`%(data)s` is not unique already defined at %(row_num)s:%(column_num)s" % {
                    "data": data,
                    "row_num": self._column_obj.table_obj.real_body_row_num + d[data],
                    "column_num": self._column_obj.real_column_num
                }
                self._raise_body_error(row_nun, err)
            d[data] = row_nun


class NotEmptyRule(BaseRule):
    def verify(self, data_list):
        for row_nun, data in enumerate(data_list):
            if data is None:
                self._raise_body_error(row_nun, "data is empty")


class StructRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        rules, _ = parse_struct_clause(self._column_obj, clause)
        self._value = rules

    def verify(self, data_list):
        for rows in data_list:
            if rows is not None:
                self.__verify(rows, self._value)

    def __verify(self, data_list, rules):
        for index, rule_group in enumerate(rules):
            if isinstance(rule_group, list):
                self.__verify(data_list, rule_group)
            elif isinstance(rule_group, tuple):
                child_data_list = iter([d[index] for d in data_list]) if len(rules) > 1 else iter(data_list)
                for rule in rule_group:
                    if isinstance(rule, BaseRule):
                        rule.verify(copy(child_data_list))


class GlobalRule(object):
    def __init__(self):
        self._values = {}

    @property
    def values(self):
        return self._values

    def verify(self, _table_obj):
        pass


class GlobalKeyRule(GlobalRule):
    def verify(self, table_obj):
        column_num_list = sorted(self._values.values())
        data_lists = [table_obj.columns[col_num].data_list for col_num in column_num_list]
        key_set = set()
        for row_nun, data in enumerate(zip(*data_lists)):
            for col_num, d in enumerate(data):
                if d is None:
                    err = "%(row_num)s:%(column_num)s primary key is empty" % {
                        "row_num": table_obj.real_body_row_num + row_nun,
                        "column_num": column_num_list[col_num] + 1
                    }
                    raise RuleException(err)
            if data in key_set:
                err = "%(row_num)s:%(column_num)s primary key repeat" % {
                    "row_num": table_obj.real_body_row_num + row_nun,
                    "column_num": ",".join([str(col_num + 1) for col_num in column_num_list])
                }
                raise RuleException(err)
            key_set.add(data)


class GlobalMacroRule(GlobalRule):
    def verify(self, table_obj):
        if MacroType.name not in self._values:
            raise RuleException("rule:`macro:name` is not exist")

        if MacroType.value not in self._values:
            raise RuleException("rule:`macro:value` is not exist")

        column_num = self._values[MacroType.name]
        column_obj = table_obj.columns[column_num]
        if column_obj.data_type is not DataType.str:
            err = "%(row_num)s:%(column_num)s rule:`macro:name` data type is not `str`" % {
                "row_num": table_obj.real_rule_row_num,
                "column_num": column_num + 1
            }
            raise RuleException(err)

        macro_name_set = set()
        for row_nun, data in enumerate(column_obj.data_list):
            if data is None:
                continue
            if data in macro_name_set:
                err = "%(row_num)s:%(column_num)s macro name repeat" % {
                    "row_num": table_obj.real_body_row_num + row_nun,
                    "column_num": column_num + 1
                }
                raise RuleException(err)
            macro_name_set.add(data)


class RuleException(Exception):

    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


def create_rule_obj(column_obj, rule_str):
    # 规则条件有两种类型 tag、tag:clause
    tag_and_clause = rule_str.split(":", 1)
    assert len(tag_and_clause) <= 2
    cls = RuleType[tag_and_clause[0]].value
    rule_obj = type(cls.__name__, (cls,), dict())(column_obj, rule_str)
    rule_obj.value = tag_and_clause[-1]
    return rule_obj


def parse_rules(column_obj, rule_str):
    rules = []
    for each_rule in iter_rule(rule_str):
        try:
            rule_obj = create_rule_obj(column_obj, each_rule)
            rules.append(rule_obj)
        except (AssertionError, ValueError, KeyError):
            err = "%(row_num)s:%(column_num)s rule:`%(rule)s` formal error" % {
                "row_num": column_obj.table_obj.real_rule_row_num,
                "column_num": column_obj.real_column_num,
                "rule": each_rule,
            }
            raise RuleException(err)
    return rules


def iter_rule(rules):
    start_index, cur_index, rules_len = 0, 1, len(rules)
    while cur_index <= rules_len:
        rule_str = rules[start_index:cur_index]
        if rule_str in RuleType.__members__:
            if rule_str == RuleType.struct.name:
                last_pos = find_struct_last_position(rules[start_index:])
            else:
                last_pos = find_other_last_position(rules[start_index:])
            last_pos = start_index + last_pos
            yield rules[start_index:last_pos]
            start_index, cur_index = last_pos + 1, last_pos + 1
        cur_index += 1


def find_struct_last_position(clause):
    symbol_count = 0
    for index, c in enumerate(clause, start=1):
        if c == "[" or c == "(":
            symbol_count += 1
            continue

        if c == "]" or c == ")":
            symbol_count -= 1
            if symbol_count == 0:
                return index


def find_other_last_position(clause):
    index, clause_len = 0, len(clause)
    while index < clause_len:
        if clause[index] == "|":
            return index
        index += 1
    return index


def parse_struct_clause(column_obj, clause, index=0, rules=None):
    clause_len = len(clause)
    while index < clause_len:
        c = clause[index]
        if c == "[" or c == "(":
            index += 1
            child_rules, last_index = parse_struct_clause(column_obj, clause, index, [])
            if rules is None:
                rules = child_rules
            else:
                rules.append(child_rules)
            index = last_index
        elif c == "]" or c == ")":
            index += 1
            break
        elif c == ",":
            index += 1
        else:
            child_rules, last_index = parse_struct_clause_1(column_obj, clause[index:])
            rules.append(child_rules)
            index += last_index
    return rules, index


def parse_struct_clause_1(column_obj, clause):
    rules, start_index, last_index, clause_str = [], 0, 0, len(clause)
    while last_index < clause_str:
        c = clause[last_index]
        if c == "|":
            rule_obj = create_rule_obj(column_obj, clause[start_index:last_index])
            rules.append(rule_obj)
            start_index = last_index + 1
        elif c == "," or c == "]" or c == ")":
            rule_obj = create_rule_obj(column_obj, clause[start_index:last_index])
            rules.append(rule_obj)
            return tuple(rules), last_index
        last_index += 1


###############################
# 规则标记类型定义
###############################
RuleType = Enum("RuleType", {
    "key": KeyRule, "macro": MacroRule, "ref": RefRule,
    "len": LenRule, "range": RangeRule, "source": SourceRule,
    "unique": UniqueRule, "not_empty": NotEmptyRule, "struct": StructRule
})

###############################
# 宏定义标记类型定义
###############################
MacroType = Enum("MacroType", ("name", "value", "desc"))

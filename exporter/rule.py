# -*- coding: utf-8 -*-
import os
import const
from collections import Counter


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

    def verify(self):
        pass

    def _raise(self, row):
        raise RuleException("row:%(row)s %(rule)s verification failed" % {"row": row, "rule": self._rule_str})


class KeyRule(BaseRule):

    def __init__(self, column_obj, rule_str):
        super().__init__(column_obj, rule_str)

    @BaseRule.value.setter
    def value(self, clause):
        key_num = int(clause)
        global_key_rule = self._column_obj.table_obj.global_rules.get(self.__class__.__name__, GlobalKeyRule())
        assert key_num not in global_key_rule.value_list
        global_key_rule.value_list.append(key_num)
        global_key_rule.column_num_list.append(self._column_obj.column_num)
        self._column_obj.table_obj.global_rules[self.__class__.__name__] = global_key_rule
        self._value = key_num


class MacroRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        assert clause in const.MacroType.__members__
        global_macro_rule = self._column_obj.table_obj.global_rules.get(self.__class__.__name__, GlobalMacroRule())
        assert const.MacroType[clause] not in global_macro_rule.value_list
        global_macro_rule.value_list.append(const.MacroType[clause])
        global_macro_rule.column_num_list.append(self._column_obj.column_num)
        self._column_obj.table_obj.global_rules[self.__class__.__name__] = global_macro_rule
        self._value = const.MacroType[clause]


class RefRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        table_name, table_field = clause.split(const.RuleSplitType.clause_range_split.value)
        self._value = (table_name, table_field)

    def verify(self):
        ref_table_obj = self._column_obj.table_obj.get_table_obj(self._value[0])
        if ref_table_obj:
            ref_column_obj = ref_table_obj.columns_by_field.get(self._value[1], None)
            if ref_column_obj:
                data_set = set(ref_column_obj.data_list)
                for row_nun, data in enumerate(self._column_obj.data_list):
                    if data not in data_set:
                        super()._raise(row_nun)
            else:
                err = "field %(table_field)s in table %(table_name)s does not exists  " % \
                      {"table_name": self._value[0], "table_field": self._value[1]}
                raise RuleException(err)
        else:
            raise RuleException("table %(table_name)s does not exists" % {"table_name": self._value[0]})


class LenRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        self._value = int(clause)

    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data and len(data) > self._value:
                super()._raise(row_nun)


class RangeRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        min_num, max_num = clause.split(const.RuleSplitType.clause_range_split.value)
        min_num = int(min_num)
        max_num = int(max_num)
        assert min_num >= max_num
        self._value = (min_num, max_num)

    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data and not (self._value[0] <= data <= self._value[1]):
                super()._raise(row_nun)


class SourceRule(BaseRule):
    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data and not os.path.exists(os.path.join(self._value, data)):
                super()._raise(row_nun)


class UniqueRule(BaseRule):
    def verify(self):
        d = Counter(self._column_obj.data_list)
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data and d[data] != 1:
                super()._raise(row_nun)


class NotEmptyRule(BaseRule):
    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data is None:
                super()._raise(row_nun)


class GlobalRule(object):
    def __init__(self):
        self._value_list = []
        self._column_num_list = []

    @property
    def value_list(self):
        return self._value_list

    @property
    def column_num_list(self):
        return self._column_num_list

    def verify(self, _table_obj):
        pass


class GlobalKeyRule(GlobalRule):
    def verify(self, table_obj):
        self._column_num_list.sort()
        data_lists = [table_obj.columns[col_num].data_list for col_num in self._column_num_list]
        key_set = set()
        for row_nun, data in enumerate(zip(*data_lists)):
            if data in key_set:
                err = "column:%(column)s row:%(row)s primary key repeat" % \
                      {"column": self._column_num_list, "row": table_obj.body_row_num + row_nun}
                raise RuleException(err)
            key_set.add(data)


class GlobalMacroRule(GlobalRule):
    def verify(self, table_obj):
        if const.MacroType["name"] not in self._value_list:
            raise RuleException("column macro:name does not exist")

        if const.MacroType["value"] not in self._value_list:
            raise RuleException("column macro:value does not exist")

        for macro, col_num in zip(self._value_list, self._column_num_list):
            if macro is const.MacroType["name"] and not table_obj.columns[col_num].data_type is str:
                raise RuleException("column:%(column)s macro:name data type is not str" % {"column": col_num})


class RuleException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err

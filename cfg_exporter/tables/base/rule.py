import os
from enum import Enum
from typing import Sized

from cfg_exporter.const import DataType


class BaseRule(object):
    def __init__(self, table_obj, column_num, rule_str):
        self._table_obj = table_obj
        self._column_num = column_num
        self._rule_str = rule_str
        self._value = None

    @property
    def table_obj(self):
        return self.table_obj

    @property
    def column_num(self):
        return self._column_num

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, clause):
        self._value = clause

    def verify(self, _column_data_iter):
        pass

    def _raise_rule_error(self, error):
        raise RuleException(f'rule:`{self._rule_str}` {error}')

    def _raise_body_error(self, row_num, error):
        err = '%(row_num)s:%(column_num)s rule:`%(rule)s` %(error)s' % {
            'row_num': self._table_obj.data_row_num + row_num,
            'column_num': self._column_num + 1,
            'rule': self._rule_str,
            'error': error
        }
        raise RuleException(err)


class KeyRule(BaseRule):

    def __init__(self, table_obj, column_num, rule_str):
        super().__init__(table_obj, column_num, rule_str)

    @BaseRule.value.setter
    def value(self, clause):
        key_num = int(clause)
        global_key_rule = self._table_obj.global_rules.get(self.__class__.__name__, GlobalKeyRule())

        if key_num in global_key_rule.values:
            err = f'already defined at {self._table_obj.rule_row_num}:{global_key_rule.values[key_num] + 1}'
            self._raise_rule_error(err)

        global_key_rule.values[key_num] = self._column_num
        self._table_obj.global_rules[self.__class__.__name__] = global_key_rule
        self._value = key_num


class MacroRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        if clause not in MacroType.__members__:
            self._raise_rule_error('does not exist')

        global_macro_rule = self._table_obj.global_rules.get(self.__class__.__name__, GlobalMacroRule())

        if MacroType[clause] in global_macro_rule.values:
            err = f'already defined at {self._table_obj.rule_row_num}:{global_macro_rule.values[MacroType[clause]] + 1}'
            self._raise_rule_error(err)

        global_macro_rule.values[MacroType[clause]] = self._column_num
        self._table_obj.global_rules[self.__class__.__name__] = global_macro_rule
        self._value = MacroType[clause]


class RefRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        table_name, table_field = clause.split('.')
        self._value = (table_name, table_field)

    def verify(self, column_data_iter):
        ref_table_obj = self._table_obj.get_table_obj(self._value[0])
        if ref_table_obj is None:
            self._raise_rule_error(f'table:`{self._value[0]}` does not exist')

        ref_column_data_iter = ref_table_obj.data_iter_by_field_name(self._value[1])
        if ref_column_data_iter is None:
            self._raise_rule_error(f'field:`{self._value[1]}` does not exist')

        data_set = set(ref_column_data_iter)
        for row_nun, data in enumerate(column_data_iter):
            if data is None:
                continue

            if data not in data_set:
                self._raise_body_error(row_nun, f'data:`{data}` reference does not exist')


class LenRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        self._value = int(clause)

    def verify(self, column_data_iter):
        for row_nun, data in enumerate(column_data_iter):
            if data is None:
                continue

            if not isinstance(data, Sized):
                self._raise_rule_error(f'data:`{data}` the data type does not `Sized`')

            if len(data) > self._value:
                self._raise_body_error(row_nun, f'data:`{data}` exceeds the length limit')


class RangeRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        min_num, max_num = clause.split('-')
        min_num = int(min_num)
        max_num = int(max_num)
        assert min_num <= max_num
        self._value = (min_num, max_num)

    def verify(self, column_data_iter):
        for row_nun, data in enumerate(column_data_iter):
            if data is None:
                continue

            if type(data) in (int, float):
                if not (self._value[0] <= data <= self._value[1]):
                    self._raise_body_error(row_nun, f'data:`{data}` is out of range')

            elif isinstance(data, Sized):
                if not (self._value[0] <= len(data) <= self._value[1]):
                    self._raise_body_error(row_nun, f'data:`{data}` is out of range')


class SourceRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        self._value = clause

    def verify(self, column_data_iter):
        for row_nun, data in enumerate(column_data_iter):
            if data is None:
                continue

            if not os.path.exists(os.path.join(self._value, data)):
                self._raise_body_error(row_nun, f'data:`{data}` path not found')


class UniqueRule(BaseRule):
    def verify(self, column_data_iter):
        d = {}
        for row_nun, data in enumerate(column_data_iter):
            if data is None:
                continue

            if data in d:
                err = f'data:`{data}` is not unique already defined at ' \
                      f'{self._table_obj.data_row_num + d[data]}:{self._column_num + 1}'
                self._raise_body_error(row_nun, err)
            d[data] = row_nun


class NotEmptyRule(BaseRule):
    def verify(self, column_data_iter):
        for row_nun, data in enumerate(column_data_iter):
            if data is None:
                self._raise_body_error(row_nun, 'the data is empty')


class StructRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        rules, _ = parse_struct_clause(self._table_obj, self._column_num, clause)
        self._value = rules

    def verify(self, column_data_iter):
        for data in column_data_iter:
            if data is not None:
                self.__verify(data, self._value)

    def __verify(self, cell_data, rules):
        for index, rule_group in enumerate(rules):
            if isinstance(rule_group, list):
                self.__verify(cell_data, rule_group)
            elif isinstance(rule_group, tuple):
                for rule in rule_group:
                    if isinstance(rule, BaseRule):
                        if len(rules) > 1:
                            child_column_data_iter = self.__child_column_data_iter(cell_data, index)
                        else:
                            child_column_data_iter = cell_data
                        rule.verify(child_column_data_iter)

    @staticmethod
    def __child_column_data_iter(cell_data, index):
        for data in cell_data:
            yield data[index]


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
        column_data_iter_list = [table_obj.data_iter_by_column_num(col_num) for col_num in column_num_list]
        key_set = set()
        for row_nun, data in enumerate(zip(*column_data_iter_list)):
            for col_num, d in enumerate(data):
                if d is None:
                    err = f'{table_obj.data_row_num + row_nun}:{column_num_list[col_num] + 1} primary key is empty'
                    raise RuleException(err)

            if data in key_set:
                err = '%(row_num)s:%(column_num)s primary key repeat' % {
                    'row_num': table_obj.data_row_num + row_nun,
                    'column_num': ','.join([str(col_num + 1) for col_num in column_num_list])
                }
                raise RuleException(err)
            key_set.add(data)


class GlobalMacroRule(GlobalRule):
    def verify(self, table_obj):
        if MacroType.name not in self._values:
            raise RuleException('rule:`macro:name` does not exist')

        if MacroType.value not in self._values:
            raise RuleException('rule:`macro:value` does not exist')

        column_num = self._values[MacroType.name]
        data_type = table_obj.data_type_by_column_num(column_num)
        if data_type is not DataType.str:
            raise RuleException(f'{table_obj.rule_row_num}:{column_num + 1} rule:`macro:name` data type is not `str`')

        macro_name_set = set()
        column_data_iter = table_obj.data_iter_by_column_num(column_num)
        for row_nun, data in enumerate(column_data_iter):
            if data is None:
                continue

            if data in macro_name_set:
                raise RuleException(f'{table_obj.data_row_num + row_nun}:{column_num + 1} macro name repeat')
            macro_name_set.add(data)


class RuleException(Exception):

    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


def create_rule_obj(table_obj, column_num, rule_str):
    # 规则条件有两种类型 tag、tag:clause
    tag_and_clause = rule_str.split(':', 1)
    assert len(tag_and_clause) <= 2
    cls = RuleType[tag_and_clause[0]].value
    rule_obj = type(cls.__name__, (cls,), dict())(table_obj, column_num, rule_str)
    rule_obj.value = tag_and_clause[-1]
    return rule_obj


def parse_rules(table_obj, column_num, rules):
    rule_list = []
    for each_rule in iter_rule(rules):
        try:
            rule_obj = create_rule_obj(table_obj, column_num, each_rule)
            rule_list.append(rule_obj)
        except (AssertionError, ValueError, KeyError):
            raise RuleException(f'rule:`{each_rule}` formal error')
    return rule_list


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
        if c == '[' or c == '(':
            symbol_count += 1
            continue

        if c == ']' or c == ')':
            symbol_count -= 1
            if symbol_count == 0:
                return index


def find_other_last_position(clause):
    index, clause_len = 0, len(clause)
    while index < clause_len:
        if clause[index] == '|':
            return index
        index += 1
    return index


def parse_struct_clause(table_obj, column_num, clause, index=0, rules=None):
    clause_len = len(clause)
    while index < clause_len:
        c = clause[index]
        if c == '[' or c == '(':
            index += 1
            child_rules, last_index = parse_struct_clause(table_obj, column_num, clause, index, [])
            if rules is None:
                rules = child_rules
            else:
                rules.append(child_rules)
            index = last_index
        elif c == ']' or c == ')':
            index += 1
            break
        elif c == ',':
            index += 1
        else:
            child_rules, last_index = parse_struct_clause_1(table_obj, column_num, clause[index:])
            rules.append(child_rules)
            index += last_index
    return rules, index


def parse_struct_clause_1(table_obj, column_num, clause):
    rules, start_index, last_index, clause_str = [], 0, 0, len(clause)
    while last_index < clause_str:
        c = clause[last_index]
        if c == '|':
            rule_obj = create_rule_obj(table_obj, column_num, clause[start_index:last_index])
            rules.append(rule_obj)
            start_index = last_index + 1
        elif c == ',' or c == ']' or c == ')':
            rule_obj = create_rule_obj(table_obj, column_num, clause[start_index:last_index])
            rules.append(rule_obj)
            return tuple(rules), last_index
        last_index += 1


###############################
# 宏定义标记类型定义
###############################
MacroType = Enum('MacroType', ('name', 'value', 'desc'))

###############################
# 规则标记类型定义
###############################
RuleType = Enum('RuleType', {
    'key': KeyRule, 'macro': MacroRule, 'ref': RefRule,
    'len': LenRule, 'range': RangeRule, 'source': SourceRule,
    'unique': UniqueRule, 'not_empty': NotEmptyRule, 'struct': StructRule
})

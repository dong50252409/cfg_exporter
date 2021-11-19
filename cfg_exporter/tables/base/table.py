# -*- coding: utf-8 -*-

import os
from collections import Counter
from cfg_exporter import util
from cfg_exporter.const import DataType, RuleSplitType, MacroType, RuleType


class Table(object):
    def __init__(self, container_obj, filename, field_row, type_row, rule_row, desc_row, body_row):
        self.__container_obj = container_obj
        self.__full_filename = os.path.abspath(filename)
        self.__field_row = field_row
        self.__type_row = type_row
        self.__rule_row = rule_row
        self.__desc_row = desc_row
        self.__body_row = body_row
        self.__columns = {}
        self.__columns_by_field = {}
        self.__global_rules = {}
        self.__is_load = False

    def _load_column(self, rows):
        try:
            body = rows[self.body_row_num:]
            for col_num, field_name in enumerate(rows[self.__field_row]):
                column = Column(self, col_num)
                column.field_name = field_name
                column.data_type = rows[self.__type_row][col_num]
                if self.__rule_row is not None:
                    column.rules = rows[self.__rule_row][col_num]
                if self.__desc_row is not None:
                    column.description = rows[self.__desc_row][col_num]
                column.data_list = body
                self.__columns[col_num] = column
                self.__columns_by_field[field_name] = column
            self.__is_load = True
        except ColumnException as e:
            err = "table:%(table_name)s %(error)s" % {"table_name": self.table_name, "error": e.err}
            raise TableException(err)

    def get_table_obj(self, full_filename):
        return self.__container_obj.get_table_obj(full_filename)

    @property
    def full_filename(self):
        return self.__full_filename

    @property
    def filename(self):
        return os.path.basename(self.__full_filename)

    @property
    def table_name(self):
        return os.path.splitext(os.path.basename(self.__full_filename))[0]

    @property
    def field_name_row_num(self):
        return self.__field_row

    @property
    def data_type_row_num(self):
        return self.__type_row

    @property
    def body_row_num(self):
        return self.__body_row

    @property
    def rule_row_num(self):
        return self.__rule_row

    @property
    def description_row_num(self):
        return self.__desc_row

    @property
    def columns(self):
        return self.__columns

    @property
    def columns_by_field(self):
        return self.__columns_by_field

    @property
    def global_rules(self):
        return self.__global_rules

    @property
    def is_load(self):
        return self.__is_load

    def verify(self):
        for column in self.__columns.values():
            column.verify()
        for global_rule in self.__global_rules.values():
            global_rule.verify(self)

    def export(self):
        pass


class TableException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


class Column(object):
    def __init__(self, table_obj, column_num):
        self.__table_obj = table_obj
        self.__column_num = column_num
        self.__field_name = None
        self.__data_type = None
        self.__rules = []
        self.__description = None
        self.__data_list = []

    @property
    def table_obj(self):
        return self.__table_obj

    @property
    def column_num(self):
        return self.__column_num

    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, field_name):
        if field_name is None:
            err = "column:%(column)s field name is undefined" % {"column": self.__column_num + 1}
            raise ColumnException(err)

        field_name = util.trim(field_name)

        if field_name == "":
            err = "column:%(column)s field name is undefined" % {"column": self.__column_num + 1}
            raise ColumnException(err)

        self.__field_name = util.trim(field_name)

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        if data_type is None:
            err = "column:%(column)s data type is undefined" % {"column": self.__column_num + 1}
            raise ColumnException(err)

        data_type = util.trim(data_type)

        if data_type == "":
            err = "column:%(column)s data type is undefined" % {"column": self.__column_num + 1}
            raise ColumnException(err)

        if data_type not in DataType.__members__:
            error = "column:%(column)s data type %(data_type)s is unsupported " \
                    "supported data types [%(support_data_type)s]" % \
                    {"column": self.__column_num + 1, "data_type": data_type,
                     "support_data_type": ",".join(DataType.__members__.keys())}
            raise ColumnException(error)

        self.__data_type = DataType[data_type].value

    @property
    def rules(self):
        return self.__rules

    @rules.setter
    def rules(self, rule):
        if rule is None or rule == "":
            return

        rule = util.trim(rule)

        if rule != "":
            for rule_str in rule.split(RuleSplitType.split.value):
                try:
                    # 规则条件有两种类型 tag、tag:clause
                    tag_and_clause = rule_str.split(RuleSplitType.clause_split.value)
                    assert len(tag_and_clause) <= 2
                    cls = RuleType[tag_and_clause[0]].value
                    rule_obj = type(cls.__name__, (cls,), dict())(self, rule_str)
                    rule_obj.value = tag_and_clause[-1]
                    self.__rules.append(rule_obj)
                except (AssertionError, ValueError, KeyError):
                    error = "column:%(column_num)s incorrect rule %(rule)s" % \
                            {"column_num": self.column_num + 1, "rule": rule_str}
                    raise ColumnException(error)
            self.__rules = tuple(self.__rules)

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, desc):
        if desc is None:
            return
        self.__description = util.trim(desc)

    @property
    def data_list(self):
        return self.__data_list

    @data_list.setter
    def data_list(self, rows):
        for row_num, row in enumerate(rows):
            if row[self.__column_num]:
                if self.__data_type is list or self.__data_type is tuple:
                    try:
                        data = eval(row[self.__column_num])
                        assert isinstance(data, self.__data_type)
                    except (SyntaxError, NameError, AssertionError):
                        error = "column:%(column_num)s row:%(row_num)s incorrect data %(data)s" % \
                                {"column_num": self.column_num + 1, "row_num": row_num, "data": row[self.__column_num]}
                        raise ColumnException(error)
                else:
                    data = self.__data_type(row[self.__column_num])
                self.__data_list.append(data)
            else:
                self.__data_list.append(None)
        self.__data_list = tuple(self.__data_list)

    def verify(self):
        for rule in self.__rules:
            try:
                rule.verify()
            except RuleException as e:
                error = "column:%(column_num)s %(err)s" % {"column_num": self.column_num + 1, "err": e.err}
                raise ColumnException(error)


class ColumnException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


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
        assert clause in MacroType.__members__
        global_macro_rule = self._column_obj.table_obj.global_rules.get(self.__class__.__name__, GlobalMacroRule())
        assert MacroType[clause] not in global_macro_rule.value_list
        global_macro_rule.value_list.append(MacroType[clause])
        global_macro_rule.column_num_list.append(self._column_obj.column_num)
        self._column_obj.table_obj.global_rules[self.__class__.__name__] = global_macro_rule
        self._value = MacroType[clause]


class RefRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        table_name, table_field = clause.split(RuleSplitType.clause_range_split.value)
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
        min_num, max_num = clause.split(RuleSplitType.clause_range_split.value)
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
        if MacroType["name"] not in self._value_list:
            raise RuleException("column macro:name does not exist")

        if MacroType["value"] not in self._value_list:
            raise RuleException("column macro:value does not exist")

        for macro, col_num in zip(self._value_list, self._column_num_list):
            if macro is MacroType["name"] and not table_obj.columns[col_num].data_type is str:
                raise RuleException("column:%(column)s macro:name data type is not str" % {"column": col_num})


class RuleException(Exception):

    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err

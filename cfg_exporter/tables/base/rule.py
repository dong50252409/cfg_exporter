import os
from cfg_exporter.tables.base.const import MacroType, DataType


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

    def verify(self):
        ref_table_obj = self._column_obj.table_obj.get_table_obj(self._value[0])
        if ref_table_obj:
            ref_column_obj = ref_table_obj.columns_by_field.get(self._value[1], None)
            if ref_column_obj:
                data_set = set(ref_column_obj.data_list)
                for row_nun, data in enumerate(self._column_obj.data_list):
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
        assert self._column_obj.data_type in (DataType.str.value, DataType.list.value, DataType.tuple.value)
        self._value = int(clause)

    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data is not None and len(data) > self._value:
                err = "data:`%(data)s` exceeds the length limit" % {"data": data}
                self._raise_body_error(row_nun, err)


class RangeRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        assert self._column_obj.data_type in (DataType.int.value, DataType.float.value)
        min_num, max_num = clause.split("-")
        min_num = int(min_num)
        max_num = int(max_num)
        assert min_num <= max_num
        self._value = (min_num, max_num)

    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data is not None and not (self._value[0] <= data <= self._value[1]):
                err = "data:`%(data)s` is out of range" % {"data": data}
                self._raise_body_error(row_nun, err)


class SourceRule(BaseRule):

    @BaseRule.value.setter
    def value(self, clause):
        assert self._column_obj.data_type is DataType.str.value
        self._value = clause

    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data is not None and not os.path.exists(os.path.join(self._value, data)):
                err = "data:`%(data)s` path not found" % {"data": data}
                self._raise_body_error(row_nun, err)


class UniqueRule(BaseRule):
    def verify(self):
        d = {}
        for row_nun, data in enumerate(self._column_obj.data_list):
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
    def verify(self):
        for row_nun, data in enumerate(self._column_obj.data_list):
            if data is None:
                self._raise_body_error(row_nun, "data is empty")


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
        if column_obj.data_type is not DataType.str.value:
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

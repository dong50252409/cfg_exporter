# -*- coding: utf-8 -*-
import const
from rule import RuleException
from util import trim


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

        field_name = trim(field_name)

        if field_name == "":
            err = "column:%(column)s field name is undefined" % {"column": self.__column_num + 1}
            raise ColumnException(err)

        self.__field_name = trim(field_name)

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        if data_type is None:
            err = "column:%(column)s data type is undefined" % {"column": self.__column_num + 1}
            raise ColumnException(err)

        data_type = trim(data_type)

        if data_type == "":
            err = "column:%(column)s data type is undefined" % {"column": self.__column_num + 1}
            raise ColumnException(err)

        if data_type not in const.DataTypes.__members__:
            error = "column:%(column)s data type %(data_type)s is unsupported " \
                    "supported data types [%(support_data_type)s]" % \
                    {"column": self.__column_num + 1, "data_type": data_type,
                     "support_data_type": ",".join(const.DataTypes.__members__.keys())}
            raise ColumnException(error)

        self.__data_type = const.DataTypes[data_type].value

    @property
    def rules(self):
        return self.__rules

    @rules.setter
    def rules(self, rule):
        if rule is None or rule == "":
            return

        rule = trim(rule)

        if rule != "":
            for rule_str in rule.split(const.RuleSplitType.split.value):
                try:
                    # 规则条件有两种类型 tag、tag:clause
                    tag_and_clause = rule_str.split(const.RuleSplitType.clause_split.value)
                    assert len(tag_and_clause) <= 2
                    cls = const.RuleTypes.__members__[tag_and_clause[0]].value
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
        self.__description = trim(desc)

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

import os
from typing import Iterable

import cfg_exporter.util as util
from itertools import zip_longest

from cfg_exporter.const import DataType
from cfg_exporter.tables.base.column import Column, ColumnException
from cfg_exporter.tables.base.rule import RuleException, parse_rules

FIELD_NAME_INDEX, DATA_TYPE_INDEX, RULE_INDEX, DESC_INDEX, DATA_INDEX = range(5)


class Table(object):
    def __init__(self, container_obj, filename, **kwargs):
        self.__container_obj = container_obj
        self.__full_filename = os.path.abspath(filename)
        self.__field_row = kwargs["field_row"] - 1
        self.__type_row = kwargs["type_row"] - 1
        self.__rule_row = None
        if "rule_row" in kwargs:
            self.__rule_row = kwargs["rule_row"] - 1
        self.__desc_row = None
        if "desc_row" in kwargs:
            self.__desc_row = kwargs["desc_row"] - 1
        self.__body_row = kwargs["body_row"] - 1
        self.__global_rules = {}
        self.__table = [
            [],  # field_list
            [],  # data_type_list
            [],  # rule_list
            [],  # desc_list
            []  # data_list
        ]
        self.__is_load = False

    def _load_table(self, rows):
        field_list = rows[self.__field_row]
        data_type_list = rows[self.__type_row]
        rule_list = rows[self.__rule_row] if self.__rule_row is not None else []
        desc_list = rows[self.__desc_row] if self.__desc_row is not None else []
        data_list = rows[self.__body_row:]
        self.__table[4].extend([[] for _ in range(len(data_list))])
        zip_iter = zip_longest(field_list, data_type_list, rule_list, desc_list)
        for index, (field_name, data_type, rules, desc) in enumerate(zip_iter):
            field_name = util.trim(field_name)
            if field_name:
                try:
                    self.__table[FIELD_NAME_INDEX].append(field_name)
                    self.__table[DATA_TYPE_INDEX].append(convert_data_type(data_type))
                    self.__table[RULE_INDEX].append(convert_rules(self, index, rules))
                    self.__table[DESC_INDEX].append(convert_desc(desc))
                    for col_num, rows in enumerate(data_list):
                        data = convert_data(self.column_data_type(index), rows[index])
                        self.__table[DATA_INDEX][col_num].append(data)
                except (TypeError,) as e:
                    err = "%(row_num)s:%(column_num)s %(err)s" % {
                        "row_num": self.__type_row + 1, "column_num": index + 1,
                        "err": e.err
                    }
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
    def real_field_name_row_num(self):
        return self.__field_row + 1

    @property
    def real_data_type_row_num(self):
        return self.__type_row + 1

    @property
    def real_body_row_num(self):
        return self.__body_row + 1

    @property
    def real_rule_row_num(self):
        return self.__rule_row + 1

    @property
    def real_description_row_num(self):
        return self.__desc_row + 1

    def column_field_name(self, column_num):
        return self.__table[FIELD_NAME_INDEX][column_num]

    def column_data_type(self, column_num):
        return self.__table[DATA_TYPE_INDEX][column_num]

    def column_rules(self, column_num):
        return self.__table[RULE_INDEX][column_num]

    def column_description(self, column_num):
        return self.__table[DESC_INDEX][column_num]

    def column_data_list(self, column_num):
        for row in self.__table[DATA_INDEX]:
            yield row[column_num]

    @property
    def global_rules(self):
        return self.__global_rules

    @property
    def is_load(self):
        return self.__is_load

    def verify(self):
        try:
            for col_num, rules in enumerate(self.__table[RULE_INDEX]):
                for rule in rules:
                    rule.verify(self.column_data_list(col_num))
            for global_rule in self.__global_rules.values():
                global_rule.verify(self)
        except (ColumnException, RuleException) as e:
            err = "table:`%(table_name)s` %(error)s" % {"table_name": self.table_name, "error": e.err}
            raise TableException(err)

    def export(self):
        from cfg_exporter.tables.exporter.erl_export import ErlExport
        obj = ErlExport()
        obj.export(self)
        pass


class TableException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


def convert_data_type(data_type):
    data_type = util.trim(data_type)
    if data_type == "":
        raise "data type is undefined"

    if data_type not in DataType.__members__:
        raise "data type `%(data_type)s` is unsupported\n" \
              "supported data types [%(support_data_type)s]" % {
                  "data_type": data_type,
                  "support_data_type": ",".join(DataType.__members__.keys())
              }

    return DataType[data_type]


def convert_rules(table_obj, column_num, rules):
    rules = util.trim(rules)
    if rules != "":
        return tuple(parse_rules(table_obj, column_num, rules))
    return []


def convert_desc(desc):
    return desc if util.trim(desc) else None


def convert_data(data_type, row):
    try:
        if row:
            if data_type.value is Iterable:
                data = eval(row)
                assert isinstance(data, data_type.value)
                return data
            else:
                return data_type.value(row)
        else:
            return None
    except (SyntaxError, NameError, AssertionError, ValueError):
        raise "incorrect data or data type"

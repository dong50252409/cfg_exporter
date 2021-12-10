import itertools
import os
from abc import abstractmethod
from typing import Iterable

import cfg_exporter.util as util
import cfg_exporter.tables.base.rule as rule
from cfg_exporter.const import DataType
from cfg_exporter.tables.base.rule import KeyRule, MacroRule, RuleException, MacroType

FIELD_NAME_INDEX, DATA_TYPE_INDEX, RULE_INDEX, DESC_INDEX, DATA_INDEX = range(5)


class Table(object):
    def __init__(self, container_obj, filename, args):
        self.__container_obj = container_obj
        self.__full_filename = os.path.abspath(filename)
        self.args = args
        self.__parse_args()
        self.__table = [[], [], [], [], []]
        self.__key_columns = []
        self.__global_rules = {}
        self.__is_load = False

    def __parse_args(self):
        self.__field_row = self.args.field_row - 1
        self.__type_row = self.args.type_row - 1
        self.__rule_row = self.args.rule_row - 1 if 'rule_row' in self.args else None
        self.__desc_row = self.args.desc_row - 1 if 'desc_row' in self.args else None
        self.__data_row = self.args.data_row - 1
        try:
            assert self.__data_row == max(
                self.__data_row,
                self.__field_row,
                self.__type_row,
                self.__rule_row if self.__rule_row else 0,
                self.__desc_row if self.__desc_row else 0
            )
        except AssertionError:
            raise TableException('the data row line is not at the bottom')

    @abstractmethod
    def load_table(self):
        ...

    def _load_table(self, rows):
        field_list = rows[self.__field_row]
        data_type_list = rows[self.__type_row]
        rule_list = rows[self.__rule_row] if self.__rule_row is not None else []
        desc_list = rows[self.__desc_row] if self.__desc_row is not None else []
        data_list = rows[self.__data_row:]

        self.__row_count = len(data_list)
        self.__column_count = len(self.__table[FIELD_NAME_INDEX])
        self.__table[DATA_INDEX].extend([[] for _ in range(self.__row_count)])

        zip_iter = itertools.zip_longest(field_list, data_type_list, rule_list, desc_list)
        for index, (field_name, data_type, rules, desc) in enumerate(zip_iter):
            field_name = util.trim(field_name)
            if field_name:
                try:
                    self.__table[FIELD_NAME_INDEX].append(field_name)
                    self.__table[DATA_TYPE_INDEX].append(convert_data_type(data_type))
                    self.__table[RULE_INDEX].append(convert_rules(self, index, rules))
                    self.__table[DESC_INDEX].append(convert_desc(desc))
                    for col_num, rows in enumerate(data_list):
                        data = convert_data(self.data_type_by_column_num(index), rows[index])
                        self.__table[DATA_INDEX][col_num].append(data)
                except (RuleException, DataException) as e:
                    raise TableException(f'{self.__type_row + 1}:{index + 1} {e.err}')

        if KeyRule.__name__ in self.__global_rules:
            self.__key_columns = [col_num for _, col_num in
                                  sorted(self.__global_rules[KeyRule.__name__].values.items())]
        self.__is_load = True

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
        return self.__field_row + 1

    @property
    def data_type_row_num(self):
        return self.__type_row + 1

    @property
    def data_row_num(self):
        return self.__data_row + 1

    @property
    def rule_row_num(self):
        return self.__rule_row + 1

    @property
    def description_row_num(self):
        return self.__desc_row + 1

    @property
    def row_count(self):
        return self.__row_count

    @property
    def column_count(self):
        return self.__column_count

    @property
    def field_names(self):
        return self.__table[FIELD_NAME_INDEX]

    def field_name_by_column_num(self, column_num):
        return self.field_names[column_num]

    @property
    def data_types(self):
        return self.__table[DATA_TYPE_INDEX]

    def data_type_by_column_num(self, column_num):
        return self.data_types[column_num]

    @property
    def rules(self):
        return self.__table[RULE_INDEX]

    def rule_by_column_num(self, column_num):
        return self.rules[column_num]

    @property
    def global_rules(self):
        return self.__global_rules

    @property
    def descriptions(self):
        return self.__table[DESC_INDEX]

    def description_by_column_num(self, column_num):
        return self.descriptions[column_num]

    @property
    def data_iter(self):
        for row in self.__table[DATA_INDEX]:
            yield row

    def data_iter_by_column_num(self, column_num):
        for row in self.data_iter:
            yield row[column_num]

    def data_iter_by_field_name(self, field_name):
        if field_name in self.field_names:
            column_num = self.field_names.index(field_name)
            return self.__data_iter_by_field_name(column_num)

    def __data_iter_by_field_name(self, column_num):
        for row in self.data_iter:
            yield row[column_num]

    @property
    def key_columns(self):
        return self.__key_columns

    @property
    def key_data_iter(self):
        for row in self.data_iter:
            yield [row[col_num] for col_num in self.key_columns]

    @property
    def macro_data_iter(self):
        if MacroRule.__name__ in self.global_rules:
            macro_dict = self.global_rules[MacroRule.__name__].values
            if MacroType.name in macro_dict and MacroType.desc in macro_dict:
                for row in self.data_iter:
                    macro_name = row[macro_dict[MacroType.name]]
                    if macro_name is not None:
                        yield macro_name, row[macro_dict[MacroType.value]], row[macro_dict[MacroType.desc]]
            elif MacroType.name in macro_dict:
                for row in self.data_iter:
                    macro_name = row[macro_dict[MacroType.name]]
                    if macro_name is not None:
                        yield macro_name, row[macro_dict[MacroType.value]], None

    @property
    def is_load(self):
        return self.__is_load

    def verify(self):
        try:
            for col_num, rules in enumerate(self.rules):
                for rule_obj in rules:
                    rule_obj.verify(self.data_iter_by_column_num(col_num))
            for global_rule_obj in self.global_rules.values():
                global_rule_obj.verify(self)
        except RuleException as e:
            raise TableException(f'table:`{self.table_name}` {e.err}')


class TableException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


def convert_data_type(data_type):
    data_type = util.trim(data_type)
    if data_type == '':
        raise DataException('the data type is undefined')

    if data_type not in DataType.__members__:
        raise DataException(
            f'data type `{data_type}` is unsupported\nsupported data types [{", ".join(DataType.__members__.keys())}]')

    return DataType[data_type]


def convert_rules(table_obj, column_num, rules):
    rules = util.trim(rules)
    if rules != '':
        return tuple(rule.parse_rules(table_obj, column_num, rules))
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
        raise DataException('incorrect data or data type')


class DataException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err

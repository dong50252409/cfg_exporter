import itertools
import logging
import os
from abc import abstractmethod

from cfg_exporter import *
import cfg_exporter.util as util
import cfg_exporter.tables.base.rule as rule
from cfg_exporter.const import DataType
from cfg_exporter.language import LANG
from cfg_exporter.tables.base.raw import RawType
from cfg_exporter.tables.base.rule import KeyRule, MacroRule, RuleException, RuleType, MacroType

FIELD_NAME_INDEX, DATA_TYPE_INDEX, RULE_INDEX, DESC_INDEX, DATA_INDEX = range(5)


class Table(object):
    def __init__(self, container_obj, filename, args):
        self._container_obj = container_obj
        self._full_filename = filename
        self.args = args
        self.__parse_args()
        self._table = [[], [], [], [], []]
        self._key_columns = []
        self._global_rules = {}
        self._is_load = False

    def __parse_args(self):
        self._field_row = self.args.field_row - 1
        self._type_row = self.args.type_row - 1
        self._rule_row = self.args.rule_row - 1 if self.args.rule_row else None
        self._desc_row = self.args.desc_row - 1 if self.args.desc_row else None
        self._data_row = self.args.data_row - 1
        try:
            assert self._data_row == max(
                self._data_row,
                self._field_row,
                self._type_row,
                self._rule_row if self._rule_row else 0,
                self._desc_row if self._desc_row else 0
            )
        except AssertionError:
            raise TableException('the data row line is not at the bottom')

    @abstractmethod
    def load_table(self):
        ...

    def _load_table(self, rows):
        logging.debug(LANG.LOAD_TABLE.format(table=self.filename))
        loadable_column_list = self.__load_field_name(rows)

        self.__load_other(rows, loadable_column_list)

        if KeyRule.__name__ in self._global_rules:
            self._key_columns = [col_num for col_num in sorted(self._global_rules[KeyRule.__name__].values.values())]

        self._is_load = True
        logging.debug(LANG.TABLE_LOADED.format(table=self.filename))

    def __load_field_name(self, rows):
        column_list = []
        field_list = rows[self._field_row]
        for index, field_name in enumerate(field_list):
            try:
                field_name = convert_field_name(field_name)
                if field_name:
                    self._table[FIELD_NAME_INDEX].append(field_name)
                    column_list.append(True)
                else:
                    column_list.append(False)

            except DataException as e:
                err_list = [LANG.ROW_COL_NUM, LANG.TABLE, LANG.FIELD, e.err]
                err = ' '.join(err_list).format(
                    row_num=self.data_type_row_num, col_num=index + 1,
                    table=self.filename, field=field_name)
                raise TableException(err)
        return column_list

    def __load_other(self, rows, loadable_column_list):
        data_type_list = rows[self._type_row]
        rule_list = rows[self._rule_row] if self._rule_row is not None else []
        desc_list = rows[self._desc_row] if self._desc_row is not None else []
        data_list = rows[self._data_row:]

        self._row_count = len(data_list)
        self._column_count = len(self._table[FIELD_NAME_INDEX])
        self._table[DATA_INDEX].extend([[] for _ in range(self._row_count)])

        col_num = 0
        zip_iter = itertools.zip_longest(loadable_column_list, data_type_list, rule_list, desc_list)
        for index, (loadable_column, data_type, rules, desc) in enumerate(zip_iter):
            try:
                if loadable_column:
                    real_data_type = convert_data_type(data_type)
                    self._table[DATA_TYPE_INDEX].append(real_data_type)
                    self._table[RULE_INDEX].append(
                        [] if real_data_type is RawType else convert_rules(self, index, rules))
                    self._table[DESC_INDEX].append(convert_desc(desc))
                    for row_num, rows in enumerate(data_list):
                        real_data = convert_data(real_data_type, rows[index])
                        self._table[DATA_INDEX][row_num].append(real_data)
                    col_num += 1

            except RuleException as e:
                err_list = [LANG.ROW_COL_NUM, LANG.TABLE, LANG.FIELD, LANG.TYPE, LANG.RULE, e.err]
                err = ' '.join(err_list).format(
                    row_num=self.rule_row_num, col_num=index + 1,
                    table=self.filename, field=self.field_name_by_column_num(col_num),
                    type=self.data_type_by_column_num(col_num).name, rule=e.rule_str)
                raise TableException(err)

            except DataException as e:
                err_list = [LANG.ROW_COL_NUM, LANG.TABLE, LANG.FIELD, e.err]
                err = ' '.join(err_list).format(
                    row_num=self.data_type_row_num, col_num=index + 1,
                    table=self.filename, field=self.field_name_by_column_num(col_num))
                raise TableException(err)

    @property
    def is_load(self):
        return self._is_load

    def has_table_and_field(self, table_name, field_name):
        if table_name == self.table_name:
            return True, field_name in self.field_names
        return self._container_obj.has_table_and_field(table_name, field_name)

    def get_table_obj(self, full_filename):
        return self._container_obj.get_table_obj(full_filename)

    @property
    def full_filename(self) -> str:
        """
        返回配置表的完整路径以及全名
        """
        return self._full_filename

    @property
    def filename(self) -> str:
        """
        返回配置表的全名
        """
        return os.path.basename(self.full_filename)

    @property
    def table_name(self) -> str:
        """
        返回配置表的表名
        """
        return os.path.splitext(self.filename)[0]

    @property
    def field_name_row_num(self) -> int:
        """
        返回配置表的列字段名行号
        """
        return self._field_row + 1

    @property
    def data_type_row_num(self) -> int:
        """
        返回配置表的列数据类型行号
        """
        return self._type_row + 1

    @property
    def data_row_num(self) -> int:
        """
        返回配置表的数据行起始行号
        """
        return self._data_row + 1

    @property
    def rule_row_num(self) -> int:
        """
        返回配置表的列规则行号
        """
        return self._rule_row + 1

    @property
    def description_row_num(self) -> int:
        """
        返回配置表的列描述行号
        """
        return self._desc_row + 1

    @property
    def row_count(self) -> int:
        """
        返回配置表的总数据数
        """
        return self._row_count

    @property
    def column_count(self) -> int:
        """
        返回配置表的总列数
        """
        return self._column_count

    @property
    def field_names(self) -> list[str]:
        """
        返回配置表的字段名列表
        """
        return self._table[FIELD_NAME_INDEX]

    def field_name_by_column_num(self, column_num: int) -> str:
        """
        根据列号，从0开始，返回配置表的字段名
        """
        return self.field_names[column_num]

    @property
    def data_types(self) -> list[Any]:
        """
        返回配置表的数据类型列表
        """
        return self._table[DATA_TYPE_INDEX]

    def data_type_by_column_num(self, column_num: int) -> Any:
        """
        根据列号，从0开始，返回配置表的数据类型
        """
        return self.data_types[column_num]

    @property
    def rules(self) -> list[list[rule.BaseRule]]:
        """
        返回配置表的规则列表
        """
        return self._table[RULE_INDEX]

    def rule_by_column_num(self, column_num: int) -> list[rule.BaseRule]:
        """
        根据列号，从0开始，返回配置表的规则
        """
        return self.rules[column_num]

    @property
    def global_rules(self) -> dict[str, rule.GlobalRule]:
        """
        返回配置表的全局规则列表
        """
        return self._global_rules

    @property
    def descriptions(self) -> list[str]:
        """
        返回配置表的描述列表
        """
        return self._table[DESC_INDEX]

    def description_by_column_num(self, column_num: int) -> str:
        """
        返回配置表的描述，根据列号，从0开始
        """
        return self.descriptions[column_num]

    @property
    def row_iter(self) -> Iterator[list[AnyType]]:
        """
        迭代返回配置表的每行数据
        """
        for row in self._table[DATA_INDEX]:
            yield row

    def data_iter_by_column_num(self, column_num: int) -> Iterator[AnyType]:
        """
        根据列号，从0开始，迭代返回配置表的每列数据
        """
        for row in self.row_iter:
            yield row[column_num]

    def data_iter_by_field_name(self, field_name: str) -> Iterator[str]:
        """
        根据字段名，迭代返回配置表的每列数据
        """
        if field_name in self.field_names:
            column_num = self.field_names.index(field_name)
            for row in self.row_iter:
                yield row[column_num]

    @property
    def key_columns(self) -> list[int]:
        """
        返回主键列列号，列号从0开始
        """
        return self._key_columns

    @property
    def key_data_iter(self) -> Iter:
        """
        迭代返回主键列数据，多值以元祖形式返回
        """
        func = multi_value_func(self.key_columns) if len(self.key_columns) > 1 else sgl_value_func(self.key_columns[0])
        for row in self.row_iter:
            yield func(row)

    @property
    def macro_data_iter(self) -> Iterator[tuple[str, AnyType, str]]:
        """
        迭代返回宏定义名、宏定义值、宏定义描述的元祖
        """
        if MacroRule.__name__ in self.global_rules:
            macro_dict = self.global_rules[MacroRule.__name__].values
            if MacroType.name in macro_dict and MacroType.desc in macro_dict:
                for row in self.row_iter:
                    macro_name = row[macro_dict[MacroType.name]]
                    if macro_name is not None:
                        yield macro_name, row[macro_dict[MacroType.value]], row[macro_dict[MacroType.desc]]
            elif MacroType.name in macro_dict:
                for row in self.row_iter:
                    macro_name = row[macro_dict[MacroType.name]]
                    if macro_name is not None:
                        yield macro_name, row[macro_dict[MacroType.value]], None

    def index_list(self, index_field_names: list[str], value_field_names: list[str]) -> Iter:
        """
        根据下标字段列表和值字段列表迭代返回对应数据，多值以元祖形式返回
        例如：有多个同一种类型的道具，可返回当前类型的所有道具id
        """
        if len(index_field_names) > 1:
            index_func = multi_field_func([self.field_names.index(field_name) for field_name in index_field_names])
        else:
            index_func = sgl_field_func(self.field_names.index(index_field_names[0]))

        if len(value_field_names) > 1:
            value_func = multi_value_func([self.field_names.index(field_name) for field_name in value_field_names])
        else:
            value_func = sgl_value_func(self.field_names.index(value_field_names[0]))

        d = {}
        for row in self.row_iter:
            fields = index_func(row)
            str_fields = str(fields)
            values = value_func(row)
            if str_fields in d:
                _, values_list = d[str_fields]
                values_list.append(values)
            else:
                d[str_fields] = (fields, [values])
        for values in d.values():
            yield values

    def verify(self) -> None:
        """
        执行配置表的规则验证
        """
        for col_num, rules in enumerate(self.rules):
            try:
                for rule_obj in rules:
                    rule_obj.verify(self.data_iter_by_column_num(col_num))
            except RuleException as e:
                err_list = [LANG.ROW_COL_NUM, LANG.TABLE, LANG.FIELD, LANG.TYPE, LANG.RULE, e.err]
                err = ' '.join(err_list).format(
                    row_num=self.data_row_num + e.row_num, col_num=col_num + 1,
                    table=self.filename, field=self.field_name_by_column_num(col_num),
                    type=self.data_type_by_column_num(col_num).name, rule=e.rule_str
                )
                raise TableException(err)

        for global_rule_obj in self.global_rules.values():
            try:
                global_rule_obj.verify(self)
            except RuleException as e:
                err_list = []
                if e.row_num is not None and e.col_num is not None:
                    err_list.append(LANG.ROW_COL_NUM.format(row_num=self.data_row_num + e.row_num, col_num=e.col_num))

                err_list.append(LANG.TABLE.format(table=self.filename))

                if e.rule_str:
                    err_list.append(LANG.RULE.format(rule=e.rule_str))

                err_list.append(e.err)
                raise TableException(' '.join(err_list))


class TableException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


class DataException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


def multi_value_func(key_columns):
    return lambda row: tuple([row[col_num] for col_num in key_columns])


def sgl_value_func(col_num):
    return lambda row: row[col_num]


def multi_field_func(col_num_list):
    return lambda row: tuple([row[col_num] for col_num in col_num_list])


def sgl_field_func(col_num):
    return lambda row: [row[col_num]]


def convert_field_name(field_name: str) -> StrOrNone:
    field_name = util.trim(field_name)
    if field_name:
        if not util.check_naming(field_name):
            raise DataException(LANG.INVALID_FIELD_NAME)
        return field_name


def convert_data_type(data_type):
    data_type = util.trim(data_type)
    if data_type == '':
        raise DataException(LANG.UNDEFINED_DATA_TYPE)

    if data_type not in DataType.__members__:
        raise DataException(
            LANG.UNSUPPORTED_DATA_TYPE.format(type=data_type, supported={", ".join(DataType.__members__.keys())}))
    return DataType[data_type]


def convert_rules(table_obj, column_num, rules):
    rules = util.trim(rules)
    if rules != '':
        return tuple(parse_rules(table_obj, column_num, rules))
    return []


def parse_rules(table_obj, column_num, rules):
    rule_list = []
    for each_rule in iter_rule(rules):
        try:
            rule_obj = rule.create_rule_obj(table_obj, column_num, each_rule)
            rule_list.append(rule_obj)
        except (AssertionError, ValueError, KeyError):
            raise DataException(LANG.PARSE_RULE_EXCEPTION.format(rule=each_rule))
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


def convert_desc(desc):
    return util.trim_desc(desc)


def convert_data(data_type, row):
    try:
        if row != '':
            if data_type.value is Iterable:
                data = eval(row)
                assert isinstance(data, data_type.value)
                return data
            elif data_type.value is RawType:
                return RawType(row)
            else:
                return data_type.value(row)
        else:
            return None
    except (SyntaxError, NameError, AssertionError, ValueError, AttributeError):
        raise DataException(LANG.CONVERT_DATA_EXCEPTION.format(type=data_type.name, data=row))


__all__ = ('Table', 'TableException')

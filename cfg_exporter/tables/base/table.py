import itertools
import os
import typing
from abc import ABC, abstractmethod

import cfg_exporter.tables.base.rule as rule
import cfg_exporter.util as util
from cfg_exporter import AnyType, Iter
from cfg_exporter.const import DataType, DATA_TYPE_DETAIL_SPLIT
from cfg_exporter.tables.base.rule import KeyRule, ConstRule, RuleException, RuleType, ConstType
from cfg_exporter.tables.base.type import RawType, DefaultValue

INDEX_RANGE = 6

FIELD_NAME_INDEX, DATA_TYPE_INDEX, DATA_TYPE_DETAIL_INDEX, RULE_INDEX, DESC_INDEX, DATA_INDEX = range(INDEX_RANGE)


class Table(ABC):

    def __init__(self, container_obj, filename, args):
        self._container_obj = container_obj
        self._full_filename = filename
        self.args = args
        self.__parse_args()
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
        self._table = [[] for _ in range(INDEX_RANGE)]

        loadable_column_list = self.__load_field_name(rows)

        self.__load_other(rows, loadable_column_list)

        if KeyRule.__name__ in self._global_rules:
            self._key_columns = [col_num for col_num in sorted(self._global_rules[KeyRule.__name__].values.values())]
        self._is_load = True

    def __load_field_name(self, rows):
        column_list = []
        field_list = rows[self._field_row]
        for index, field_name in enumerate(field_list):
            try:
                naming_convention = self.args.export_type.value.naming_convention()
                field_name = convert_field_name(field_name, naming_convention)
                if field_name:
                    self._table[FIELD_NAME_INDEX].append(field_name)
                column_list.append(field_name)

            except FieldNameException as e:
                err_list = [_('r{row_num}:c{col_num}'), _('table:`{table}`'), _('field:`{field}`'), e.err]
                err = ' '.join(err_list) \
                    .format(row_num=self.field_name_row_num, col_num=index + 1, table=self.filename, field=field_name)
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

        real_col_num = 0
        zip_iter = itertools.zip_longest(loadable_column_list, data_type_list, rule_list, desc_list)
        for index, (field_name, data_type, rules, desc) in enumerate(zip_iter):
            try:
                if field_name:
                    real_data_type, data_type_detail = convert_data_type(data_type, self.args.export_type.value)
                    self._table[DATA_TYPE_INDEX].append(real_data_type)
                    self._table[DATA_TYPE_DETAIL_INDEX].append(data_type_detail)
                    self._table[RULE_INDEX].append(
                        [] if real_data_type is RawType else convert_rules(self, real_col_num, rules))
                    self._table[DESC_INDEX].append(convert_desc(desc))
                    for row_num, rows in enumerate(data_list):
                        try:
                            real_data = convert_data(real_data_type, rows[index])
                            self._table[DATA_INDEX][row_num].append(real_data)
                        except DataException as e:
                            err_list = [_('r{row_num}:c{col_num}'), _('table:`{table}`'), _('field:`{field}`'), e.err]
                            err = ' '.join(err_list) \
                                .format(row_num=self.data_row_num + row_num, col_num=index + 1, table=self.filename,
                                        field=field_name)
                            raise TableException(err)
                    real_col_num += 1

            except DataTypeException as e:
                err_list = [_('r{row_num}:c{col_num}'), _('table:`{table}`'), _('field:`{field}`'), e.err]
                err = ' '.join(err_list) \
                    .format(row_num=self.data_type_row_num, col_num=index + 1, table=self.filename, field=field_name)
                raise TableException(err)

            except RuleException as e:
                err_list = [_('r{row_num}:c{col_num}'), _('table:`{table}`'), _('field:`{field}`'), _('type:`{type}`'),
                            _('rule:`{rule}`'), e.err]
                err = ' '.join(err_list) \
                    .format(row_num=self.rule_row_num, col_num=index + 1, table=self.filename, field=field_name,
                            type=real_data_type.name, rule=e.rule_str)
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
        ??????????????????????????????????????????
        """
        return self._full_filename

    @property
    def filename(self) -> str:
        """
        ????????????????????????
        """
        return os.path.basename(self.full_filename)

    @property
    def table_name(self) -> str:
        """
        ????????????????????????
        """
        return os.path.splitext(self.filename)[0]

    @property
    def field_name_row_num(self) -> int:
        """
        ????????????????????????????????????
        """
        return self._field_row + 1

    @property
    def data_type_row_num(self) -> int:
        """
        ???????????????????????????????????????
        """
        return self._type_row + 1

    @property
    def data_row_num(self) -> int:
        """
        ???????????????????????????????????????
        """
        return self._data_row + 1

    @property
    def rule_row_num(self) -> int:
        """
        ?????????????????????????????????
        """
        return self._rule_row + 1

    @property
    def description_row_num(self) -> int:
        """
        ?????????????????????????????????
        """
        return self._desc_row + 1

    @property
    def row_count(self) -> int:
        """
        ??????????????????????????????
        """
        return self._row_count

    @property
    def column_count(self) -> int:
        """
        ???????????????????????????
        """
        return self._column_count

    def column_num_by_field_name(self, field_name):
        """
        ??????????????????????????????????????????0??????
        """
        return self.field_names.index(field_name)

    @property
    def field_names(self) -> typing.List[str]:
        """
        ?????????????????????????????????
        """
        return self._table[FIELD_NAME_INDEX]

    def field_name_by_column_num(self, column_num: int) -> str:
        """
        ??????????????????????????????????????????????????????0??????
        """
        return self.field_names[column_num]

    @property
    def data_types(self) -> typing.List[typing.Any]:
        """
        ????????????????????????????????????
        """
        return self._table[DATA_TYPE_INDEX]

    def data_type_by_column_num(self, column_num: int) -> DataType:
        """
        ?????????????????????????????????????????????????????????0??????
        """
        return self.data_types[column_num]

    @property
    def data_type_details(self) -> typing.List[str]:
        """
        ??????????????????????????????
        """
        return self._table[DATA_TYPE_DETAIL_INDEX]

    def data_type_detail_by_column_num(self, column_num: int) -> str:
        return self.data_type_details[column_num]

    @property
    def rules(self) -> typing.List[typing.List[rule.BaseRule]]:
        """
        ??????????????????????????????
        """
        return self._table[RULE_INDEX]

    def rule_by_column_num(self, column_num: int) -> typing.List[rule.BaseRule]:
        """
        ???????????????????????????????????????????????????0??????
        """
        return self.rules[column_num]

    @property
    def global_rules(self) -> typing.Dict[str, rule.GlobalRule]:
        """
        ????????????????????????????????????
        """
        return self._global_rules

    @property
    def descriptions(self) -> typing.List[str]:
        """
        ??????????????????????????????
        """
        return self._table[DESC_INDEX]

    def description_by_column_num(self, column_num: int) -> str:
        """
        ???????????????????????????????????????????????????0??????
        """
        return self.descriptions[column_num]

    def value(self, row, column, value):
        """
        ???????????????????????????
        """
        self._table[DATA_INDEX][row][column] = value

    @property
    def row_iter(self) -> typing.Iterator[typing.List[AnyType]]:
        """
        ????????????????????????????????????
        """
        for row in self._table[DATA_INDEX]:
            yield row

    def data_iter_by_column_nums(self, *column_nums) -> typing.Iterator[AnyType]:
        """
        ???????????????????????????????????????????????????????????????0??????
        """
        func = multi_value_func(column_nums) if len(column_nums) > 1 else sgl_value_func(column_nums[0])
        for row in self.row_iter:
            yield func(row)

    def data_iter_by_field_names(self, *field_names) -> typing.Iterator[str]:
        """
        ??????????????????????????????????????????????????????
        """
        column_nums = [self.column_num_by_field_name(field_name) for field_name in field_names]
        func = multi_value_func(column_nums) if len(column_nums) > 1 else sgl_value_func(column_nums[0])
        for row in self.row_iter:
            yield func(row)

    @property
    def key_columns(self) -> typing.List[int]:
        """
        ?????????????????????????????????0??????
        """
        return self._key_columns

    @property
    def key_field_name_iter(self) -> typing.List[str]:
        """
        ????????????????????????
        """
        for index in self.key_columns:
            yield self.field_names[index]

    @property
    def key_data_iter(self) -> Iter:
        """
        ?????????????????????????????????????????????????????????
        """
        key_count = len(self.key_columns)
        if key_count != 0:
            func = multi_value_func(self.key_columns) if len(self.key_columns) > 1 else sgl_value_func(
                self.key_columns[0])
            for row in self.row_iter:
                yield func(row)

    @property
    def has_const(self):
        """
        ??????????????????????????????
        """
        return ConstRule.__name__ in self.global_rules

    @property
    def const_data_iter(self) -> typing.Iterator[typing.Tuple[str, AnyType, str, str]]:
        """
        ?????????????????????????????????????????????????????????
        """
        if ConstRule.__name__ in self.global_rules:
            for const_name, (const_value, const_data_type_detail), const_desc in \
                    zip(self.const_name_iter(), self.const_value_iter(), self.const_desc_iter()):
                if const_name and not isinstance(const_name, DefaultValue) \
                        and const_value is not None and not isinstance(const_value, DefaultValue):
                    yield const_name, const_value, const_data_type_detail, const_desc

    def const_name_iter(self):
        if ConstRule.__name__ in self.global_rules:
            col_num = self.global_rules[ConstRule.__name__].values[ConstType.name]
            for row in self.row_iter:
                yield row[col_num]

    def const_value_iter(self):
        if ConstRule.__name__ in self.global_rules:
            if ConstType.value in self.global_rules[ConstRule.__name__].values:
                col_num = self.global_rules[ConstRule.__name__].values[ConstType.value]
                data_type_detail = self.data_type_detail_by_column_num(col_num)
                for row in self.row_iter:
                    yield row[col_num], data_type_detail
            else:
                for index, _ in enumerate(self.row_iter, start=1):
                    yield index, "int"

    def const_desc_iter(self):
        if ConstRule.__name__ in self.global_rules:
            if ConstType.desc in self.global_rules[ConstRule.__name__].values:
                col_num = self.global_rules[ConstRule.__name__].values[ConstType.desc]
                for row in self.row_iter:
                    const_desc = row[col_num]
                    if isinstance(const_desc, DefaultValue):
                        const_desc = const_desc.text
                    yield const_desc
            else:
                for _ in self.row_iter:
                    yield None

    def index_list(self, index_field_names: typing.List[str], value_field_names: typing.List[str]) -> Iter:
        """
        ????????????????????????????????????????????????????????????????????????????????????????????????
        ?????????????????????????????????????????????????????????????????????????????????id
        """
        if len(index_field_names) > 1:
            index_func = multi_value_func([self.field_names.index(field_name) for field_name in index_field_names])
        else:
            f = sgl_value_func(self.field_names.index(index_field_names[0]))
            index_func = lambda _: (f(row),)

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
        ??????????????????????????????
        """
        for col_num, rules in enumerate(self.rules):
            try:
                for rule_obj in rules:
                    rule_obj.verify(self.data_iter_by_column_nums(col_num))
            except RuleException as e:
                err_list = [_('r{row_num}:c{col_num}'), _('table:`{table}`'), _('field:`{field}`'), _('type:`{type}`'),
                            _('rule:`{rule}`'), e.err]
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
                    err_list.append(_('r{row_num}:c{col_num}')
                                    .format(row_num=self.data_row_num + e.row_num, col_num=e.col_num))

                err_list.append(_('table:`{table}`').format(table=self.filename))

                if e.rule_str:
                    err_list.append(_('rule:`{rule}`').format(rule=e.rule_str))

                err_list.append(e.err)
                raise TableException(' '.join(err_list))


def multi_value_func(key_columns):
    return lambda row: tuple(row[col_num] for col_num in key_columns)


def sgl_value_func(col_num):
    return lambda row: row[col_num]


def convert_field_name(field_name, naming_convention):
    field_name = util.trim(field_name)
    if field_name:
        if not util.check_naming(field_name):
            raise FieldNameException(_('invalid field name'))
        return naming_convention(field_name)


def convert_data_type(data_type, export_type):
    data_type = util.trim(data_type)
    if data_type == '' or data_type is None:
        raise DataTypeException(_('the data type is undefined'))
    split = data_type.split(DATA_TYPE_DETAIL_SPLIT)
    new_data_type = split[0]
    data_type_detail = export_type.data_type_detail(split[-1])
    if new_data_type not in DataType.__members__:
        raise DataTypeException(_('data type `{type}` is unsupported\nsupported data types [{supported}]')
                                .format(type=data_type, supported=", ".join(DataType.__members__.keys())))
    return DataType[new_data_type], data_type_detail


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
            raise RuleException(_('is invalid rule'), each_rule)
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
        return data_type(row)
    except (SyntaxError, NameError, AssertionError, ValueError, AttributeError):
        raise DataException(_('type:`{type}` `{data}` is invalid data').format(type=data_type.name, data=row))


class TableException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


class FieldNameException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err


class DataTypeException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err


class DataException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err


__all__ = ('Table', 'TableException')

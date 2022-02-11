import os
import re
from collections import Counter
from typing import Iterable

from cfg_exporter.const import DataType
from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.export import BaseExport
from cfg_exporter.lang_template import lang
from cfg_exporter.tables.base.type import LangType, IgnoreValue, ReferenceValue

EXTENSION = 'lua'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', EXTENSION)
BASE_TEMPLATE = f'{EXTENSION}_base.{TEMPLATE_EXTENSION}'

tab = str.maketrans('()[]', '{}{}')
sub_str = '__lua_rt__'
pattern = re.compile(fr'{sub_str}\d+')
re_sub_dict = {}


def rt_replace(match):
    return re_sub_dict[match.group(0)]


def format_value(value):
    if value is None:
        return 'nil'
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, Iterable):
        return pattern.sub(rt_replace, f'{value}'.translate(tab))
    elif isinstance(value, LangType):
        return f'"{lang(value.text)}"'
    elif isinstance(value, IgnoreValue):
        return format_value(value.text)
    elif isinstance(value, ReferenceValue):
        return format_value(value.raw_value)
    else:
        return f'{value}'


class LuaExport(BaseExport):

    def __init__(self, args):
        global_vars = {'format_value': format_value}
        super().__init__(args, BASE_TEMPLATE_PATH, [EXTENSION], global_vars)

    def export(self, table_obj):

        if self.args.lua_optimize:
            default_values = _analyze_default_value(table_obj)
            replace_table = _analyze_replace_table(table_obj)
        else:
            default_values = None
            replace_table = None

        ctx = {
            'table_obj': table_obj, 'prefix': self.args.file_prefix,
            'default_values': default_values, 'replace_table': replace_table
        }
        table_name = table_obj.table_name
        filename = f'{table_name}.{EXTENSION}'

        if table_name in self.extend_templates.get(EXTENSION, []):
            self.render(filename, f'{table_name}.{EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(filename, BASE_TEMPLATE, ctx)

    def file_desc(self) -> str:
        return "-------------------------------------\n" \
               "--  AUTO GENERATE BY CFG_EXPORTER  --\n" \
               "-------------------------------------\n"


def _analyze_default_value(table_obj):
    default_values = []
    for field_name, data_type in zip(table_obj.field_names, table_obj.data_types):
        if field_name in table_obj.key_field_name_iter:
            continue

        if data_type in (DataType.iter, DataType.lang, DataType.raw):
            counter = Counter(f'{value}' for value in table_obj.data_iter_by_field_names(field_name))
        else:
            counter = Counter(table_obj.data_iter_by_field_names(field_name))

        default_value, count = counter.most_common(1)[0]

        if count >= 3:
            if default_value is None:
                continue

            default_value = data_type.value.convert(default_value)

            ignore_value_obj = IgnoreValue(default_value)
            default_values.append((field_name, default_value))
            col_num = table_obj.column_num_by_field_name(field_name)

            for row_num, value in enumerate(table_obj.data_iter_by_column_nums(col_num)):
                if value == default_value:
                    table_obj.value(row_num, col_num, ignore_value_obj)
    return default_values


def _analyze_replace_table(table_obj):
    replace_table = {}
    for field_name, data_type in zip(table_obj.field_names, table_obj.data_types):
        if field_name in table_obj.key_field_name_iter:
            continue

        if data_type is DataType.iter:
            col_num = table_obj.column_num_by_field_name(field_name)
            for row_num, value in enumerate(table_obj.data_iter_by_column_nums(col_num)):
                table_obj.value(row_num, col_num, _replace_table(value, replace_table))

    return [ref_value.raw_value for ref_value in replace_table.values()]


def _replace_table(value, replace_table):
    if isinstance(value, list):
        if len(value) == 0:
            return _get_ref_value((), replace_table)
        return [_replace_table(child_value, replace_table) for child_value in value]
    elif isinstance(value, tuple):
        return _get_ref_value(value, replace_table)


def _get_ref_value(value, replace_table):
    if value not in replace_table:
        index = len(replace_table) + 1
        rt_key = f'{sub_str}{index}'
        rt_value = f'rt[{index}]'
        re_sub_dict[rt_key] = rt_value
        replace_table[value] = ReferenceValue(rt_key, value)
    return replace_table[value]

import os
import typing

import cfg_exporter.custom as custom
from cfg_exporter.const import DataType
from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.export import BaseExport
from cfg_exporter.lang_template import lang
from cfg_exporter.tables.base.type import DefaultValue

EXTENSION = 'lua'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', EXTENSION)
BASE_TEMPLATE = f'{EXTENSION}_base.{TEMPLATE_EXTENSION}'

tab = str.maketrans('()[]', '{}{}')


def _by_default(value):
    """
    默认Iter类型格式化
    """
    return f'{value}'.translate(tab)


def _by_reference(replace_table):
    """
    引用Iter类型格式化
    """
    return lambda value: _get_reference(replace_table, value)


def _get_reference(replace_table, value):
    key = _by_default(value)
    _, layer_num, index_num = replace_table[key]
    return f'rt_{layer_num}[{index_num}]'


# Iter类型格式化函数
_format_iter_value = _by_default


def format_value(value):
    if value is None:
        return 'nil'
    elif isinstance(value, DataType.str):
        return f'"{value}"'
    elif isinstance(value, DataType.iter):
        return _format_iter_value(value)
    elif isinstance(value, DataType.lang):
        return f'"{lang(value.text)}"'
    elif isinstance(value, DefaultValue):
        return format_value(value.text)
    else:
        return f'{value}'


class LuaExport(BaseExport):

    def __init__(self, args):
        global_vars = {'format_value': format_value}
        super().__init__(args, BASE_TEMPLATE_PATH, [EXTENSION], global_vars)

    def export(self, table_obj) -> typing.NoReturn:
        global _format_iter_value
        if self.args.lua_optimize:
            replace_table, reference_table = _analyze_reference_table(table_obj)
            default_values = custom.analyze_default_value(table_obj).items()
            _format_iter_value = _by_reference(replace_table)
        else:
            default_values = reference_table = []
            _format_iter_value = _by_default

        ctx = {
            'table_obj': table_obj, 'prefix': self.args.file_prefix,
            'reference_table': reference_table, 'default_values': default_values
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

    @staticmethod
    def naming_convention() -> typing.Any:
        import cfg_exporter.util as util
        return util.snake_case


def _analyze_reference_table(table_obj):
    """
    统计替换引用表
    """
    replace_table = {}
    for field_name, data_type in zip(table_obj.field_names, table_obj.data_types):
        if field_name in table_obj.key_field_name_iter:
            continue

        if data_type is DataType.iter:
            for value in table_obj.data_iter_by_field_names(field_name):
                _stat_replace_table_layer(replace_table, value, 0)

    _stat_replace_table_index(replace_table)
    reference_table = _stat_reference_table(replace_table)
    return replace_table, reference_table


def _stat_replace_table_layer(reference_table, value, layer_num):
    """
    统计替换表的最高层级
    """
    if isinstance(value, DataType.iter.value.real_type):
        for child_value in value:
            if isinstance(child_value, DataType.iter.value.real_type):
                _stat_replace_table_layer(reference_table, child_value, layer_num + 1)

        key = _by_default(value)
        if key in reference_table:
            if reference_table[key][1] < layer_num:
                reference_table[key] = (value, layer_num)
        else:
            reference_table[key] = (value, layer_num)


def _stat_replace_table_index(reference_table):
    """
    统计替换表的元素下标
    """
    index_dict = {}
    for key, (value, layer_num) in reference_table.items():
        replace_rt = _replace_rt_table(reference_table, value)
        index = index_dict.get(layer_num, 0) + 1
        index_dict[layer_num] = index
        reference_table[key] = (replace_rt, layer_num, index)


def _replace_rt_table(reference_table, value):
    """
    替换引用表的上级引用
    """
    if isinstance(value, (list, tuple)):
        t = (f'{_get_reference(reference_table, v)}' if isinstance(v, (list, tuple)) else f'{format_value(v)}' for v in
             value)
        return f'{{{", ".join(t)}}}'
    return _by_default(value)


def _stat_reference_table(replace_table):
    """
    统计生成引用表
    """
    rt_dict = {}
    for rt_value, layer_num, _index_num in replace_table.values():
        layer_list = rt_dict.get(layer_num, [])
        layer_list.append(rt_value)
        rt_dict[layer_num] = layer_list
    return sorted(rt_dict.items(), key=lambda item: item[0], reverse=True)

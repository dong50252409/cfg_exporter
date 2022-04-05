import os
import typing

import cfg_exporter.util as util
from cfg_exporter.const import DataType
from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.export import BaseExport
from cfg_exporter.lang_template import lang
from cfg_exporter.tables.base.type import DefaultValue

EXTENSION = 'cs'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', EXTENSION)
BASE_TEMPLATE = f'{EXTENSION}_base.{TEMPLATE_EXTENSION}'


def _by_default(value):
    """
    默认Iter类型格式化
    """
    return f'{value}'


def _by_reference(replace_table):
    """
    引用Iter类型格式化
    """
    return lambda value: _get_reference(replace_table, value)


def _get_reference(replace_table, value):
    key = _by_default(value)
    if key in replace_table:
        _, layer_num, index_num = replace_table[key]
        return f'_rt_{layer_num}[{index_num}]'
    return f'{value}'


# Iter类型格式化函数
_format_iter_value = _by_default


def format_value(value):
    if isinstance(value, DataType.str):
        return f'"{value}"'
    elif isinstance(value, DataType.lang):
        return f'"{lang(value.text)}"'
    elif isinstance(value, DataType.iter):
        return _format_iter_value(value)
    elif isinstance(value, DefaultValue):
        return format_value(value.text)
    else:
        return f'{value}'


_data_type_details = {
    'str': 'string',
    'lang': 'string',
    'iter': 'object',
    'raw': 'string'
}


class CSExport(BaseExport):

    def __init__(self, args):
        global_vars = {'format_value': format_value}
        super().__init__(args, BASE_TEMPLATE_PATH, [EXTENSION], global_vars)

    def export(self, table_obj) -> typing.NoReturn:
        ctx = {
            'table_obj': table_obj, 'prefix': self.args.file_prefix
        }

        table_name = table_obj.table_name
        filename = f'{util.pascal_case(table_name)}Config.{EXTENSION}'

        if table_name in self.extend_templates.get(EXTENSION, []):
            self.render(filename, f'{table_name}.{EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(filename, BASE_TEMPLATE, ctx)

    def file_desc(self) -> str:
        return "// AUTO GENERATE BY CFG_EXPORTER\n"

    @staticmethod
    def naming_convention() -> typing.Any:
        import cfg_exporter.util as util
        return util.snake_case

    @staticmethod
    def data_type_detail(data_type_str) -> str:
        return _data_type_details.get(data_type_str, data_type_str)

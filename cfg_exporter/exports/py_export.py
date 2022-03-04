import os

from cfg_exporter.const import DataType
from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.export import BaseExport
from cfg_exporter.lang_template import lang
from cfg_exporter.tables.base.type import IgnoreValue

EXTENSION = 'py'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', EXTENSION)
BASE_TEMPLATE = f'{EXTENSION}_base.{TEMPLATE_EXTENSION}'


def format_value(value):
    if isinstance(value, DataType.str):
        return f'"{value}"'
    elif isinstance(value, DataType.lang):
        return f'"{lang(value.text)}"'
    elif isinstance(value, IgnoreValue):
        return format_value(value.text)
    else:
        return f'{value}'


_real_data_type = {
    DataType.int: 'int',
    DataType.int64: 'int',
    DataType.float: 'float',
    DataType.str: 'str',
    DataType.lang: 'str',
    DataType.iter: 'typing.Union[list, tuple]',
    DataType.raw: 'typing.Any'
}


def real_type(data_type):
    return _real_data_type[data_type]


class PyExport(BaseExport):

    def __init__(self, args):
        global_vars = {'format_value': format_value, 'real_type': real_type}
        super().__init__(args, BASE_TEMPLATE_PATH, [EXTENSION], global_vars)

    def export(self, table_obj):
        ctx = {
            'table_obj': table_obj, 'prefix': self.args.file_prefix
        }
        table_name = table_obj.table_name
        filename = f'{table_name}.{EXTENSION}'

        if table_name in self.extend_templates.get(EXTENSION, []):
            self.render(filename, f'{table_name}.{EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(filename, BASE_TEMPLATE, ctx)

    def file_desc(self) -> str:
        return "######################################\n" \
               "#   AUTO GENERATE BY CFG_EXPORTER    #\n" \
               "######################################\n"

import os
import typing

from cfg_exporter.const import TEMPLATE_EXTENSION, DataType
from cfg_exporter.exports.base.export import BaseExport
from cfg_exporter.lang_template import lang

EXTENSION = 'json'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', EXTENSION)
BASE_TEMPLATE = f'{EXTENSION}_base.{TEMPLATE_EXTENSION}'

tab = str.maketrans('()', '[]')


def format_value(value):
    if value is None:
        return '""'
    elif isinstance(value, DataType.str):
        return f'"{value}"'
    elif isinstance(value, DataType.iter):
        return f'{value}'.translate(tab)
    elif isinstance(value, DataType.lang):
        return f'"{lang(value.text)}"'
    else:
        return f'{value}'


class JSONExport(BaseExport):

    def __init__(self, args):
        global_vars = {'format_value': format_value}
        super().__init__(args, BASE_TEMPLATE_PATH, [EXTENSION], global_vars)

    def export(self, table_obj) -> typing.NoReturn:
        ctx = {'table_obj': table_obj}
        table_name = table_obj.table_name

        filename = f'{table_name}.{EXTENSION}'
        if table_name in self.extend_templates.get(EXTENSION, []):
            self.render(filename, f'{table_name}.{EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(filename, BASE_TEMPLATE, ctx)

    def file_desc(self) -> str:
        pass

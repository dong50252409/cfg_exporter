import os
from typing import Iterable

from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.export import BaseExport

EXTENSION = 'json'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', EXTENSION)
BASE_TEMPLATE = f'{EXTENSION}_base.{TEMPLATE_EXTENSION}'

tab = str.maketrans('()', '[]')


def format_value(value):
    if value is None:
        return '""'
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, Iterable):
        return f'{value}'.translate(tab)
    else:
        return f'{value}'


class JSONExport(BaseExport):

    def __init__(self, args):
        global_vars = {'format_value': format_value}
        super().__init__(args, BASE_TEMPLATE_PATH, [EXTENSION], global_vars)

    def export(self, table_obj):
        ctx = {'table_obj': table_obj}
        table_name = table_obj.table_name

        filename = f'{table_name}.{EXTENSION}'
        if table_name in self.extend_templates.get(EXTENSION, []):
            self.render(filename, f'{table_name}.{EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(filename, BASE_TEMPLATE, ctx)

    def file_desc(self) -> str:
        pass

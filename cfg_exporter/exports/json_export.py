import os
from typing import Iterable

from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.export import Export

JSON_EXTENSION = 'json'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', 'json')
JSON_BASE_TEMPLATE = f'json_base.{TEMPLATE_EXTENSION}'


def format_value(value):
    if value is None:
        return '""'
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, Iterable):
        return f'{value}'.replace('(', '[').replace(')', ']').replace('\'', '"')
    else:
        return f'{value}'


class JSONExport(Export):

    def __init__(self, args):
        global_vars = {'format_value': format_value}
        super().__init__(args, BASE_TEMPLATE_PATH, [JSON_EXTENSION], global_vars)

    def export(self, table_obj):
        ctx = {'table_obj': table_obj}
        table_name = table_obj.table_name

        erl_filename = f'{table_name}.{JSON_EXTENSION}'
        if table_name in self.extend_templates.get(JSON_EXTENSION, []):
            self.render(erl_filename, f'{table_name}.{JSON_EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(erl_filename, JSON_BASE_TEMPLATE, ctx)

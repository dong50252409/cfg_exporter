import os
from typing import Iterable

from cfg_exporter.exports.base.export import Export

BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', 'erl')
ERL_BASE_TEMPLATE = 'erl_base.tmpl'
HRL_BASE_TEMPLATE = 'hrl_base.tmpl'


def format_value(value):
    if value is None:
        return 'undefined'
    elif isinstance(value, str):
        return f'<<"{value}"/utf8>>'
    elif isinstance(value, Iterable):
        return f'{value}'.replace('(', '{').replace(')', '}')
    else:
        return f'{value}'


class ErlExport(Export):

    def __init__(self, table_obj, args):
        global_vars = {'format_value': format_value}
        super().__init__(table_obj, args, [BASE_TEMPLATE_PATH], global_vars)
        self.output = os.path.join(self.args.output, self.args.erl_dir)
        self.prefix = self.args.erl_prefix
        self.extent_templates = []

    def export(self):
        ctx = {'table_obj': self.table_obj, 'prefix': self.prefix}
        self.render(self.output, f'{self.prefix}{self.table_obj.table_name}.erl', ERL_BASE_TEMPLATE, ctx)
        self.render(self.output, f'{self.prefix}{self.table_obj.table_name}.hrl', HRL_BASE_TEMPLATE, ctx)

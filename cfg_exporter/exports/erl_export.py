import os
from typing import Iterable

from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.baseexport import BaseExport
from cfg_exporter.tables.base.raw import RawType

ERL_EXTENSION = 'erl'
HRL_EXTENSION = 'hrl'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', ERL_EXTENSION)
ERL_BASE_TEMPLATE = f'{ERL_EXTENSION}_base.{TEMPLATE_EXTENSION}'
HRL_BASE_TEMPLATE = f'{HRL_EXTENSION}_base.{TEMPLATE_EXTENSION}'


def format_value(value):
    if value is None:
        return 'undefined'
    elif isinstance(value, str):
        return f'<<"{value}"/utf8>>'
    elif isinstance(value, Iterable):
        return f'{value}'.replace('(', '{').replace(')', '}')
    elif isinstance(value, RawType):
        return f'{value}'
    else:
        return f'{value}'


class ErlExport(BaseExport):

    def __init__(self, args):
        global_vars = {'format_value': format_value}
        super().__init__(args, BASE_TEMPLATE_PATH, [ERL_EXTENSION, HRL_EXTENSION], global_vars)
        self.prefix = self.args.erl_prefix

    def export(self, table_obj):
        ctx = {'table_obj': table_obj, 'prefix': self.prefix}
        table_name = table_obj.table_name

        self.output = os.path.join(self.args.output, self.args.erl_dir)
        erl_filename = f'{table_name}.{ERL_EXTENSION}'
        if table_name in self.extend_templates.get(ERL_EXTENSION, []):
            self.render(erl_filename, f'{table_name}.{ERL_EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(erl_filename, ERL_BASE_TEMPLATE, ctx)

        self.output = os.path.join(self.args.output, self.args.hrl_dir)
        hrl_filename = f'{table_name}.{HRL_EXTENSION}'
        if table_name in self.extend_templates.get(HRL_EXTENSION, []):
            self.render(hrl_filename, f'{table_name}.{HRL_EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(hrl_filename, HRL_BASE_TEMPLATE, ctx)

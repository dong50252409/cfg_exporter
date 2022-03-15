import os

from cfg_exporter.const import TEMPLATE_EXTENSION, DataType
from cfg_exporter.exports.base.export import BaseExport
from cfg_exporter.lang_template import lang

ERL_EXTENSION = 'erl'
HRL_EXTENSION = 'hrl'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', ERL_EXTENSION)
ERL_BASE_TEMPLATE = f'{ERL_EXTENSION}_base.{TEMPLATE_EXTENSION}'
HRL_BASE_TEMPLATE = f'{HRL_EXTENSION}_base.{TEMPLATE_EXTENSION}'

tab = str.maketrans('()', '{}')


def format_value(value):
    if value is None:
        return 'undefined'
    elif isinstance(value, DataType.str):
        return f'<<"{value}"/utf8>>'
    elif isinstance(value, DataType.iter):
        return f'{value}'.translate(tab)
    elif isinstance(value, DataType.lang):
        return f'<<"{lang(value.text)}"/utf8>>'
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

    def file_desc(self) -> str:
        return "%%===================================\n" \
               "%%  AUTO GENERATE BY CFG_EXPORTER\n" \
               "%%===================================\n"

    @staticmethod
    def naming_convention():
        import cfg_exporter.util as util
        return util.snake_case

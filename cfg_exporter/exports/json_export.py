import os

from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.exports.base.export import Export

JSON_EXTENSION = 'json'
BASE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', 'json')
JSON_BASE_TEMPLATE = f'json_base.{TEMPLATE_EXTENSION}'


class JSONExport(Export):

    def __init__(self, args):
        super().__init__(args, BASE_TEMPLATE_PATH, [JSON_EXTENSION, JSON_EXTENSION])

    def export(self, table_obj):
        ctx = {'table_obj': table_obj}
        table_name = table_obj.table_name

        self.output = os.path.join(self.args.output, self.args.erl_dir)
        erl_filename = f'{self.prefix}{table_name}.{JSON_EXTENSION}'
        if table_name in self.extend_templates.get(JSON_EXTENSION, []):
            self.render(erl_filename, f'{table_name}.{JSON_EXTENSION}.{TEMPLATE_EXTENSION}', ctx)
        else:
            self.render(erl_filename, JSON_EXTENSION, ctx)

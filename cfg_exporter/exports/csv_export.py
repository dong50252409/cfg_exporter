import logging
import os

import csv

from cfg_exporter.const import DataType
from cfg_exporter.exports.base.export import BaseExport
from cfg_exporter.lang_template import lang


def format_value(value):
    if value is None:
        return ''
    elif isinstance(value, DataType.lang):
        return lang(value.text)
    else:
        return value


class CSVExport(BaseExport):

    def __init__(self, args):
        super().__init__(args, '', [], {})
        self._func_dict = {
            self.args.field_row: lambda table_obj: table_obj.field_names,
            self.args.type_row: lambda table_obj: (data_type.name for data_type in table_obj.data_types)
        }

        if self.args.desc_row is not None:
            self._func_dict[self.args.desc_row] = lambda table_obj: (desc if desc else '' for desc in
                                                                     table_obj.descriptions)

        if self.args.rule_row is not None:
            self._func_dict[self.args.rule_row] = lambda table_obj: (
                '|'.join(rule.rule_str for rule in rule_group) if rule_group else '' for rule_group in table_obj.rules)

        self._space_line = lambda table_obj: [''] * len(table_obj.field_names)

    def export(self, table_obj):
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        filename = f'{self.args.file_prefix}{table_obj.table_name}.csv'
        logging.debug(f'render {filename} ...')
        full_filename = os.path.join(self.args.output, filename)

        with open(full_filename, 'w', encoding=self.args.csv_encoding, newline='') as wf:
            csv_writer = csv.writer(wf)
            for line in range(1, self.args.data_row):
                func = self._func_dict.get(line, self._space_line)
                csv_writer.writerow(func(table_obj))
            for row in table_obj.row_iter:
                csv_writer.writerow(format_value(value) for value in row)

    def file_desc(self) -> str:
        pass

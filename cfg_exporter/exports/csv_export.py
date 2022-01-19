import logging
import os

import csv
from cfg_exporter.exports.base.export import BaseExport


class CSVExport(BaseExport):

    def __init__(self, args):
        super().__init__(args, '', [], {})

    def export(self, table_obj):
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        filename = f'{self.args.file_prefix}{table_obj.table_name}.csv'
        logging.debug(f'render {filename} ...')
        full_filename = os.path.join(self.args.output, filename)

        with open(full_filename, 'w', encoding=self.args.csv_encoding, newline='') as wf:
            csv_writer = csv.writer(wf)
            line = 1
            while True:
                if line == self.args.field_row:
                    csv_writer.writerow(table_obj.field_names)
                elif line == self.args.type_row:
                    csv_writer.writerow(data_type.name for data_type in table_obj.data_types)
                elif line == self.args.desc_row:
                    csv_writer.writerow(desc if desc else '' for desc in table_obj.descriptions)
                elif line == self.args.rule_row:
                    csv_writer.writerow(
                        '|'.join(rule.rule_str for rule in rule_group) if rule_group else ''
                        for rule_group in table_obj.rules)
                elif line == self.args.data_row:
                    break
                else:
                    csv_writer.writerow([''] * len(table_obj.field_names))
                line += 1
            csv_writer.writerows(table_obj.row_iter)

    def file_desc(self) -> str:
        pass

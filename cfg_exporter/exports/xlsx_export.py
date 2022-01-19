import logging
import os
from typing import Iterable

from openpyxl import Workbook

from cfg_exporter import RawType
from cfg_exporter.exports.base.export import BaseExport


class XLSXExport(BaseExport):

    def __init__(self, args):
        super().__init__(args, '', [], {})

    def export(self, table_obj):
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        filename = f'{self.args.file_prefix}{table_obj.table_name}.xlsx'
        logging.debug(f'render {filename} ...')
        full_filename = os.path.join(self.args.output, filename)
        wb = Workbook(write_only=True)
        sheet = wb.create_sheet()
        line = 1
        while True:
            if line == self.args.field_row:
                sheet.append(table_obj.field_names)
            elif line == self.args.type_row:
                sheet.append(data_type.name for data_type in table_obj.data_types)
            elif line == self.args.desc_row:
                sheet.append(desc if desc else '' for desc in table_obj.descriptions)
            elif line == self.args.rule_row:
                sheet.append(
                    '|'.join(rule.rule_str for rule in rule_group) if rule_group else '' for rule_group in
                    table_obj.rules)
            elif line == self.args.data_row:
                break
            else:
                sheet.append([])
            line += 1
        for row in table_obj.row_iter:
            sheet.append(
                '' if content is None else str(content) if isinstance(content, (Iterable, RawType)) else content for
                content in row)
        wb.save(full_filename)

    def file_desc(self) -> str:
        pass

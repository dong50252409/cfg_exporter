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
        sheet.append(table_obj.field_names)
        sheet.append(data_type.name for data_type in table_obj.data_types)
        sheet.append(desc if desc else '' for desc in table_obj.descriptions)
        sheet.append(
            '|'.join(rule.rule_str for rule in rule_group) if rule_group else '' for rule_group in table_obj.rules)
        sheet.append([])
        for row in table_obj.row_iter:
            sheet.append(
                '' if content is None else str(content) if isinstance(content, (Iterable, RawType)) else content for
                content in row)
        wb.save(full_filename)

    def file_desc(self) -> str:
        pass

import os

from openpyxl import Workbook
from cfg_exporter.exports.base.export import BaseExport


class XLSXExport(BaseExport):

    def __init__(self, args):
        super().__init__(args, '', [], {})

    def export(self, table_obj):
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        filename = f'{self.args.file_prefix}{table_obj.table_name}.xlsx'
        full_filename = os.path.join(self.args.output, filename)
        wb = Workbook()
        sheet = wb.active
        sheet.title = table_obj.table_name
        sheet.append(table_obj.field_names)
        sheet.append(data_type.name for data_type in table_obj.data_types)
        sheet.append(desc if desc else '' for desc in table_obj.descriptions)
        sheet.append(
            '|'.join(rule.rule_str for rule in rule_group) if rule_group else '' for rule_group in table_obj.rules)
        for row_idx, row in enumerate(table_obj.row_iter, 6):
            for col_idx, content in enumerate(row, 1):
                if content:
                    if isinstance(content, (int, float, str)):
                        sheet.cell(row=row_idx, column=col_idx).value = content
                    else:
                        sheet.cell(row=row_idx, column=col_idx).value = str(content)

        wb.save(full_filename)

    def file_desc(self) -> str:
        pass

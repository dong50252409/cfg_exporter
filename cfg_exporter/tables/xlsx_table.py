import openpyxl
from cfg_exporter.tables.base.table import Table


class XLSXTable(Table):
    def __init__(self, container, file, **kwargs):
        super().__init__(container, file, **kwargs)
        self.__default_sheet = kwargs["default_sheet"]

    def load_table(self):
        book = openpyxl.load_workbook(self.full_filename, read_only=True, data_only=True)
        sheet = book[book.sheetnames[self.__default_sheet - 1]]
        rows = list(sheet.iter_rows(values_only=True))
        super()._load_table(rows)

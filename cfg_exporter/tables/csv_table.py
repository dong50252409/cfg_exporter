import csv
from cfg_exporter.tables.base.table import Table


class CSVTable(Table):
    def __init__(self, container, file, args):
        super().__init__(container, file, args)

    def load_table(self):
        with open(self.full_filename, 'r', encoding='utf-8-sig') as f:
            rows = list(csv.reader(f))
        self._load_table(rows)

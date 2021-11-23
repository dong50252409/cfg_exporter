import csv
from cfg_exporter.tables.base.table import Table


class CSVTable(Table):
    def __init__(self, container, file, **kwargs):
        super().__init__(container, file, **kwargs)
        self.__encoding = kwargs["csv_encoding"]

    def load_column(self):
        with open(self.full_filename, "r", encoding=self.__encoding) as f:
            rows = list(csv.reader(f))
        super()._load_column(rows)

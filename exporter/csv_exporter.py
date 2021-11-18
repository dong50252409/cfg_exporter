# -*- coding: utf-8 -*-

import csv
import helper
from table import Table


class CSVTable(Table):
    def __init__(self, cfg_obj, file):
        super().__init__(cfg_obj, file)

    def load_column(self):
        with open(self.full_filename, "r", encoding=helper.args.csv_encoding) as f:
            rows = list(csv.reader(f))
        super()._load_column(rows)


def extension():
    return ".csv",

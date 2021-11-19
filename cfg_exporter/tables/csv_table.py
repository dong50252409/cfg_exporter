# -*- coding: utf-8 -*-

import csv

from cfg_exporter import helper
from cfg_exporter.tables.base.table import Table


class CSVTable(Table):
    def __init__(self, container, file):
        field_row = helper.args.field_row - 1
        type_row = helper.args.type_row - 1
        rule_row = helper.args.rule_row - 1 if helper.args.rule_row else None
        desc_row = helper.args.desc_row - 1 if helper.args.desc_row else None
        body_row = helper.args.body_row - 1
        super().__init__(container, file, field_row, type_row, rule_row, desc_row, body_row)

    def load_column(self):
        with open(self.full_filename, "r", encoding=helper.args.csv_encoding) as f:
            rows = list(csv.reader(f))
        super()._load_column(rows)

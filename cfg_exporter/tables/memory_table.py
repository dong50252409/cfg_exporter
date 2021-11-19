# -*- coding: utf-8 -*-
from cfg_exporter.tables.base.table import Table


class MemoryTable(Table):
    def __init__(self, container, file, **kwargs):
        field_row = kwargs["field_row"]
        type_row = kwargs["type_row"]
        rule_row = kwargs.get("rule_row", None)
        desc_row = kwargs.get("desc_row", None)
        body_row = kwargs["body_row"]
        super().__init__(container, file, field_row, type_row, rule_row, desc_row, body_row)
        self.__data_rows = kwargs["data_rows"]

    def load_column(self):
        super()._load_column(self.__data_rows)

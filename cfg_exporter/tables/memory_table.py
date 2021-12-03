from cfg_exporter.tables.base.table import Table


class MemoryTable(Table):
    def __init__(self, container, file, **kwargs):
        super().__init__(container, file, **kwargs)
        self.__data_rows = kwargs["data_rows"]

    def load_table(self):
        super()._load_table(self.__data_rows)

from cfg_exporter.tables.base.table import Table


class MemoryTable(Table):
    def __init__(self, container, file, args):
        super().__init__(container, file, args)

    def load_table(self):
        self._load_table(self.args.data_rows)

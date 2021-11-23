import os
from cfg_exporter.tables.base.column import Column, ColumnException


class Table(object):
    def __init__(self, container_obj, filename, **kwargs):
        self.__container_obj = container_obj
        self.__full_filename = os.path.abspath(filename)
        self.__field_row = kwargs["field_row"] - 1
        self.__type_row = kwargs["type_row"] - 1
        self.__rule_row = None
        if "rule_row" in kwargs:
            self.__rule_row = kwargs["rule_row"] - 1
        self.__desc_row = None
        if "desc_row" in kwargs:
            self.__desc_row = kwargs["desc_row"] - 1
        self.__body_row = kwargs["body_row"] - 1
        self.__columns = {}
        self.__columns_by_field = {}
        self.__global_rules = {}
        self.__is_load = False

    def _load_column(self, rows):
        try:
            body = rows[self.__body_row:]
            for col_num, field_name in enumerate(rows[self.__field_row]):
                column = Column(self, col_num)
                column.field_name = field_name
                column.data_type = rows[self.__type_row][col_num]
                if self.__rule_row is not None:
                    column.rules = rows[self.__rule_row][col_num]
                if self.__desc_row is not None:
                    column.description = rows[self.__desc_row][col_num]
                column.data_list = body
                self.__columns[col_num] = column
                self.__columns_by_field[field_name] = column
            self.__is_load = True
        except ColumnException as e:
            err = "table:%(table_name)s %(error)s" % {"table_name": self.table_name, "error": e.err}
            raise TableException(err)

    def get_table_obj(self, full_filename):
        return self.__container_obj.get_table_obj(full_filename)

    @property
    def full_filename(self):
        return self.__full_filename

    @property
    def filename(self):
        return os.path.basename(self.__full_filename)

    @property
    def table_name(self):
        return os.path.splitext(os.path.basename(self.__full_filename))[0]

    @property
    def field_name_row_num(self):
        return self.__field_row

    @property
    def data_type_row_num(self):
        return self.__type_row

    @property
    def body_row_num(self):
        return self.__body_row

    @property
    def rule_row_num(self):
        return self.__rule_row

    @property
    def description_row_num(self):
        return self.__desc_row

    @property
    def columns(self):
        return self.__columns

    @property
    def columns_by_field(self):
        return self.__columns_by_field

    @property
    def global_rules(self):
        return self.__global_rules

    @property
    def is_load(self):
        return self.__is_load

    def verify(self):
        for column in self.__columns.values():
            column.verify()
        for global_rule in self.__global_rules.values():
            global_rule.verify(self)

    def export(self):
        pass


class TableException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err

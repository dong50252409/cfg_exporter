# -*- coding: utf-8 -*-

import os
import helper

from column import Column, ColumnException


class Table(object):
    def __init__(self, cfg_obj, file):
        self.__cfg_obj = cfg_obj
        self.__full_filename = os.path.abspath(file)
        self.__table_name = os.path.basename(self.__full_filename)
        self.__columns = {}
        self.__columns_by_field = {}
        self.__global_rules = {}
        self.__is_load = False

    def _load_column(self, rows):
        try:
            body = rows[self.body_row_num:]
            for col_num, field_name in enumerate(rows[self.field_name_row_num]):
                column = Column(self, col_num)
                column.field_name = field_name
                column.data_type = rows[self.data_type_row_num][col_num]
                column.rules = rows[self.rule_row_num][col_num]
                column.description = rows[self.description_row_num][col_num]
                column.data_list = body
                self.__columns[col_num] = column
                self.__columns_by_field[field_name] = column
            self.__is_load = True
        except ColumnException as e:
            err = "table:%(table_name)s %(error)s" % {"table_name": self.table_name, "error": e.err}
            raise TableException(err)

    @property
    def field_name_row_num(self):
        return helper.args.field_row - 1

    @property
    def data_type_row_num(self):
        return helper.args.type_row - 1

    @property
    def body_row_num(self):
        return helper.args.body_row - 1

    @property
    def rule_row_num(self):
        return helper.args.rule_row - 1 if helper.args.rule_row else None

    @property
    def description_row_num(self):
        return helper.args.desc_row - 1 if helper.args.desc_row else None

    def get_table(self, table_name):
        return self.__cfg_obj.get_table_obj(table_name)

    @property
    def full_filename(self):
        return self.__full_filename

    @property
    def table_name(self):
        return self.__table_name

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

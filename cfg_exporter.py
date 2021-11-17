# -*- coding: utf-8 -*-

import glob
import helper
from os import path
from const import Extension


class CfgExporter(object):
    def __init__(self):
        self.cfg_dict = {}
        pass

    def __do_load_files(self, source, recursive):
        if path.isdir(source):
            for macro in Extension.__members__.values():
                for file in glob.glob(path.join(source, "**/*" + macro.value[0]), recursive=recursive):
                    cls = macro.value[1]
                    self.cfg_dict[path.abspath(file)] = type(cls.__name__, (cls,), dict())(self, file)
        elif path.isfile(source):
            for macro in Extension.__members__.values():
                if source.endswith(macro.value[0]):
                    cls = macro.value[1]
                    self.cfg_dict[path.abspath(source)] = type(cls.__name__, (cls,), dict())(self, source)

    def load_files(self):
        self.__do_load_files(helper.args.source, helper.args.recursive)

    def verify(self):
        for source, table_obj, in self.cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_column()
            table_obj.verify()

    def export(self):
        for source, table_obj, in self.cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_column()
            table_obj.export()

    def get_table_obj(self, table_name):
        full_filename = path.abspath(table_name)
        if path.exists(full_filename):
            if full_filename in self.cfg_dict:
                table_obj = self.cfg_dict[full_filename]
                if not table_obj.is_load:
                    table_obj.load_column()
            else:
                self.__do_load_files(full_filename, False)
                table_obj = self.cfg_dict[full_filename]
                table_obj.load_column()
            return table_obj
        return None

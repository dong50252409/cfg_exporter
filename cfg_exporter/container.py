# -*- coding: utf-8 -*-
import importlib
import os
import glob
import const


class Container(object):
    def __init__(self, source, recursive, target, export_type):
        self.__cfg_dict = {}
        self.__source = source
        self.__recursive = recursive
        self.__target = target
        self.__export_type = export_type

    def create_table_obj(self, cls, filename, **kwargs):
        table_obj = type(cls.__name__, (cls,), dict())(self, filename, **kwargs)
        if table_obj.table_name in self.__cfg_dict:
            old_table_obj = self.__cfg_dict[table_obj.table_name]
            print("waring the %(new_filename)s table has the same name as the %(old_filename)s table. "
                  "the %(old_filename)s table will be replaced" %
                  {"new_filename": table_obj.filename, "old_filename": old_table_obj.filename})
        self.__cfg_dict[table_obj.table_name] = table_obj

    def get_table_obj(self, table_name):
        if table_name in self.__cfg_dict:
            table_obj = self.__cfg_dict[table_name]
            if not table_obj.is_load:
                table_obj.load_column()
            return table_obj
        return None

    def import_table(self):
        for macro in const.ExtensionType.__members__.values():
            mod = importlib.import_module(macro.value.__module__)
            for ext in getattr(mod, "extension")():
                if os.path.isdir(self.__source):
                    source = os.path.join(self.__source, "**/*" + ext)
                    for file in glob.glob(source, recursive=self.__recursive):
                        self.create_table_obj(macro.value, file)
                elif os.path.isfile(self.__source) and self.__source.endswith(ext):
                    self.create_table_obj(macro.value, self.__source)

    def verify_table(self):
        for _, table_obj, in self.__cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_column()
            table_obj.verify()

    def export_table(self):
        for source, table_obj, in self.__cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_column()
            table_obj.export()

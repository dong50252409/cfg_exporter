# -*- coding: utf-8 -*-
import importlib
import os
import glob

import helper
import const


class CfgExporter(object):
    def __init__(self):
        self.cfg_dict = {}
        pass

    def __do_load_files(self, source, recursive):
        for macro in const.Extension.__members__.values():
            mod = importlib.import_module(macro.value.__module__)
            for ext in getattr(mod, "extension")():
                if os.path.isdir(source):
                    for file in glob.glob(os.path.join(source, "**/*" + ext), recursive=recursive):
                        cls = macro.value
                        self.cfg_dict[os.path.abspath(file)] = type(cls.__name__, (cls,), dict())(self, file)
                elif os.path.isfile(source) and source.endswith(ext):
                    cls = macro.value
                    self.cfg_dict[os.path.abspath(source)] = type(cls.__name__, (cls,), dict())(self, source)

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
        full_filename = os.path.abspath(table_name)
        if os.path.exists(full_filename):
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

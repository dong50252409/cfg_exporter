import os
import glob

from cfg_exporter.const import ExtensionType


class Container(object):
    def __init__(self, source, recursive, target, export_type, **kwargs):
        self.__cfg_dict = {}
        self.__source = source
        self.__recursive = recursive
        self.__target = target
        self.__export_type = export_type
        self.__kwargs = kwargs

    def set_data_rows(self, data_rows):
        self.__kwargs["data_rows"] = data_rows

    def create_table_obj(self, cls, filename):
        table_obj = type(cls.__name__, (cls,), dict())(self, filename, **self.__kwargs)
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
        for macro in ExtensionType.__members__.values():
            if os.path.isdir(self.__source):
                source = os.path.join(self.__source, "**/*.%(ext)s" % {"ext": macro.name})
                for file in glob.glob(source, recursive=self.__recursive):
                    self.create_table_obj(macro.value, file)
            elif os.path.isfile(self.__source) and self.__source.endswith(".%(ext)s" % {"ext": macro.name}):
                self.create_table_obj(macro.value, self.__source)

    def verify_table(self):
        for _, table_obj, in self.__cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_table()
            table_obj.verify()

    def export_table(self):
        for source, table_obj, in self.__cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_table()
            table_obj.export()

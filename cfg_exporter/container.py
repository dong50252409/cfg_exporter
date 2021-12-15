import os
import glob

from cfg_exporter.const import ExtensionType


class Container(object):
    def __init__(self, args):
        self.__cfg_dict = {}
        self.args = args
        cls = self.args.export_type.value
        self.__export_obj = type(cls.__name__, (cls,), dict())(self.args)

    def set_data_rows(self, data_rows):
        setattr(self.args, "data_rows", data_rows)

    def create_table_obj(self, cls, filename):
        table_obj = type(cls.__name__, (cls,), dict())(self, filename, self.args)
        if table_obj.table_name in self.__cfg_dict:
            old_table_obj = self.__cfg_dict[table_obj.table_name]
            print(f'waring the `{table_obj.filename}` table has the same name as the `{old_table_obj.filename}` table.'
                  f'the `{old_table_obj.filename}` table will be replaced')
        self.__cfg_dict[table_obj.table_name] = table_obj

    def has_table_and_field(self, table_name, field_name):
        if table_name in self.__cfg_dict:
            table_obj = self.__cfg_dict[table_name]
            if not table_obj.is_load:
                table_obj.load_table()
            return True, field_name in table_obj.field_names
        return False, False

    def get_table_obj(self, table_name):
        if table_name in self.__cfg_dict:
            table_obj = self.__cfg_dict[table_name]
            if not table_obj.is_load:
                table_obj.load_table()
            return table_obj

    def import_table(self):
        source = self.args.source
        for macro in ExtensionType.__members__.values():
            if os.path.isdir(source):
                source = os.path.join(source, '**', f'*.{macro.name}')
                for file in glob.glob(source, recursive=self.args.recursive):
                    self.create_table_obj(macro.value, file)
            elif os.path.isfile(source) and source.endswith(f'.{macro.name}'):
                self.create_table_obj(macro.value, source)

    def verify_table(self):
        for _, table_obj, in self.__cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_table()
            table_obj.verify()

    def export_table(self):
        for source, table_obj, in self.__cfg_dict.items():
            if not table_obj.is_load:
                table_obj.load_table()
            self.__export_obj.export(table_obj)

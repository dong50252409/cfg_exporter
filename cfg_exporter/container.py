import os
import shutil
import glob
import logging
from cfg_exporter.language import LANG
from cfg_exporter.const import ExtensionType


class Container(object):
    def __init__(self, source, args):
        self._cfg_dict = {}
        self._skipped_cfg_dict = {}
        self._source = source
        self._effect_cfg_list = []
        self.args = args
        log_level = logging.NOTSET if self.args.verbose else logging.WARNING
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s: %(message)s')
        cls = self.args.export_type.value
        self.__export_obj = type(cls.__name__, (cls,), dict())(self.args)

    def create_table_obj(self, cls, filename):
        table_obj = type(cls.__name__, (cls,), dict())(self, filename, self.args)
        if table_obj.table_name in self._cfg_dict:
            old_table_obj = self._cfg_dict[table_obj.table_name]
            logging.warning(LANG.REPLACE_TABLE.format(new_filename=table_obj.full_filename,
                                                      old_filename=old_table_obj.full_filename))
        self._cfg_dict[table_obj.table_name] = table_obj

    def has_table_and_field(self, table_name, field_name):
        table_obj = self.get_table_obj(table_name)
        if table_obj:
            return True, field_name in table_obj.field_names

        return False, False

    def get_table_obj(self, table_name):
        if table_name in self._cfg_dict:
            table_obj = self._cfg_dict[table_name]
            if not table_obj.is_load:
                table_obj.load_table()
            return table_obj
        elif table_name in self._skipped_cfg_dict:
            macro, file = self._skipped_cfg_dict.pop(table_name)
            logging.debug(LANG.REFERENCE_TABLE.format(table=file))
            self.create_table_obj(macro.value, file)
            return self.get_table_obj(table_name)

    def import_table(self):
        for macro in ExtensionType.__members__.values():
            source = self.args.source
            if os.path.isdir(source):
                if self.args.recursive:
                    source = os.path.join(source, '**', f'*.{macro.name}')
                else:
                    source = os.path.join(source, f'*.{macro.name}')
                for file in glob.iglob(source, recursive=self.args.recursive):
                    file = os.path.abspath(file)
                    basename = os.path.basename(file)
                    if basename not in self.args.exclude_files:
                        if basename in self._source and self._source[basename] == os.stat(file).st_mtime:
                            self._skipped_cfg_dict[os.path.splitext(basename)[0]] = (macro, file)
                        else:
                            self.create_table_obj(macro.value, file)

            elif os.path.isfile(source) and source.endswith(f'.{macro.name}'):
                self.create_table_obj(macro.value, source)
        self._effect_cfg_list = list(self._cfg_dict.keys())

    def import_custom_table(self, cls, filename, data_rows):
        setattr(self.args, "data_rows", data_rows)
        self.create_table_obj(cls, filename)
        self._effect_cfg_list = list(self._cfg_dict.keys())

    def verify_table(self):
        for table_name in self._effect_cfg_list:
            table_obj = self._cfg_dict[table_name]
            if not table_obj.is_load:
                table_obj.load_table()
            table_obj.verify()

    def export_table(self):
        if self.args.clear_dir:
            shutil.rmtree(self.args.output, ignore_errors=True)
        for table_name in self._effect_cfg_list:
            table_obj = self._cfg_dict[table_name]
            if not table_obj.is_load:
                table_obj.load_table()
            self.__export_obj.export(table_obj)
            self._source[table_obj.filename] = os.stat(table_obj.full_filename).st_mtime

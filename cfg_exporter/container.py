import glob
import logging
import os
import shutil
import timeit

from cfg_exporter.const import ExtensionType
from cfg_exporter.lang_template import LangTemplate


class Container:
    def __init__(self, source, args):
        self._cfg_dict = {}
        self._skipped_cfg_dict = {}
        self._source = source
        self._effect_cfg_list = []
        self._args = args
        log_level = logging.NOTSET if self._args.verbose else logging.WARNING
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s: %(message)s')

    def __load_table(self, table_name):
        table_obj = self._cfg_dict[table_name]
        if not table_obj.is_load:
            logging.debug(_('loading table {table} ...').format(table=table_obj.filename))
            elapsed_time = '{:.3f}'.format(timeit.timeit(stmt=table_obj.load_table, number=1))
            logging.debug(_('table {table} loaded! elapsed time:{elapsed_time}/s')
                          .format(table=table_obj.filename, elapsed_time=elapsed_time))
        return table_obj

    def create_table_obj(self, cls, filename):
        table_obj = type(cls.__name__, (cls,), dict())(self, filename, self._args)
        if table_obj.table_name in self._cfg_dict:
            old_table_obj = self._cfg_dict[table_obj.table_name]
            logging.warning(_('waring! the {new_filename} table has been loaded '
                              'the {old_filename} table will be replaced')
                            .format(new_filename=table_obj.full_filename, old_filename=old_table_obj.full_filename))
        self._cfg_dict[table_obj.table_name] = table_obj

    def has_table_and_field(self, table_name, field_name):
        table_obj = self.get_table_obj(table_name)
        if table_obj:
            return True, field_name in table_obj.field_names

        return False, False

    def get_table_obj(self, table_name):
        if table_name in self._cfg_dict:
            return self.__load_table(table_name)
        elif table_name in self._skipped_cfg_dict:
            macro, file = self._skipped_cfg_dict.pop(table_name)
            logging.debug(_('reference table `{table}`').format(table=file))
            self.create_table_obj(macro.value, file)
            return self.get_table_obj(table_name)

    def import_table(self):
        for macro in ExtensionType.__members__.values():
            source = self._args.source
            if os.path.isdir(source):
                if self._args.recursive:
                    source = os.path.join(source, '**', f'*.{macro.name}')
                else:
                    source = os.path.join(source, f'*.{macro.name}')
                for file in glob.iglob(source, recursive=self._args.recursive):
                    file = os.path.abspath(file)
                    basename = os.path.basename(file)
                    if basename not in self._args.exclude_files:
                        if basename in self._source and self._source[basename] == os.stat(file).st_mtime:
                            self._skipped_cfg_dict[os.path.splitext(basename)[0]] = (macro, file)
                        else:
                            self.create_table_obj(macro.value, file)

            elif os.path.isfile(source) and source.endswith(f'.{macro.name}'):
                self.create_table_obj(macro.value, source)
        self._effect_cfg_list = list(self._cfg_dict.keys())

    def import_custom_table(self, cls, filename, data_rows):
        setattr(self._args, "data_rows", data_rows)
        self.create_table_obj(cls, filename)
        self._effect_cfg_list = list(self._cfg_dict.keys())

    def verify_table(self):
        for table_name in self._effect_cfg_list:
            table_obj = self.__load_table(table_name)
            table_obj.verify()

    def export_table(self):
        if self._args.clear_dir:
            shutil.rmtree(self._args.output, ignore_errors=True)

        cls = self._args.export_type.value
        export_obj = type(cls.__name__, (cls,), dict())(self._args)

        for table_name in self._effect_cfg_list:
            table_obj = self.__load_table(table_name)
            logging.debug(_('export {filename} ...').format(filename=table_obj.filename))
            elapsed_time = '{:.3f}'.format(timeit.timeit(stmt=lambda: export_obj.export(table_obj), number=1))
            logging.debug(_('export {filename} finished! elapsed_time:{elapsed_time}/s')
                          .format(filename=table_obj.filename, elapsed_time=elapsed_time))
            self._source[table_obj.filename] = os.stat(table_obj.full_filename).st_mtime

    def export_lang_template(self):
        lang_obj = LangTemplate(self._args)
        for table_name in self._effect_cfg_list:
            table_obj = self.__load_table(table_name)
            lang_obj.export(table_obj)

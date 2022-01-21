import os
import csv

from cfg_exporter.tables.base.type import LangType


class LangTemplate(object):
    def __init__(self, args):
        self._args = args
        self._csv_f = None
        if self._args.export_lang_template is not None:
            if not os.path.exists(self._args.export_lang_template):
                os.makedirs(self._args.export_lang_template)
            filename = os.path.join(self._args.export_lang_template, 'lang_template.csv')
            self._csv_f = open(filename, 'w', encoding='utf-8-sig', newline='')
            self._csv_writer = csv.writer(self._csv_f)
            self._csv_writer.writerow(['msgid', 'msgstr'])
        pass

    def export(self, table_obj):
        for field_name, data_type in zip(table_obj.field_names, table_obj.data_types):
            if data_type.value is LangType:
                self._csv_writer.writerow(['', ''])
                self._csv_writer.writerow([f'#: {table_obj.filename} {field_name} :#', ''])
                self._csv_writer.writerows(
                    [value, ''] for value in table_obj.data_iter_by_field_names(field_name)
                    if value is not None and value.text != '')

    def save(self):
        if self._csv_f:
            self._csv_f.close()


LANG = {}


def load(lang_template):
    global LANG
    with open(lang_template, 'r', encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))[2:]
        LANG = {row[0]: row[1] for row in rows if
                (not row[0].startswith('#: ') or not row[0].endswith(' :#')) and row[1] != ''}


def lang(s):
    return LANG.get(s, s)


__all__ = ('LangTemplate', 'lang', 'load')

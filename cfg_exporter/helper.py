import os
from argparse import RawTextHelpFormatter, ArgumentTypeError, ArgumentParser

from cfg_exporter.language import LANG
from cfg_exporter.const import ExportType, ExtensionType, TEMPLATE_EXTENSION


def valid_source(source):
    if os.path.exists(source):
        return source
    else:
        raise ArgumentTypeError(LANG.VALID_SOURCE.format(source=source))


def valid_export(export):
    if export in ExportType.__members__:
        return ExportType[export]
    else:
        raise ArgumentTypeError(LANG.VALID_EXPORT.format(export=export))


def valid_table(row_num):
    try:
        row_num = int(row_num)
        assert row_num > 0
        return row_num
    except (ValueError, AssertionError):
        raise ArgumentTypeError(LANG.VALID_TABLE.format(row_num=row_num))


parser = ArgumentParser(description=LANG.DESCRIPTION, formatter_class=RawTextHelpFormatter)

base_group = parser.add_argument_group(title=LANG.BASE_OPTIONS)

base_group.add_argument('--exclude_files', default=[], action="extend", nargs="+", help=LANG.EXCLUDE_FILES)

base_group.add_argument('-e', '--export_type', type=valid_export,
                        metavar=f'[{",".join(ExportType.__members__.keys())}]', help=LANG.EXPORT_TYPE)

base_group.add_argument('--file_prefix', default='', help=LANG.FILE_PREFIX)

base_group.add_argument('--force', default=False, action='store_true', help=LANG.FORCE)

base_group.add_argument('-o', '--output', type=str, default="", help=LANG.OUTPUT)

base_group.add_argument('-r', '--recursive', default=False, action='store_true', help=LANG.RECURSIVE)

base_group.add_argument('--verification', default=False, action='store_true', help=LANG.VERIFICATION)

base_group.add_argument('-s', '--source', type=valid_source, required=True,
                        help=LANG.SOURCE.format(extensions=",".join(ExtensionType.__members__.keys())))

base_group.add_argument('--template_path', help=LANG.TEMPLATE_PATH.format(template_extension=TEMPLATE_EXTENSION))

base_group.add_argument('--verbose', default=False, action='store_true', help=LANG.VERBOSE)

table_group = parser.add_argument_group(title=LANG.TABLE_OPTIONS)

table_group.add_argument('--data_row', type=valid_table, required=True, help=LANG.DATA_ROW)

table_group.add_argument('--desc_row', type=valid_table, help=LANG.DESC_ROW)

table_group.add_argument('--field_row', type=valid_table, required=True, help=LANG.FIELD_ROW)

table_group.add_argument('--rule_row', type=valid_table, help=LANG.RULE_ROW)

table_group.add_argument('--type_row', type=valid_table, required=True, help=LANG.TYPE_ROW)

csv_group = parser.add_argument_group(title=LANG.CSV_OPTIONS)

csv_group.add_argument('--csv_encoding', default='utf-8-sig', metavar='ENCODING', help=LANG.CSV_ENCODING)

erl_group = parser.add_argument_group(title=LANG.ERLANG_OPTIONS)

erl_group.add_argument('--erl_dir', default='', help=LANG.ERL_DIR)

erl_group.add_argument('--erl_prefix', default='', help=LANG.ERL_PREFIX)

erl_group.add_argument('--hrl_dir', default='', help=LANG.HRL_DIR)

args = parser.parse_args()

__all__ = 'args',

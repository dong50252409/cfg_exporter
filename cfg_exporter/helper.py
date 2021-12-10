import os
from argparse import RawTextHelpFormatter, ArgumentTypeError, ArgumentParser

from cfg_exporter.const import ExportType, ExtensionType, TEMPLATE_EXTENSION


def valid_source(source):
    if os.path.exists(source):
        return source
    else:
        raise ArgumentTypeError(f'the source path does not exists {source}')


def valid_export(export):
    if export in ExportType.__members__:
        return ExportType[export]
    else:
        raise ArgumentTypeError(f'the export file type does not exits {export}')


def valid_table(row_num):
    try:
        row_num = int(row_num)
        assert row_num > 0
        return row_num
    except (ValueError, AssertionError):
        raise ArgumentTypeError(f'{row_num} is not a valid line number')


def valid_default_sheet(sheet):
    try:
        sheet = int(sheet)
        assert sheet > 0
        return sheet
    except (ValueError, AssertionError):
        raise ArgumentTypeError(f'{sheet} is not a valid worksheet')


parser = ArgumentParser(description='Configuration table export toolset', formatter_class=RawTextHelpFormatter)

base_group = parser.add_argument_group(title='base options:')

base_group.add_argument('-s', '--source',
                        type=valid_source,
                        required=True,
                        help=f'specify the configuration table source path.\n'
                             f'supported file types '
                             f'[{",".join(ExtensionType.__members__.keys())}]')

base_group.add_argument('-r', '--recursive',
                        default=False,
                        action='store_true',
                        help='recursively search the source path.')

base_group.add_argument('-v', '--verification',
                        default=False,
                        action='store_true',
                        help='verify only the correctness of the configuration table.')

base_group.add_argument('-o', '--output',
                        type=str,
                        default="",
                        help='specify the configuration table output path.')

base_group.add_argument('-t', '--export_type',
                        type=valid_export,
                        metavar=f'[{",".join(ExportType.__members__.keys())}]',
                        help='specify the configuration table export type.')

base_group.add_argument('--template_path',
                        help='specify the extension template path.\n'
                             f'the template name consists of the table name, export type, '
                             f'and {TEMPLATE_EXTENSION} extension\n'
                             'e.g:\n'
                             f'`item.erl.{TEMPLATE_EXTENSION}` `item.lua.{TEMPLATE_EXTENSION}` ...\n'
                             'loads the template based on the specified export type\n'
                             'e.g\n'
                             f'`--export_type erl` templates ending with `.erl.{TEMPLATE_EXTENSION}` '
                             f'and `.hrl.{TEMPLATE_EXTENSION}` will be loaded\n'
                             f'`--export_type lua` templates ending with `.lua.{TEMPLATE_EXTENSION}` will be loaded')

table_group = parser.add_argument_group(title='table options:')

table_group.add_argument('--field_row',
                         type=valid_table,
                         required=True,
                         help='specify the line number of the configuration table field name.')

table_group.add_argument('--type_row',
                         type=valid_table,
                         required=True,
                         help='specify the line number of the configuration table data type.')

table_group.add_argument('--data_row',
                         type=valid_table,
                         required=True,
                         help='specify the start line number of the configuration table body data.')

table_group.add_argument('--rule_row',
                         type=valid_table,
                         help='specify the line number of the configuration table check rule.')

table_group.add_argument('--desc_row',
                         type=valid_table,
                         help='specify the line number of the configuration table column description.')

csv_group = parser.add_argument_group(title='csv options:')

csv_group.add_argument('--csv_encoding',
                       default='utf-8-sig',
                       metavar='ENCODING',
                       help='specify the default encoding format for CSV files.\n'
                            'DEFAULT UTF-8')

xlsx_group = parser.add_argument_group(title='xlsx options:')

xlsx_group.add_argument('--default_sheet',
                        type=valid_default_sheet,
                        default=1,
                        metavar='SHEET_NUM',
                        help='specify the default worksheet for XLSX files.\n'
                             'DEFAULT 1')

erl_group = parser.add_argument_group(title='erlang options:')

erl_group.add_argument('--erl_prefix',
                       default='',
                       help='specify the prefix of filename and record name.')

erl_group.add_argument('--erl_dir',
                       default='',
                       help='specify output directory for where to generate the .erl.')

erl_group.add_argument('--hrl_dir',
                       default='',
                       help='specify output directory for where to generate the .hrl.')

args = parser.parse_args()

__all__ = args

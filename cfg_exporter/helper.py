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


parser = ArgumentParser(description='Configuration table export toolset', formatter_class=RawTextHelpFormatter)

base_group = parser.add_argument_group(title='base options:')

base_group.add_argument('--exclude_files',
                        default=[],
                        action="extend",
                        nargs="+",
                        help='specify a list of file names not to load.')

base_group.add_argument('-e', '--export_type',
                        type=valid_export,
                        metavar=f'[{",".join(ExportType.__members__.keys())}]',
                        help='specify the configuration table export type.')

base_group.add_argument('--file_prefix',
                        default='',
                        help='specify the prefix of the output filename.')

base_group.add_argument('-o', '--output',
                        type=str,
                        default="",
                        help='specify the configuration table output path.')

base_group.add_argument('-r', '--recursive',
                        default=False,
                        action='store_true',
                        help='recursively search the source path.')

base_group.add_argument('--verification',
                        default=False,
                        action='store_true',
                        help='verify only the correctness of the configuration table.')

base_group.add_argument('-s', '--source',
                        type=valid_source,
                        required=True,
                        help=f'specify the configuration table source path.\n'
                             f'supported file types '
                             f'[{",".join(ExtensionType.__members__.keys())}]')

base_group.add_argument('--template_path',
                        help='specify the extension template path.\n'
                             f'the template name consists of the table name, export type, '
                             f'and {TEMPLATE_EXTENSION} extension\n'
                             'e.g:\n'
                             f'`item.erl.{TEMPLATE_EXTENSION}` `item.hrl.{TEMPLATE_EXTENSION}` '
                             f'`item.lua.{TEMPLATE_EXTENSION}` ...\n'
                             'loads the template based on the specified export type\n'
                             'e.g\n'
                             f'`--export_type erl` templates ending with `.erl.{TEMPLATE_EXTENSION}` '
                             f'and `.hrl.{TEMPLATE_EXTENSION}` will be loaded\n'
                             f'`--export_type lua` templates ending with `.lua.{TEMPLATE_EXTENSION}` will be loaded')

base_group.add_argument('--verbose',
                        default=False,
                        action='store_true',
                        help='show the details.')

table_group = parser.add_argument_group(title='table options:')

table_group.add_argument('--data_row',
                         type=valid_table,
                         required=True,
                         help='specify the start line number of the configuration table body data.')

table_group.add_argument('--desc_row',
                         type=valid_table,
                         help='specify the line number of the configuration table column description.')

table_group.add_argument('--field_row',
                         type=valid_table,
                         required=True,
                         help='specify the line number of the configuration table field name.')

table_group.add_argument('--rule_row',
                         type=valid_table,
                         help='specify the line number of the configuration table check rule.')

table_group.add_argument('--type_row',
                         type=valid_table,
                         required=True,
                         help='specify the line number of the configuration table data type.')

csv_group = parser.add_argument_group(title='csv options:')

csv_group.add_argument('--csv_encoding',
                       default='utf-8-sig',
                       metavar='ENCODING',
                       help='specify the default encoding format for CSV files.\n'
                            'DEFAULT UTF-8')

xlsx_group = parser.add_argument_group(title='xlsx options:')

xlsx_group.add_argument('--multi_sheets',
                        default=False,
                        action='store_true',
                        help='an XLSX file contains multiple worksheets that must begin with an XLSX file name.\n'
                             'e.g `item.xlsx` file contains worksheets such as `item` `item_type` `Sheet1`\n'
                             'it will load the `item` and `item_type` worksheets')

erl_group = parser.add_argument_group(title='erlang options:')

erl_group.add_argument('--erl_dir',
                       default='',
                       help='specify output directory for where to generate the .erl.')

erl_group.add_argument('--erl_prefix',
                       default='',
                       help='specify the prefix of the record name.')

erl_group.add_argument('--hrl_dir',
                       default='',
                       help='specify output directory for where to generate the .hrl.')

args = parser.parse_args()

__all__ = 'args',

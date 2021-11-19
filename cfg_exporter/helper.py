# -*- coding: utf-8 -*-
import os
from argparse import RawTextHelpFormatter, ArgumentTypeError, ArgumentParser

from cfg_exporter.const import ExportType, ExtensionType


def valid_source(source):
    if os.path.exists(source):
        return source
    else:
        err = "the source path does not exists %(source)s" % {"source": source}
        raise ArgumentTypeError(err)


def valid_export(export):
    if export in ExportType.__members__:
        return ExportType[export]
    else:
        err = "the export file type does not exits %(export)s" % {"export": export}
        raise ArgumentTypeError(err)


def valid_table(row_num):
    try:
        row_num = int(row_num)
        assert row_num > 0
        return row_num
    except (ValueError, AssertionError):
        err = "%(row_num)s is not a valid line number" % {"row_num": row_num}
        raise ArgumentTypeError(err)


def valid_default_sheet(sheet):
    try:
        sheet = int(sheet)
        assert sheet > 0
        return sheet
    except (ValueError, AssertionError):
        err = "%(sheet)s is not a valid worksheet" % {"sheet": sheet}
        raise ArgumentTypeError(err)


parser = ArgumentParser(description="Configuration table export toolset", formatter_class=RawTextHelpFormatter)

base_group = parser.add_argument_group(title="base options:")

base_group.add_argument("-s", "--source",
                        type=valid_source,
                        required=True,
                        help="specify the configuration table import source path.\n"
                             "supported file types [%(supported)s]" %
                             {"supported": ",".join([macro.name for macro in ExtensionType.__members__.values()])})

base_group.add_argument("-r", "--recursive",
                        default=False,
                        action="store_true",
                        help="search the source path recursively.")

base_group.add_argument("-t", "--target",
                        type=str,
                        required=True,
                        help="specify the configuration table export target path.")

base_group.add_argument("-e", "--export",
                        type=valid_export,
                        required=True,
                        metavar="[%(choices)s]" % {"choices": ",".join(ExportType.__members__.keys())},
                        help="specify export file type.")

table_group = parser.add_argument_group(title="table options:")

table_group.add_argument("--field_row",
                         type=valid_table,
                         required=True,
                         help="specify the row number of the configuration table field name.")

table_group.add_argument("--type_row",
                         type=valid_table,
                         required=True,
                         help="specify the row number of the configuration table data type.")

table_group.add_argument("--body_row",
                         type=valid_table,
                         required=True,
                         help="specify the row number of the configuration table body content.")

table_group.add_argument("--rule_row",
                         type=valid_table,
                         help="specify the row number of the configuration table check rule.")

table_group.add_argument("--desc_row",
                         type=valid_table,
                         help="specify the row number of the configuration table column description.")

csv_group = parser.add_argument_group(title="csv options:")
csv_group.add_argument("--csv_encoding",
                       default="utf-8",
                       metavar="ENCODING",
                       help="specify the default encoding format for CSV files.\n"
                            "DEFAULT utf-8")

xlsx_group = parser.add_argument_group(title="xlsx options:")

xlsx_group.add_argument("--default_sheet",
                        type=valid_default_sheet,
                        default=1,
                        metavar="SHEET_NUM",
                        help="specify the default worksheet for XLSX files.\n"
                             "DEFAULT 1")

args = parser.parse_args()

#!/usr/bin/env python3

# import multiprocessing

import cfg_exporter.helper as helper
from container import Container


def table_args():
    kwargs.update({
        "field_row": helper.args.field_row,
        "type_row": helper.args.type_row,
        "rule_row": helper.args.rule_row,
        "desc_row": helper.args.desc_row,
        "body_row": helper.args.body_row
    })


def csv_args():
    kwargs.update({
        "csv_encoding": helper.args.csv_encoding
    })


def xlsx_args():
    kwargs.update({
        "default_sheet": helper.args.default_sheet
    })


if __name__ == '__main__':
    # multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    source = helper.args.source
    recursive = helper.args.source
    target = helper.args.source
    export_type = helper.args.source
    kwargs = {}
    table_args()
    csv_args()
    xlsx_args()

    obj = Container(source, recursive, target, export_type, **kwargs)
    obj.import_table()
    obj.verify_table()
    obj.export_table()

    pass

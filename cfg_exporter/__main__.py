#!/usr/bin/env python3

# import multiprocessing
import logging

import cfg_exporter.helper as helper
from cfg_exporter.container import Container
from cfg_exporter.tables.base.table import TableException

if __name__ == '__main__':
    # multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    try:
        obj = Container(helper.args)
        obj.import_table()
        obj.verify_table()
        if not helper.args.verification and helper.args.export_type is not None:
            obj.export_table()
    except TableException as e:
        logging.error(e.err)
    pass

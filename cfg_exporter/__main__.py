#!/usr/bin/env python3

# import multiprocessing
import logging
import hashlib
import json
import os
import timeit
import sys
import cfg_exporter.helper as helper
from cfg_exporter.container import Container
from cfg_exporter.language import LANG
from cfg_exporter.tables.base.table import TableException

SOURCE_DIR = '.source'


def __load_source(args):
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)

    filename = hashlib.md5(f'{args.source}_{args.output}'.encode('utf8')).hexdigest()
    filename = os.path.join(SOURCE_DIR, filename)

    if args.force:
        return filename, {}

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return filename, json.load(f)
    else:
        return filename, {}


def run():
    try:
        filename, source = __load_source(helper.args)
        obj = Container(source, helper.args)
        obj.import_table()
        obj.verify_table()
        if not helper.args.verification and helper.args.export_type is not None:
            obj.export_table()
            with open(filename, 'w') as f:
                json.dump(source, f)
    except TableException as e:
        logging.error(e.err)


if __name__ == '__main__':
    # multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    logging.info(LANG.FINISHED.format(timeit.timeit(stmt=run, number=1)))
    pass

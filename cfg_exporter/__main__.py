#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import multiprocessing

from cfg_exporter import helper
from container import Container

if __name__ == '__main__':
    # multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    source = helper.args.source
    recursive = helper.args.source
    target = helper.args.source
    export_type = helper.args.source
    obj = Container(source, recursive, target, export_type)
    obj.import_table()
    obj.verify_table()
    obj.export_table()
    pass

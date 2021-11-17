#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import multiprocessing

from cfg_exporter import CfgExporter

if __name__ == '__main__':
    # multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    cfg = CfgExporter()
    cfg.load_files()
    cfg.verify()
    pass

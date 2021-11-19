# -*- coding: utf-8 -*-
import os

from cfg_exporter.const import ExportType
from cfg_exporter.container import Container
from cfg_exporter.tables.memory_table import MemoryTable


def test_key_rule():
    fields = ["id"]
    types = ["int"]
    rules = ["key:1"]
    body = [
        ["1"],
        ["2"],
        ["3"],
        ["4"],
    ]
    rows = [fields, types, rules, body]
    kwargs = {"field_row": 0, "type_row": 1, "rule_row": 2, "body_row": 3, "data_rows": rows}
    obj = Container(os.path.curdir, False, os.path.curdir, ExportType.erl)
    obj.create_table_obj(MemoryTable.__name__, "memory_table", **kwargs)
    pass


def test_macro_rule():
    pass


def test_ref_rule():
    pass


def test_len_rule():
    pass


def test_range_rule():
    pass


def test_source_rule():
    pass


def test_unique_rule():
    pass


def test_not_empty_rule():
    pass

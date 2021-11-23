# -*- coding: utf-8 -*-
from cfg_exporter.container import Container
from cfg_exporter.tables.memory_table import MemoryTable


def table_args():
    return {
        "field_row": 1,
        "type_row": 2,
        "rule_row": 3,
        "body_row": 4
    }


def test_content_1():
    fields = ["id", "macro_name", "macro_desc", "test_ref", "test_len", "test_range", "test_source", "test_unique",
              "test_not_empty"]
    types = ["int", "str", "str", "int", "str", "int", "str", "int", "int"]
    rules = ["key:1|macro:value", "macro:name", "macro:desc",
             "ref:%(table_name)s.id" % {"table_name": test_content_2.__name__},
             "len:10", "range:0-500", "source:.", "unique", "not_empty"]
    body = [
        [1, "key_1", "desc_1", 100, "abc", 0, "test_rule.py", 1, 1],
        [2, "key_2", "desc_2", 200, "abcd", 500, "__init__.py", 2, 2],
        [3, "key_3", "desc_3", 300, "abcde", 255, ".pytest_cache/README.md", 3, 3],
        [4, "key_4", "desc_4", 400, "abcdef", 123, ".pytest_cache/v/cache/stepwise", 4, 4],
        [5, "", "", "", "", "", "", "", 6],
    ]
    return [fields, types, rules] + body


def test_content_2():
    fields = ["id"]
    types = ["int"]
    rules = ["key:1"]
    body = [
        [100], [200], [300], [400], [500], [600]
    ]
    return [fields, types, rules] + body


def test_base():
    kwargs = table_args()
    obj1 = Container("", False, "", "", **kwargs)
    obj1.set_data_rows(test_content_1())
    obj1.create_table_obj(MemoryTable, test_content_1.__name__)
    obj1.set_data_rows(test_content_2())
    obj1.create_table_obj(MemoryTable, test_content_2.__name__)
    obj1.verify_table()
    pass


def test_key_rule():
    pass


def test_macro_rule():
    pass


def test_ref_rule():
    pass


#

def test_len_rule():
    pass


def test_range_rule():
    pass


#
def test_source_rule():
    pass


#
#
def test_unique_rule():
    pass


#
#
def test_not_empty_rule():
    pass
#

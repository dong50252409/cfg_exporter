# -*- coding: utf-8 -*-
import sys

import pytest

from cfg_exporter.container import Container
from cfg_exporter.tables.base.table import TableException
from cfg_exporter.tables.memory_table import MemoryTable


def table_args():
    return {
        "field_row": 1,
        "type_row": 2,
        "rule_row": 3,
        "body_row": 4
    }


def content_1():
    fields = ["id1", "id2", "macro_name", "macro_desc", "test_ref", "test_len", "test_range", "test_source",
              "test_unique", "test_not_empty"]
    types = ["int", "int", "str", "str", "int", "str", "int", "str", "int", "int"]
    rules = ["key:1|macro:value", "key:2", "macro:name", "macro:desc",
             "ref:%(table_name)s.id" % {"table_name": content_2.__name__},
             "len:10", "range:0-500", "source:.", "unique", "not_empty"]
    body = [
        [1, 9, "key_1", "desc_1", 100, "abc", 0, "test_rule.py", 1, 1],
        [2, 8, "key_2", "desc_2", 200, "abcd", 500, "__init__.py", 2, 2],
        [3, 7, "key_3", "desc_3", 300, "abcde", 255, ".pytest_cache/README.md", 3, 3],
        [4, 6, "key_4", "desc_4", 400, "abcdef", 123, ".pytest_cache/v/cache/stepwise", 4, 4],
        [5, 5, "", "", "", "", "", "", "", 6], ]
    return [fields, types, rules] + body


def content_2():
    fields = ["id"]
    types = ["int"]
    rules = ["key:1"]
    body = [
        [100], [200], [300], [400], [500], [600]
    ]
    return [fields, types, rules] + body


def exception_verity(rows):
    kwargs = table_args()
    with pytest.raises(Exception) as err:
        obj1 = Container("", False, "", "", **kwargs)
        obj1.set_data_rows(rows)
        obj1.create_table_obj(MemoryTable, sys._getframe().f_code.co_name)
        obj1.verify_table()
    assert err.type is TableException
    print(err.value)


def test_base():
    kwargs = table_args()
    obj1 = Container("", False, "", "", **kwargs)
    obj1.set_data_rows(content_1())
    obj1.create_table_obj(MemoryTable, content_1.__name__)
    obj1.set_data_rows(content_2())
    obj1.create_table_obj(MemoryTable, content_2.__name__)
    obj1.verify_table()
    pass


def test_key_rule():
    heads = [["id1", "id2"], ["int", "int"], ["key:a", "key:2"]]
    exception_verity(heads)

    heads = [["id1", "id2"], ["int", "int"], ["key:1", "key:1"]]
    exception_verity(heads)

    heads = [["id1", "id2"], ["int", "int"], ["key:1", "key:2"]]
    body = [["1", "1"], ["1", "1"]]
    exception_verity(heads + body)

    body = [["1", "1"], ["1", ""]]
    exception_verity(heads + body)
    pass


def test_macro_rule():
    heads = [["id"], ["int"], ["macro:value1"]]
    exception_verity(heads)

    heads = [["id1", "id2", "name"], ["int", "int", "str"], ["macro:value", "macro:value", "macro:name"]]
    body = [["1", "3", "a"], ["2", "4", "b"]]
    exception_verity(heads + body)

    heads = [["id"], ["int"], ["macro:value"]]
    body = [["1"], ["2"]]
    exception_verity(heads + body)

    heads = [["name"], ["str"], ["macro:name"]]
    body = [["a"], ["b"]]
    exception_verity(heads + body)

    heads = [["id", "value"], ["int", "int"], ["macro:value", "macro:name"]]
    body = [["1", "10"], ["2", "20"]]
    exception_verity(heads + body)

    heads = [["id", "name"], ["int", "str"], ["macro:value", "macro:name"]]
    body = [["1", "a"], ["1", "a"]]
    exception_verity(heads + body)
    pass


def test_ref_rule():
    heads = [["id"], ["int"], ["ref:table-field"]]
    exception_verity(heads)

    heads = [["id"], ["int"], ["ref:table.field"]]
    exception_verity(heads)

    kwargs = table_args()
    with pytest.raises(Exception) as err:
        heads1 = [["id"], ["int"], ["ref:test_ref_rule_3.id"]]
        body1 = [["1"], ["2"], ["3"]]
        heads3 = [["id"], ["int"], [""]]
        body3 = [["1"], ["2"]]
        obj1 = Container("", False, "", "", **kwargs)
        obj1.set_data_rows(heads1 + body1)
        obj1.create_table_obj(MemoryTable, "test_ref_rule_1")
        obj1.set_data_rows(heads3 + body3)
        obj1.create_table_obj(MemoryTable, "test_ref_rule_3")
        obj1.verify_table()
    assert err.type is TableException
    print(err.value)

    with pytest.raises(Exception) as err:
        heads2 = [["id"], ["int"], ["ref:test_ref_rule_3.id1"]]
        body2 = [["1"], ["2"], ["3"]]
        heads3 = [["id"], ["int"], [""]]
        body3 = [["1"], ["2"]]
        obj1 = Container("", False, "", "", **kwargs)
        obj1.set_data_rows(heads2 + body2)
        obj1.create_table_obj(MemoryTable, "test_ref_rule_2")
        obj1.set_data_rows(heads3 + body3)
        obj1.create_table_obj(MemoryTable, "test_ref_rule_3")
        obj1.verify_table()
    assert err.type is TableException
    print(err.value)
    pass


def test_len_rule():
    heads = [["test_len"], ["int"], ["len:10"]]
    body = [["1"]]
    exception_verity(heads + body)

    heads = [["test_len"], ["str"], ["len:a"]]
    body = [["asd"]]
    exception_verity(heads + body)

    heads = [["test_len"], ["str"], ["len:5"]]
    body = [["asd"], ["12345"], ["123456"]]
    exception_verity(heads + body)

    pass


def test_range_rule():
    heads = [["test_range"], ["int"], ["range:10,50"]]
    body = [["10"]]
    exception_verity(heads + body)

    heads = [["test_range"], ["str"], ["range:a-b"]]
    body = [["a"]]
    exception_verity(heads + body)

    heads = [["test_range"], ["int"], ["range:10-50"]]
    body = [["1"]]
    exception_verity(heads + body)
    pass


def test_source_rule():
    heads = [["test_source"], ["int"], ["source:."]]
    body = [["test_rule.py"]]
    exception_verity(heads + body)

    heads = [["test_source"], ["str"], ["source:."]]
    body = [["b.py"]]
    exception_verity(heads + body)
    pass


def test_unique_rule():
    heads = [["test_unique"], ["int"], ["unique"]]
    body = [["1"], ["2"], ["1"]]
    exception_verity(heads + body)
    pass


def test_not_empty_rule():
    heads = [["test_not_empty"], ["int"], ["not_empty"]]
    body = [["1"], ["2"], [""]]
    exception_verity(heads + body)
    pass

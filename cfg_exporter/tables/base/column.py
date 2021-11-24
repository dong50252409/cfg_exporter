from cfg_exporter import util
from cfg_exporter.tables.base.const import DataType, RuleType
from cfg_exporter.tables.base.rule import RuleException


class Column(object):
    def __init__(self, table_obj, column_num):
        self.__table_obj = table_obj
        self.__column_num = column_num
        self.__field_name = None
        self.__data_type = None
        self.__rules = []
        self.__description = None
        self.__data_list = []

    @property
    def table_obj(self):
        return self.__table_obj

    @property
    def column_num(self):
        return self.__column_num

    @property
    def real_column_num(self):
        return self.__column_num + 1

    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, field_name):
        if field_name is None:
            err = "%(row_num)s:%(column_num)s field name is undefined" % {
                "row_num": self.table_obj.real_field_name_row_num,
                "column_num": self.real_column_num
            }
            raise ColumnException(err)

        field_name = util.trim(field_name)

        if field_name == "":
            err = "%(row_num)s:%(column_num)s field name is undefined" % {
                "row_num": self.table_obj.real_field_name_row_num,
                "column_num": self.real_column_num
            }
            raise ColumnException(err)

        self.__field_name = util.trim(field_name)

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        if data_type is None:
            err = "%(row_num)s:%(column_num)s data type is undefined" % {
                "row_num": self.table_obj.real_data_type_row_num,
                "column_num": self.real_column_num
            }
            raise ColumnException(err)

        data_type = util.trim(data_type)

        if data_type == "":
            err = "%(row_num)s:%(column_num)s data type is undefined" % {
                "row_num": self.table_obj.real_data_type_row_num,
                "column_num": self.real_column_num
            }
            raise ColumnException(err)

        if data_type not in DataType.__members__:
            err = "%(row_num)s:%(column_num)s data type `%(data_type)s` is unsupported\n" \
                  "supported data types [%(support_data_type)s]" % {
                      "row_num": self.table_obj.real_data_type_row_num,
                      "column_num": self.real_column_num,
                      "data_type": data_type,
                      "support_data_type": ",".join(DataType.__members__.keys())
                  }
            raise ColumnException(err)

        self.__data_type = DataType[data_type].value

    @property
    def rules(self):
        return self.__rules

    @rules.setter
    def rules(self, rule):
        if rule is None:
            return

        rule = util.trim(rule)

        if rule != "":
            for rule_str in rule.split("|"):
                try:
                    # 规则条件有两种类型 tag、tag:clause
                    tag_and_clause = rule_str.split(":")
                    assert len(tag_and_clause) <= 2
                    cls = RuleType[tag_and_clause[0]].value
                    rule_obj = type(cls.__name__, (cls,), dict())(self, rule_str)
                    rule_obj.value = tag_and_clause[-1]
                    self.__rules.append(rule_obj)
                except (AssertionError, ValueError, KeyError):
                    err = "%(data_type_row_num)s:%(column_num)s data_type:`%(data_type)s` is not match " \
                          "or %(rule_row_num)s:%(column_num)s rule:`%(rule)s` formal error" % {
                              "data_type_row_num": self.table_obj.real_data_type_row_num,
                              "rule_row_num": self.table_obj.real_rule_row_num,
                              "column_num": self.real_column_num,
                              "rule": rule_str,
                              "data_type": self.__data_type.__name__
                          }
                    raise RuleException(err)

            self.__rules = tuple(self.__rules)

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, desc):
        if desc is None:
            return
        self.__description = util.trim(desc)

    @property
    def data_list(self):
        return self.__data_list

    @data_list.setter
    def data_list(self, rows):
        for row_num, row in enumerate(rows):
            if row[self.__column_num]:
                if self.__data_type is list or self.__data_type is tuple:
                    try:
                        data = eval(row[self.__column_num])
                        assert isinstance(data, self.__data_type)
                    except (SyntaxError, NameError, AssertionError):
                        err = "%(row_num)s:%(column_num)s incorrect data" % {
                            "row_num": self.table_obj.real_body_row_num + row_num,
                            "column_num": self.real_column_num
                        }
                        raise ColumnException(err)
                else:
                    data = self.__data_type(row[self.__column_num])
                self.__data_list.append(data)
            else:
                self.__data_list.append(None)
        self.__data_list = tuple(self.__data_list)

    def verify(self):
        for rule in self.__rules:
            rule.verify()


class ColumnException(Exception):
    def __init__(self, err):
        super().__init__(self)
        self.err = err

    def __str__(self):
        return self.err

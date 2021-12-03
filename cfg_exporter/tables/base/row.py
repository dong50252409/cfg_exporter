class Row(object):
    def __init__(self, table_obj, row_num):
        self.__table_obj = table_obj
        self.__row_num = row_num
        self.__field_name = None
        self.__data_type = None
        self.__rules = []
        self.__description = None
        self.__data_list = []

    @property
    def table_obj(self):
        return self.__table_obj

    @property
    def cow_num(self):
        return self.__row_num

    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, field_name):
        self.__field_name = field_name

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        self.__data_type = data_type

    @property
    def rules(self):
        return self.__rules

    @rules.setter
    def rules(self, rules):
        self.__rules = rules

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, desc):
        self.__description = desc

    @property
    def data_list(self):
        return self.__data_list

    @data_list.setter
    def data_list(self, data_list):
        self.__data_type = data_list

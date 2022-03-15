from collections import Counter

from cfg_exporter.tables.base.type import DefaultValue


def analyze_default_value(table_obj):
    """
    分析表默认值
    """
    from cfg_exporter.const import DataType
    default_values = {}
    for field_name, data_type in zip(table_obj.field_names, table_obj.data_types):
        if field_name in table_obj.key_field_name_iter:
            continue

        if data_type in (DataType.iter, DataType.lang, DataType.raw):
            counter = Counter(f'{value}' for value in table_obj.data_iter_by_field_names(field_name))
        else:
            counter = Counter(table_obj.data_iter_by_field_names(field_name))

        default_value, count = counter.most_common(1)[0]

        if count >= 3:
            if default_value is None:
                continue

            default_value = data_type.value(default_value)

            default_value_obj = DefaultValue(default_value)
            default_values[field_name] = default_value
            col_num = table_obj.column_num_by_field_name(field_name)

            for row_num, value in enumerate(table_obj.data_iter_by_column_nums(col_num)):
                if value == default_value:
                    table_obj.value(row_num, col_num, default_value_obj)
    return default_values

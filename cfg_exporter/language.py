import locale

en_US = {
    # helper.py
    'VALID_SOURCE': 'the source path does not exists {source}',
    'VALID_EXPORT': 'the export file type does not exits {export}',
    'VALID_TABLE': '{row_num} is not a valid line number',
    'DESCRIPTION': 'Configuration table export toolset',
    'BASE_OPTIONS': 'Base options',
    'CLEAR_DIR': 'clear the output directory',
    'EXCLUDE_FILES': 'specify a list of file names not to load.',
    'EXPORT_TYPE': 'specify the configuration table export type.',
    'FILE_PREFIX': 'specify the prefix of the output filename.',
    'FORCE': 'force all configuration tables to be generated.',
    'OUTPUT': 'specify the configuration table output path.',
    'RECURSIVE': 'recursively search the source path.',
    'VERIFICATION': 'verify only the correctness of the configuration table.',
    'SOURCE': 'specify the configuration table source path.\nsupported file types [{extensions}]',
    'TEMPLATE_PATH': 'specify the extension template path.\n'
                     'the template name consists of the table name, export type, '
                     'and {template_extension} extension\n'
                     'e.g:\n'
                     '`item.erl.{template_extension}` `item.hrl.{template_extension}` `item.lua.{template_extension}`\n'
                     'loads the template based on the specified export type\n'
                     'e.g:\n'
                     '`--export_type erl` templates ending with `.erl.{template_extension}` '
                     'and `.hrl.{template_extension}` will be loaded\n'
                     '`--export_type lua` templates ending with `.lua.{template_extension}` will be loaded',
    'VERBOSE': 'show the details.',
    'TABLE_OPTIONS': 'Table options',
    'DATA_ROW': 'specify the start line number of the configuration table body data.',
    'DESC_ROW': 'specify the line number of the configuration table column description.',
    'FIELD_ROW': 'specify the line number of the configuration table field name.',
    'RULE_ROW': 'specify the line number of the configuration table check rule.',
    'TYPE_ROW': 'specify the line number of the configuration table data type.',
    'CSV_OPTIONS': 'CSV options',
    'CSV_ENCODING': 'specify the default encoding format for CSV files.\nDEFAULT UTF-8',
    'ERLANG_OPTIONS': 'Erlang options',
    'ERL_DIR': 'specify output directory for where to generate the .erl.',
    'ERL_PREFIX': 'specify the prefix of the record name.',
    'HRL_DIR': 'specify output directory for where to generate the .hrl.',
    'REPLACE_TABLE': 'waring the `{new_filename}` table has the same name as the `{new_filename}` table.'
                     'the `{old_filename}` table will be replaced',
    'REFERENCE_TABLE': 'reference table {table}',
    # __main__.py
    'FINISHED': 'down! elapsed {:.3f} /s',
    # table.py
    'LOAD_TABLE': 'loading table {table} ...',
    'TABLE_LOADED': 'table {table} loaded! elapsed time:{elapsed_time}/s',
    'ROW_COL_NUM': 'r{row_num}:c{col_num}',
    'TABLE': 'table:`{table}`',
    'FIELD': 'field:`{field}`',
    'TYPE': 'type:`{type}`',
    'RULE': 'rule:`{rule}`',
    'INVALID_FIELD_NAME': 'invalid field name',
    'UNDEFINED_DATA_TYPE': 'the data type is undefined',
    'UNSUPPORTED_DATA_TYPE': 'data type `{type}` is unsupported\nsupported data types [{supported}]',
    'PARSE_RULE_EXCEPTION': 'is invalid rule',
    'CONVERT_DATA_EXCEPTION': 'type:`{type}` `{data}` is invalid data',
    # rule.py
    'KEY_RULE_PARSE_ERROR': 'already defined at r{row_num}:c{col_num}',
    'MACRO_RULE_NOT_EXIST': 'does not exist',
    'MACRO_RULE_DUPLICATE_DEFINITION': 'defined at r{row_num}:c{col_num}',
    'UNIQUE_RULE_FAILED': 'data:`{data}` is not unique already defined at r{row_num}:c{col_num}',
    'NOT_EMPTY_RULE_FAILED': 'the data is empty',
    'MIN_RULE_FAILED_1': 'data:`{data}` the minimum limit was not reached',
    'MIN_RULE_FAILED_2': 'data:`{data}` length:`{len}` the minimum limit was not reached',
    'MAX_RULE_FAILED_1': 'data:`{data}` the maximum limit was exceeded',
    'MAX_RULE_FAILED_2': 'data:`{data}` length:`{len}` the maximum limit was exceeded',
    'SOURCE_RULE_FAILED': 'data:`{data}` path not found',
    'REF_RULE_PARSE_ERROR_1': 'table:`{table}` does not exist',
    'REF_RULE_PARSE_ERROR_2': 'field:`{field}` does not exist',
    'REF_RULE_FAILED': 'data:`{data}` reference does not exist',
    'STRUCT_RULE_FAILED': 'index:`{row_num}` {err}',
    'GLOBAL_KEY_RULE_FAILED_1': 'primary key is empty',
    'GLOBAL_KEY_RULE_FAILED_2': 'primary key repeat at r{row_num}:c{col_num}',
    'GLOBAL_MACRO_RULE_FAILED_1': 'does not exist',
    'GLOBAL_MACRO_RULE_FAILED_2': 'data type is not `str`',
    'GLOBAL_MACRO_RULE_FAILED_3': 'invalid macro name',
    'GLOBAL_MACRO_RULE_FAILED_4': 'macro name repeat at r{row_num}:c{col_num}',
}

zh_CN = {
    # helper.py
    'VALID_SOURCE': '{source} 路径不存在。',
    'VALID_EXPORT': '{export} 导出文件类型不存在。',
    'VALID_TABLE': '{row_num} 不是有效的行号。',
    'DESCRIPTION': '配置表导出工具集。',
    'BASE_OPTIONS': '基础选项',
    'CLEAR_DIR': '清空输出目录。',
    'EXCLUDE_FILES': '指定排除加载的文件名列表。',
    'EXPORT_TYPE': '指定配置表导出类型。',
    'FILE_PREFIX': '指定导出文件名前缀。',
    'FORCE': '强制生成所有配置表。',
    'OUTPUT': '指定配置表输出路径。',
    'RECURSIVE': '搜索子文件夹下的内容。',
    'VERIFICATION': '仅验证配置表数据是否正确。',
    'SOURCE': '指定配置表源路径\n支持的配置表类型 [{extensions}]。',
    'TEMPLATE_PATH': '指定扩展模板路径。\n'
                     '模板名由表名、导出文件类型以及{template_extension}扩展名组成\n'
                     '例如：\n'
                     '`item.erl.{template_extension}` `item.hrl.{template_extension}` `item.lua.{template_extension}`\n'
                     '根据指定导出类型加载模板\n'
                     '例如：\n'
                     '`--export_type erl` 以 `.erl.{template_extension}`和`.hrl.{template_extension}` 结尾的模板将被载入\n'
                     '`--export_type lua` 以 `.lua.{template_extension}` 结尾的模板将被载入',
    'VERBOSE': '显示详情。',
    'TABLE_OPTIONS': '配置表选项',
    'DATA_ROW': '指定配置表数据起始行号。',
    'DESC_ROW': '指定配置表描述行号。',
    'FIELD_ROW': '指定配置表字段名行号。',
    'RULE_ROW': '指定配置表规则行号。',
    'TYPE_ROW': '指定配置表数据类型行号。',
    'CSV_OPTIONS': 'CSV 选项',
    'CSV_ENCODING': '指定读取CSV文件编码格式。\n默认 UTF-8',
    'ERLANG_OPTIONS': 'Erlang选项',
    'ERL_DIR': '指定.erl文件输出目录。',
    'ERL_PREFIX': '指定record字段名前缀名。',
    'HRL_DIR': '指定.hrl文件输出目录。',
    # __main__.py
    'FINISHED': '完成! 耗时 {:.3f} /秒',
    # table.py
    'LOAD_TABLE': '载入配置表 {table} ...',
    'TABLE_LOADED': '配置表 {table} 已载入! 耗时：{elapsed_time}/s',
    'ROW_COL_NUM': '行{row_num}:列{col_num}',
    'TABLE': '配置表:`{table}`',
    'FIELD': '字段:`{field}`',
    'TYPE': '类型:`{type}`',
    'RULE': '规则:`{rule}`',
    'INVALID_FIELD_NAME': '非法的字段名',
    'UNDEFINED_DATA_TYPE': '未定义的数据类型',
    'UNSUPPORTED_DATA_TYPE': '不支持的类型 `{type}`\n支持的类型 [{supported}]',
    'PARSE_RULE_EXCEPTION': '非法的规则',
    'CONVERT_DATA_EXCEPTION': '非法的数据 类型:`{type}` `{data}`',
    # rule.py
    'KEY_RULE_PARSE_ERROR': '在 行{row_num}:列{col_num} 已经定义',
    'MACRO_RULE_NOT_EXIST': '不存在',
    'MACRO_RULE_DUPLICATE_DEFINITION': '在 行{row_num}:列{col_num} 已经定义',
    'UNIQUE_RULE_FAILED': '数据:`{data}` 不唯一，在 行{row_num}:列{col_num} 已经定义',
    'NOT_EMPTY_RULE_FAILED': '数据不能为空',
    'MIN_RULE_FAILED_1': '数据:`{data}` 小于最小限制',
    'MIN_RULE_FAILED_2': '数据:`{data}` 长度:`{len}` 小于最小限制',
    'MAX_RULE_FAILED_1': '数据:`{data}` 超过最大限制',
    'MAX_RULE_FAILED_2': '数据:`{data}` 长度:`{len}` 大于最大限制',
    'SOURCE_RULE_FAILED': '数据:`{data}` 路径不存在',
    'REF_RULE_PARSE_ERROR_1': '配置表:`{table}` 不存在',
    'REF_RULE_PARSE_ERROR_2': '字段:`{field}` 不存在',
    'REF_RULE_FAILED': '数据:`{data}` 引用数据不存在',
    'STRUCT_RULE_FAILED': '行:`{row_num}` {err}',
    'GLOBAL_KEY_RULE_FAILED_1': '主键为空',
    'GLOBAL_KEY_RULE_FAILED_2': '在 行{row_num}:列{col_num} 主键值重复定义',
    'GLOBAL_MACRO_RULE_FAILED_1': '不存在',
    'GLOBAL_MACRO_RULE_FAILED_2': '数据不能是 `str` 类型',
    'GLOBAL_MACRO_RULE_FAILED_3': '非法的宏定义名称',
    'GLOBAL_MACRO_RULE_FAILED_4': '在 行{row_num}:列{col_num} 宏定义名称重复定义',
}


class _Language:

    def __init__(self):
        lang_list = en_US
        lang, _ = locale.getdefaultlocale()
        if lang == 'zh_CN':
            lang_list.update(zh_CN)

        for K, V in lang_list.items():
            setattr(self, K, V)


LANG = _Language()

__all__ = ('LANG',)

import locale

en_US = {
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
    'HRL_DIR': 'specify output directory for where to generate the .hrl.'
}

zh_CN = {
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
    'HRL_DIR': '指定.hrl文件输出目录。'
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

__all__ = 'LANG'

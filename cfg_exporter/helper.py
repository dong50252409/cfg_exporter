import os
from argparse import RawTextHelpFormatter, ArgumentTypeError, ArgumentParser

from cfg_exporter.const import ExportType, ExtensionType, TEMPLATE_EXTENSION


def valid_source(source):
    if os.path.exists(source):
        return source
    else:
        raise ArgumentTypeError(_('the source path does not exists `{source}`').format(source=source))


def valid_export(export):
    if export in ExportType.__members__:
        return ExportType[export]
    else:
        raise ArgumentTypeError(_('the export file type does not exits {export}').format(export=export))


def valid_table(row_num):
    try:
        row_num = int(row_num)
        assert row_num > 0
        return row_num
    except (ValueError, AssertionError):
        raise ArgumentTypeError(_('{row_num} is not a valid line number').format(row_num=row_num))


def valid_lang_template(lang_template):
    if os.path.exists(lang_template):
        return lang_template
    else:
        raise ArgumentTypeError(_('the lang template path does not exists `{lang_template}`')
                                .format(source=lang_template))


parser = ArgumentParser(description=_('Configuration table export toolset'), formatter_class=RawTextHelpFormatter)

base_group = parser.add_argument_group(title=_('Base options'))

base_group.add_argument('--clear_dir', default=False, action='store_true',
                        help=_('clear the output directory.'))

base_group.add_argument('--exclude_files', default=[], nargs="*",
                        help=_('specify a list of file names not to load.'))

base_group.add_argument('-e', '--export_type', type=valid_export,
                        metavar=f'[{",".join(ExportType.__members__.keys())}]',
                        help=_('specify the configuration table export type.'))

base_group.add_argument('--file_prefix', default='',
                        help=_('specify the prefix of the output filename.'))

base_group.add_argument('--force', default=False, action='store_true',
                        help=_('force all configuration tables to be generated.'))

base_group.add_argument('-o', '--output', type=str, default="",
                        help=_('specify the configuration table output path.'))

base_group.add_argument('-r', '--recursive', default=False, action='store_true',
                        help=_('recursively search the source path.'))

base_group.add_argument('--verification', default=False, action='store_true',
                        help=_('verify only the correctness of the configuration table.'))

base_group.add_argument('-s', '--source', type=valid_source, required=True,
                        help=_(
                            'specify the configuration table source path.\nsupported file types [{extensions}]').format(
                            extensions=",".join(ExtensionType.__members__.keys())))

base_group.add_argument('--template_path',
                        help=_('specify the extension template path.\n'
                               'the template name consists of the table name, export type, '
                               'and {template_extension} extension\n'
                               'e.g:\n'
                               '`item.erl.{template_extension}` `item.hrl.{template_extension}` '
                               '`item.lua.{template_extension}`\n'
                               'loads the template based on the specified export type\n'
                               'e.g:\n'
                               '`--export_type erl` templates ending with `.erl.{template_extension}` '
                               'and `.hrl.{template_extension}` will be loaded\n'
                               '`--export_type lua` templates ending with `.lua.{template_extension}` will be loaded'
                               ).format(template_extension=TEMPLATE_EXTENSION))

base_group.add_argument('--verbose', default=False, action='store_true',
                        help=_('show the details.'))

table_group = parser.add_argument_group(title=_('Table options'))

table_group.add_argument('--data_row', type=valid_table, required=True,
                         help=_('specify the start line number of the configuration table body data.'))

table_group.add_argument('--desc_row', type=valid_table,
                         help=_('specify the line number of the configuration table column description.'))

table_group.add_argument('--field_row', type=valid_table, required=True,
                         help=_('specify the line number of the configuration table field name.'))

table_group.add_argument('--rule_row', type=valid_table,
                         help=_('specify the line number of the configuration table check rule.'))

table_group.add_argument('--type_row', type=valid_table, required=True,
                         help=_('specify the line number of the configuration table data type.'))

lang_group = parser.add_argument_group(title=_('Multi languages options'))

lang_group.add_argument('--lang_template', type=valid_lang_template,
                        help=_('specify the language template path.'))

lang_group.add_argument('--export_lang_template',
                        help=_('output language template.'))

csv_group = parser.add_argument_group(title=_('CSV options'))

csv_group.add_argument('--csv_encoding', default='utf-8-sig', metavar='ENCODING',
                       help=_('specify the default encoding format for CSV files.\nDEFAULT UTF-8'))

erl_group = parser.add_argument_group(title=_('Erlang options'))

erl_group.add_argument('--erl_dir', default='',
                       help=_('specify output directory for where to generate the .erl.'))

erl_group.add_argument('--hrl_dir', default='',
                       help=_('specify output directory for where to generate the .hrl.'))

lua_group = parser.add_argument_group(title=_('LUA options'))

lua_group.add_argument('--lua_optimize', default=False, action='store_true',
                       help=_('remove default value fields ( store them into metatable ) '
                              'and reuse all table values to save memory'))

py_group = parser.add_argument_group(title=_('PYTHON options'))

py_group.add_argument('--py_optimize', default=False, action='store_true',
                      help=_('remove default value fields and reuse all table values to save memory'))

args = parser.parse_args()

__all__ = ('args',)

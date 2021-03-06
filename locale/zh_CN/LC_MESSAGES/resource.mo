??    A      $              ,     -     :  "   F     i     x  (   ?     ?  D   ?       D   '  ;   l  >   ?     ?  &     ,   +  /   X      ?     ?     ?     ?  9   ?          /  /   N     ~     ?     ?     ?     ?  *   ?       +   &  #   R     v     ?     ?     ?  )   ?  8   ?  8   )	  ,   b	  ,   ?	  P   ?	  @   
  ?  N
  >   ;  F   z  =   ?  >   ?  *   >  &   i  C   ?  3   ?               7     I  ,   d  *   ?     ?  &   ?  7   ?  Z   )  $   ?  9  ?     ?  
   ?     ?          !  *   1     \  9   r  	   ?  F   ?  1   ?  1   /     a  %   ?  "   ?  "   ?  *   ?  	        "     >  1   T     ?     ?     ?     ?     ?     ?          '     C     \  3   i  !   ?     ?     ?     ?       '        ?     _          ?  C   ?  1     ?  3     ?       $   5  !   Z     |  !   ?  $   ?  6   ?          -     K     ^  $   w     ?     ?  (   ?  '   ?  S        l   Base options CSV options Configuration table export toolset Erlang options Table options already defined at r{row_num}:c{col_num} clear the output directory. data type `{type}` is unsupported
supported data types [{supported}] data type is not `str` data:`{data}` is not unique already defined at r{row_num}:c{col_num} data:`{data}` length:`{len}` the maximum limit was exceeded data:`{data}` length:`{len}` the minimum limit was not reached data:`{data}` path not found data:`{data}` reference does not exist data:`{data}` the maximum limit was exceeded data:`{data}` the minimum limit was not reached defined at r{row_num}:c{col_num} does not exist down! elapsed {:.3f}/s export {filename} ... export {filename} finished! elapsed_time:{elapsed_time}/s field:`{field}` field:`{field}` does not exist force all configuration tables to be generated. index:`{row_num}` {err} invalid field name invalid macro name is invalid rule loading table {table} ... macro name repeat at r{row_num}:c{col_num} primary key is empty primary key repeat at r{row_num}:c{col_num} recursively search the source path. reference table `{table}` rule:`{rule}` r{row_num}:c{col_num} show the details. specify a list of file names not to load. specify output directory for where to generate the .erl. specify output directory for where to generate the .hrl. specify the configuration table export type. specify the configuration table output path. specify the configuration table source path.
supported file types [{extensions}] specify the default encoding format for CSV files.
DEFAULT UTF-8 specify the extension template path.
the template name consists of the table name, export type, and {template_extension} extension
e.g:
`item.erl.{template_extension}` `item.hrl.{template_extension}` `item.lua.{template_extension}`
loads the template based on the specified export type
e.g:
`--export_type erl` templates ending with `.erl.{template_extension}` and `.hrl.{template_extension}` will be loaded
`--export_type lua` templates ending with `.lua.{template_extension}` will be loaded specify the line number of the configuration table check rule. specify the line number of the configuration table column description. specify the line number of the configuration table data type. specify the line number of the configuration table field name. specify the prefix of the output filename. specify the prefix of the record name. specify the start line number of the configuration table body data. table {table} loaded! elapsed time:{elapsed_time}/s table:`{table}` table:`{table}` does not exist the data is empty the data type is undefined the export file type does not exits {export} the source path does not exists `{source}` type:`{type}` type:`{type}` `{data}` is invalid data verify only the correctness of the configuration table. waring! the {new_filename} table has been loaded the {old_filename} table will be replaced {row_num} is not a valid line number Project-Id-Version: PACKAGE VERSION
POT-Creation-Date: 2022-01-20 21:24+0800
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: DY <304887750@QQ.COM>
Language-Team: LANGUAGE <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
 基础选项 CSV 选项 配置表导出工具集 Erlang选项 配置表选项 在 行{row_num}:列{col_num} 已经定义 清空输出目录。 不支持的类型 `{type}`
支持的类型 [{supported}] 不存在 数据:`{data}` 不唯一，在 行{row_num}:列{col_num} 已经定义 数据:`{data}` 长度:`{len}` 大于最大限制 数据:`{data}` 长度:`{len}` 小于最小限制 数据:`{data}` 路径不存在 数据:`{data}` 引用数据不存在 数据:`{data}` 超过最大限制 数据:`{data}` 小于最小限制 在 行{row_num}:列{col_num} 已经定义 不存在 完成! 耗时：{:.3f}/秒 导出 {filename} ... {filename}已导出！耗时：{elapsed_time}/秒 字段:`{field}` 字段:`{field}` 不存在 强制生成所有配置表。 行:`{row_num}` {err} 非法的字段名 数据不能是 `str` 类型 非法的规则 载入配置表 {table} ... 非法的宏定义名称 主键为空 在 行{row_num}:列{col_num} 主键值重复定义 搜索子文件夹下的内容。 配置表:`{table}` 不存在 规则:`{rule}` 行{row_num}:列{col_num} 显示详情。 指定排除加载的文件名列表。 指定.erl文件输出目录。 指定.hrl文件输出目录。 指定配置表导出类型。 指定配置表输出路径。 指定配置表源路径
支持的配置表类型 [{extensions}]。 指定读取CSV文件编码格式。
默认 UTF-8 指定扩展模板路径。
模板名由表名、导出文件类型以及{template_extension}扩展名组成
例如：
`item.erl.{template_extension}` `item.hrl.{template_extension}` `item.lua.{template_extension}`
根据指定导出类型加载模板
例如：
`--export_type erl` 以 `.erl.{template_extension}`和`.hrl.{template_extension}` 结尾的模板将被载入
`--export_type lua` 以 `.lua.{template_extension}` 结尾的模板将被载入 指定配置表规则行号。 指定配置表描述行号。 指定配置表数据类型行号。 指定配置表字段名行号。 指定导出文件名前缀。 指定record字段名前缀名。 指定配置表数据起始行号。 配置表 {table} 已载入! 耗时：{elapsed_time}/s 配置表:`{table}` 配置表:`{table}` 不存在 数据不能为空 未定义的数据类型 {export} 导出文件类型不存在 `{source}` 路径不存在 类型:`{type}` 非法的数据 类型:`{type}` `{data}` 仅验证配置表数据是否正确。 警告！表 {new_filename} 已经载入，旧配置表 {old_filename} 将被替换 {row_num} 不是有效的行号 
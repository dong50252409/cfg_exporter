# cfg_exporter

配置表导出工具

## 安装依赖

    pip install -r requirements.txt

## 打印帮助

    python -m cfg_exporter -h

## 特性

* 支持规则检查
* 枚举生成
* 可支持多种数据结构导入
    * `csv`
    * `excel`
    * `memory`
    * 扩展：继承`Table`类，实现`load_table`方法，参考`csv_table.py` `memory_table.py` `xlsx_table.py`
* 可支持多种数据结构导出
    * `csv`
    * `xlsx`
    * `json`
    * `erlang`
    * `lua` 可以生成深度优化的配表文件
    * `python` 可以生成深度优化的配表文件
    * 通过模板支持自定义格式
    * ....

## 命名规范

* 命名规则 `^[a-zA-Z]([a-zA-Z0-9]|_)*` 包括字段名、常量名

## 数据类型

* `int` 整数
* `float` 浮点数
* `str` UTF-8字符串
* `lang` UTF-8多语言文本
* `iter` 可迭代结构
    * `[]` 表示列表结构
    * `()` 表示元祖
* `raw` 原始类型，内容将原样输出。
  * **此数据类型无法应用规则检查**
  * **在强类型语言中以UTF-8字符串形式输出**
* [数据类型细分](#数据类型细分)

## 数据类型细分

  在数据类型定义后通过`:`分隔，描述配表生成时使用的具体类型

* `c#` 
  * 整数、浮点数
    * `int:byte` 8 位无符号整数
    * `int:sbyte` 8 位有符号整数类型
    * `int:short` 16 位有符号整数类型
    * `int:ushort` 16 位无符号整数类型
    * `int`或`int:int` 32 位有符号整数类型
    * `int:uint` 32 位无符号整数类型
    * `int:long` 64 位有符号整数类型
    * `int:ulong` 64 位无符号整数类型
    * `float`或`float:float` 32 位单精度浮点型
    * `float:double` 64 位双精度浮点型
  * 可迭代结构（仅用作演示，实际可以随便组合）
    * `iter:List<int>` 表示元素为32位有符号整数类型的列表
    * `iter:Tuple<int, int>` 表示双元素为32位有符号整数类型的元祖
    * `iter:List<Tuple<int, int>>` 表示元素为双32位有符号整数类型的元祖的列表

## 规则

规则之间可以 通过`|`分隔每个规则

* 示例

        主键列、常量的取值列
        key:1 | const:value
        
        唯一 非空 范围100-1000 值引用于item.id列
        unique | not_empty | min:100 | max:1000 | ref:item.id  

* 唯一规则

  全表不可重复指定的规则

  | 规则名称 | 描述 | 参数类型 | 示例 |
  | :----: | ---- | :----: | ---- |
  | `key:number` | 标记当前列为主键列，**有多个主键列可多次标记**<br/>主键列不可为空，联合主键不可重复，编号从1开始 | `int` | `key:1` 当前列为主键，编号为1 |
  | `const:type` | 标记当前列作为常量的一部分，并在导出配表时导出 | `str` | `type:name` 当前列为常量名<br/>`type:value` 当前列为常量值（可选，默认从1开始）<br/>`type:desc` 当前列为常量述（可选，默认为空） |

* 普通规则

  可重复指定的规则

  | 规则名称 | 描述 | 参数类型 | 示例 | 
  | :----: | ---- | :----: | ---- |
  | `unique` | 检查当前列**非空值**是否全列唯一<br/>如果指定在`struct`规则中则检查当前单元格的值是否全结构唯一 | | `unique` |
  | `not_empty` | 检查当前列的**值**是否无空值 | | `not_empty` |
  | `default:any` | 如果当前列的**值**为空，则赋予缺省值 | `any` | `default:0` `default:文案整理中` `default:[]` |
  | `size:min[~max]` | 检查当前列**非空值**的取值或长度范围<br/>`int` `float`类型的值，检查其大小 <br/>`str` `iter` 类型的值，检查其长度 | `int` | `size:1~99` 数值或长度1 - 99<br/>`size:1~` 数值或长度1 - +∞<br/>`size:~99` 数值或长度 -∞ - 99<br/>`size:99` 数值或长度恒等于99 |
  | `source:path` | 检查当前列**非空值**引用资源是否存在 | `str` | 要检查资源目录的相对或绝对路径<br/>`source:source/ui`<br/>`source:D:/project/source/ui` |
  | `ref:table_name.field_name` | 检查当前列**非空值**是否在`table_name`表`field_name`列中存在 | `str` | `ref:item.id` 当前的列值引用于`item`表的`id`列的值 |
  | `struct:rules` | 对`iter`类型结构中的各项值进行规则检查<br/>仅支持指定普通规则 | `iter` | 示例1<br/>`[(1,100,"描述1"),(2,200,"描述2")]`<br/>`struct:[(unique｜ref:item.id,min:0｜max:10000,_)]`<br/>对 `1` `2`进行`unique` `ref`规则检查<br/>对`100` `200`进行`min` `max`规则检查<br/>`_`表示占位符<br/><br/>示例2<br/>`["abc",[1,2,3],(4,5,6)]`<br/>`struct:[max:10]`<br/>对`"abc"` `[1,2,3]` `(4,5,6)` 进行长度检查 |
  | `_` | 无特殊意义，仅用作占位，配合`struct`规则使用 | | |

## 多语言文本

  工具支持通过多语言模板在导出配表时动态替换输出内容
  
  具体格式请参考[模板](example/lang_template/lang_template.csv)
1. 将配置表中需要翻译的字段类型标记为`lang`
2. 通过`--export_lang_template`命令行参数导出语言模板
   * 收集所有配表中`lang`类型的字段列
   * 将其整理到一个文件中
3. 导出配表时通过`--lang_template`命令行参数指定多语言模板文件

## 意见和建议

  有任何意见或建议随时欢迎联系我，或提交pr
# cfg_exporter
配置表导出工具

安装依赖
------
    pip install -r requirements.txt

打印帮助
------
    python -m cfg_exporter -h

特性
----
* 支持规则检查
* 枚举生成
* 可支持多种数据结构导入
    * `csv`
    * `excel`
* 可支持多种数据结构导出
    * `protobuf` 待实现
    * `json` 待实现
    * `erl` 
    * `lua` 待实现
    * 通过模板支持自定义格式
    * ....

数据类型
----
* `int` 整形
* `float` 浮点型
* `str` 字符串
* `iter` 可迭代结构
    * `[]` 表示列表结构
    * `()` 表示元祖

规则
---
规则之间可以 通过`|`分隔每个规则

* 示例

        主键列、宏的取值列
        key:1 | macro:value
        
        值引用于item.id、范围100-1000、唯一、非空
        ref:item.id | range:100-1000 | unique | not_empty

* 唯一规则

    全表不可重复指定的规则
    
    | 规则名称 | 描述 | 参数类型 | 示例 |
    | ------- | ----|  ------ | --- |
    | `key:number` | 标记当前列为主键列，有多个主键列可多次标记<br/>主键列不可为空，联合主键不可重复，编号从1开始 | `int` | `key:1` 当前列为主键，编号为1 |
    | `macro:type` | 标记当前列作为宏的一部分                                     | `str` | `type:name` 当前列为宏名称<br/>`type:value` 当前列为宏值<br/>`type:desc` 当前列为宏描述（可选） |
    
* 普通规则

  可重复指定的规则

  | 规则名称                      | 描述                                                      | 参数类型 | 示例                                                                                         |
  | --------------------------- | --------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------- |
  | `ref:table_name.field_name` | 检查当前列的值是否在`table_name` 表 `field_name` 列中存在       | `str`    | `ref:item.id` 当前列值引用自`item`表的`id`列数据                                               |
  | `len:number`                | 限定字符串、列表、元祖等可迭代结构最大长度。支持检查str、iter等类型   | `int`    | `len:100` 最大长度为`100`                                                                   |
  | `range:min-max`             | 检查值的范围，包含上下边界。支持检查int、float、str、iter等类型     | `int`    | `range:0-100` 限定取值范围在`0-100`之间                                                      |
  | `source:path`               | 检查引用资源是否存在                                          | `str`    | 要检查资源目录的路径<br/>绝对路径`source:D:/project/source/ui`<br/>相对路径 `source:source/ui`   |
  | `unique`                    | 检查当前列值是否全列唯一                                       |          | `unique`                                                                                  |
  | `not_empty`                 | 检查当前列是否无空值                                          |          | `not_empty`                                                                               |
  | `struct:rules`              | 对结构中的各项值进行规则检查，仅支持指定普通规则                    | `iter`   | 示例1<br/>`[(1,100,"描述1"),(2,200,"描述2")]`<br/><br/>`struct:[(ref:item.id｜unique, range:0-10000, _)]`<br/>对 `1、2`进行`ref`、`unique`规则检查<br/>对`100、200`进行`range`规则检查<br/>`_`表示占位符<br/><br/>示例2<br/>`["abc",[1,2,3],(4,5,6)]`<br/>`struct:[len:10]`<br/>对`"abc"、[1,2,3]、(4,5,6)` 进行`len`规则检查 |

- 支持右键菜单导出（windows）



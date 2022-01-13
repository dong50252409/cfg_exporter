-------------------------------------
--  AUTO GENERATE BY CFG_EXPORTER  --
-------------------------------------
--- @class cfg_real_time_value
--- @field auto_macro_key @ key
--- @field value 
--- @field export @ 1：仅前端读2：仅后端读
--- @field desc 

local tab = {}

tab.macro = {
    --- @field ERLANG_ATOM @ Erlang数据类型
    ERLANG_ATOM = 1,
    --- @field ERLANG_TERM @ Erlang数据类型
    ERLANG_TERM = 2,
    --- @field TUPLE_OR_TABLE @ Erlang元祖或LuaTable
    TUPLE_OR_TABLE = 3,
    --- @field INTEGER @ 数值
    INTEGER = 4,
    --- @field DESC_1 @ 单行描述
    DESC_1 = 5,
    --- @field DESC_2 @ 多行描述
    DESC_2 = 6,
}

tab.data_list = {
    [3] = {180,1},
    [4] = 604800,
    [5] = "积分越高，每个官职可领取的奖励越多",
    [6] = "[cefffe]元素适性会影响英雄的基础属性，\n不同英雄最适合的元素不同，其中[ffd967]S级[-]\n为原属性120%，[f69df3]A级[-]为100%，[80caed]B级[-]\n为85%，[8fe6a3]C级[-]为70%",
}

return tab

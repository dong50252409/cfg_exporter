-------------------------------------
--  AUTO GENERATE BY CFG_EXPORTER  --
-------------------------------------
local cfg_real_time_value = {}

cfg_real_time_value.field_list = {
    auto_macro_key = 1,                                                         -- key
    value = 2,                                                                  
    export = 3,                                                                 -- 1：仅前端读2：仅后端读
    desc = 4,                                                                   
}

cfg_real_time_value.data_list = {
    [3] = {180,1},
    [4] = 604800,
    [5] = "积分越高，每个官职可领取的奖励越多",
    [6] = "[cefffe]元素适性会影响英雄的基础属性，\n不同英雄最适合的元素不同，其中[ffd967]S级[-]\n为原属性120%，[f69df3]A级[-]为100%，[80caed]B级[-]\n为85%，[8fe6a3]C级[-]为70%",
}

cfg_real_time_value.ERLANG_ATOM = 1                                             -- Erlang数据类型
cfg_real_time_value.ERLANG_TERM = 2                                             -- Erlang数据类型
cfg_real_time_value.TUPLE_OR_TABLE = 3                                          -- Erlang元祖或LuaTable
cfg_real_time_value.INTEGER = 4                                                 -- 数值
cfg_real_time_value.DESC_1 = 5                                                  -- 单行描述
cfg_real_time_value.DESC_2 = 6                                                  -- 多行描述

return cfg_real_time_value

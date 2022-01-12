%%===================================
%%  AUTO GENERATE BY CFG_EXPORTER
%%===================================
-ifndef(CFG_REAL_TIME_VALUE_HRL).
-define(CFG_REAL_TIME_VALUE_HRL, true).

-record(cfg_real_time_value, {
    auto_macro_key,                                                             % key
    value,                                                                      
    export,                                                                     % 1：仅前端读2：仅后端读
    desc                                                                        
}).

-define(ERLANG_ATOM, 1).                                                        % Erlang数据类型
-define(ERLANG_TERM, 2).                                                        % Erlang数据类型
-define(TUPLE_OR_TABLE, 3).                                                     % Erlang元祖或LuaTable
-define(INTEGER, 4).                                                            % 数值
-define(DESC_1, 5).                                                             % 单行描述
-define(DESC_2, 6).                                                             % 多行描述

-endif.

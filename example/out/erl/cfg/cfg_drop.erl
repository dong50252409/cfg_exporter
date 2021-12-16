%%===================================
%%  AUTO GENERATE BY CFG_EXPORTER
%%===================================
-module(cfg_drop).
-compile([export_all, nowarn_export_all]).
-include("cfg_drop.hrl").

get(1) ->
    #cfg_drop{
        id = 1,
        desc = <<"掉落1"/utf8>>,
        times = 1,
        drop_take = [{1, 10, 100}, {2, 10, 200}]
    };
get(2) ->
    #cfg_drop{
        id = 2,
        desc = <<"掉落2"/utf8>>,
        times = 2,
        drop_take = [{1, 10, 100}, {2, 10, 200}, {3, 10, 200}]
    };
get(3) ->
    #cfg_drop{
        id = 3,
        desc = <<"掉落3"/utf8>>,
        times = 3,
        drop_take = [{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}]
    };
get(4) ->
    #cfg_drop{
        id = 4,
        desc = <<"掉落4"/utf8>>,
        times = 4,
        drop_take = [{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}]
    };
get(5) ->
    #cfg_drop{
        id = 5,
        desc = <<"掉落5"/utf8>>,
        times = 5,
        drop_take = [{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}, {6, 10, 200}]
    };
get(6) ->
    #cfg_drop{
        id = 6,
        desc = <<"掉落6"/utf8>>,
        times = 1,
        drop_take = [{101, 1, 100}, {102, 1, 200}, {103, 1, 200}]
    };
get(7) ->
    #cfg_drop{
        id = 7,
        desc = <<"掉落7"/utf8>>,
        times = 1,
        drop_take = [{201, 1, 100}, {202, 1, 200}]
    };
get(8) ->
    #cfg_drop{
        id = 8,
        desc = <<"掉落8"/utf8>>,
        times = 1,
        drop_take = [{203, 1, 100}, {204, 1, 200}]
    };
get(_) ->
    undefined.

list() ->
    [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8
    ].


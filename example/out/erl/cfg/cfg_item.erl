%%===================================
%%  AUTO GENERATE BY CFG_EXPORTER
%%===================================
-module(cfg_item).
-compile([export_all, nowarn_export_all]).
-include("cfg_item.hrl").

get(1) ->
    #cfg_item{
        id = 1,
        name = <<"钻石"/utf8>>,
        macro_name = <<"ITEM_DIAMOND"/utf8>>,
        description = <<"充值货币，可以通过充值、活动获得"/utf8>>,
        item_type = 1,
        item_sub_type = 1,
        price = [],
        quality_type = 5,
        args = true
    };
get(2) ->
    #cfg_item{
        id = 2,
        name = <<"金币"/utf8>>,
        macro_name = <<"ITEM_GOLD"/utf8>>,
        description = <<"常规货币"/utf8>>,
        item_type = 1,
        item_sub_type = 2,
        price = [],
        quality_type = 3,
        args = [{a,b}]
    };
get(3) ->
    #cfg_item{
        id = 3,
        name = <<"水晶"/utf8>>,
        macro_name = <<"RES_CRYSTAL"/utf8>>,
        description = <<"基础资源"/utf8>>,
        item_type = 2,
        item_sub_type = 1,
        price = [],
        quality_type = 1,
        args = undefined
    };
get(4) ->
    #cfg_item{
        id = 4,
        name = <<"金属"/utf8>>,
        macro_name = <<"RES_METAL"/utf8>>,
        description = <<"基础资源"/utf8>>,
        item_type = 2,
        item_sub_type = 2,
        price = [],
        quality_type = 1,
        args = undefined
    };
get(5) ->
    #cfg_item{
        id = 5,
        name = <<"石油"/utf8>>,
        macro_name = <<"RES_OIL"/utf8>>,
        description = <<"基础资源"/utf8>>,
        item_type = 2,
        item_sub_type = 3,
        price = [],
        quality_type = 1,
        args = undefined
    };
get(6) ->
    #cfg_item{
        id = 6,
        name = <<"粮食"/utf8>>,
        macro_name = <<"RES_FOOD"/utf8>>,
        description = <<"基础资源"/utf8>>,
        item_type = 2,
        item_sub_type = 4,
        price = [],
        quality_type = 1,
        args = undefined
    };
get(101) ->
    #cfg_item{
        id = 101,
        name = <<"传说召唤券"/utf8>>,
        macro_name = undefined,
        description = <<"可以在“传说英雄”卡池中免费进行一次召唤"/utf8>>,
        item_type = 8,
        item_sub_type = 1,
        price = [{1, 10}],
        quality_type = 5,
        args = undefined
    };
get(102) ->
    #cfg_item{
        id = 102,
        name = <<"霸业召唤券"/utf8>>,
        macro_name = undefined,
        description = <<"可以在霸业卡池“征服之军”、“整装待发”、“秩序重构”、“星战将起”、“战争号角”、“星球主宰”中免费进行一次召唤"/utf8>>,
        item_type = 8,
        item_sub_type = 2,
        price = [{2, 100}],
        quality_type = 3,
        args = undefined
    };
get(103) ->
    #cfg_item{
        id = 103,
        name = <<"传说英雄卡"/utf8>>,
        macro_name = undefined,
        description = <<"随机获得一个传说英雄"/utf8>>,
        item_type = 7,
        item_sub_type = 1,
        price = [{3, 100}, {4, 100}, {5, 100}, {6, 100}],
        quality_type = 4,
        args = undefined
    };
get(201) ->
    #cfg_item{
        id = 201,
        name = <<"人族传说卡"/utf8>>,
        macro_name = undefined,
        description = <<"随机获得一个人族的传说英雄"/utf8>>,
        item_type = 7,
        item_sub_type = 2,
        price = [{3, 500}],
        quality_type = 5,
        args = undefined
    };
get(202) ->
    #cfg_item{
        id = 202,
        name = <<"兽族传说卡"/utf8>>,
        macro_name = undefined,
        description = <<"随机获得一个兽族的传说英雄"/utf8>>,
        item_type = 7,
        item_sub_type = 3,
        price = [{4, 500}],
        quality_type = 5,
        args = undefined
    };
get(203) ->
    #cfg_item{
        id = 203,
        name = <<"机械传说卡"/utf8>>,
        macro_name = undefined,
        description = <<"随机获得一个机械族的传说英雄"/utf8>>,
        item_type = 7,
        item_sub_type = 4,
        price = [{5, 500}],
        quality_type = 5,
        args = undefined
    };
get(204) ->
    #cfg_item{
        id = 204,
        name = <<"神族传说卡"/utf8>>,
        macro_name = undefined,
        description = <<"随机获得一个神族的传说英雄"/utf8>>,
        item_type = 7,
        item_sub_type = 5,
        price = [{6, 500}],
        quality_type = 5,
        args = undefined
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
        101,
        102,
        103,
        201,
        202,
        203,
        204
    ].

get_by_type(1) ->
    [1, 2];
get_by_type(2) ->
    [3, 4, 5, 6];
get_by_type(8) ->
    [101, 102];
get_by_type(7) ->
    [103, 201, 202, 203, 204];
get_by_type(_) ->
    [].

get_by_sub_type(1, 1) ->
    [1];
get_by_sub_type(1, 2) ->
    [2];
get_by_sub_type(2, 1) ->
    [3];
get_by_sub_type(2, 2) ->
    [4];
get_by_sub_type(2, 3) ->
    [5];
get_by_sub_type(2, 4) ->
    [6];
get_by_sub_type(8, 1) ->
    [101];
get_by_sub_type(8, 2) ->
    [102];
get_by_sub_type(7, 1) ->
    [103];
get_by_sub_type(7, 2) ->
    [201];
get_by_sub_type(7, 3) ->
    [202];
get_by_sub_type(7, 4) ->
    [203];
get_by_sub_type(7, 5) ->
    [204];
get_by_sub_type(_, _) ->
    [].


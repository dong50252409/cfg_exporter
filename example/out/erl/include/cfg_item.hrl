%%===================================
%%  AUTO GENERATE BY CFG_EXPORTER
%%===================================
-ifndef(CFG_ITEM_HRL).
-define(CFG_ITEM_HRL, true).

-record(cfg_item, {
    id,                                                                         % 道具id
    name,                                                                       % 道具名称
    macro_name,                                                                 % 宏定义
    description,                                                                % 道具描述
    item_type,                                                                  % 道具类型
    item_sub_type,                                                              % 道具子类型
    price,                                                                      % 出售价格 配置格式：[(道具id,数量),...]
    quality_type,                                                               % 道具品质
    args                                                                        % 自定义数据
}).

-define(ITEM_DIAMOND, 1).                                                       % 钻石
-define(ITEM_GOLD, 2).                                                          % 金币
-define(RES_CRYSTAL, 3).                                                        % 水晶
-define(RES_METAL, 4).                                                          % 金属
-define(RES_OIL, 5).                                                            % 石油
-define(RES_FOOD, 6).                                                           % 粮食

-endif.

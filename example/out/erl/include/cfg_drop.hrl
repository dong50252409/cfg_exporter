%%===================================
%%  AUTO GENERATE BY CFG_EXPORTER
%%===================================
-ifndef(CFG_DROP_HRL).
-define(CFG_DROP_HRL, true).
-record(cfg_drop, {
    id,
    world_level,    % 世界等级
    desc,    % 描述
    times,    % 随机次数
    drop_take    % 抽取掉落列表[(物品tid，数量，权重)]
}).
-endif.

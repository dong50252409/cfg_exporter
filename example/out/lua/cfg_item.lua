-------------------------------------
--  AUTO GENERATE BY CFG_EXPORTER  --
-------------------------------------
--- @class cfg_item
--- @field id @ 道具id
--- @field name @ 道具名称
--- @field macro_name @ 宏定义
--- @field description @ 道具描述
--- @field item_type @ 道具类型
--- @field item_sub_type @ 道具子类型
--- @field price @ 出售价格 配置格式：[(道具id,数量),...]
--- @field quality_type @ 道具品质
--- @field args @ 自定义数据

local tab = {}

tab.macro = {
    --- @field ITEM_DIAMOND @ 钻石
    ITEM_DIAMOND = 1,
    --- @field ITEM_GOLD @ 金币
    ITEM_GOLD = 2,
    --- @field RES_CRYSTAL @ 水晶
    RES_CRYSTAL = 3,
    --- @field RES_METAL @ 金属
    RES_METAL = 4,
    --- @field RES_OIL @ 石油
    RES_OIL = 5,
    --- @field RES_FOOD @ 粮食
    RES_FOOD = 6,
}

--- @type table<number | string, cfg_item>
tab.data_list = {
    [1] = {
        id = 1,
        name = "钻石",
        macro_name = "ITEM_DIAMOND",
        description = "充值货币，可以通过充值、活动获得",
        item_type = 1,
        item_sub_type = 1,
        price = {},
        quality_type = 5,
        args = true
    },
    [2] = {
        id = 2,
        name = "金币",
        macro_name = "ITEM_GOLD",
        description = "常规货币",
        item_type = 1,
        item_sub_type = 2,
        price = {},
        quality_type = 3,
        args = {a,b}
    },
    [3] = {
        id = 3,
        name = "水晶",
        macro_name = "RES_CRYSTAL",
        description = "基础资源",
        item_type = 2,
        item_sub_type = 1,
        price = {},
        quality_type = 1,
        args = nil
    },
    [4] = {
        id = 4,
        name = "金属",
        macro_name = "RES_METAL",
        description = "基础资源",
        item_type = 2,
        item_sub_type = 2,
        price = {},
        quality_type = 1,
        args = nil
    },
    [5] = {
        id = 5,
        name = "石油",
        macro_name = "RES_OIL",
        description = "基础资源",
        item_type = 2,
        item_sub_type = 3,
        price = {},
        quality_type = 1,
        args = nil
    },
    [6] = {
        id = 6,
        name = "粮食",
        macro_name = "RES_FOOD",
        description = "基础资源",
        item_type = 2,
        item_sub_type = 4,
        price = {},
        quality_type = 1,
        args = nil
    },
    [101] = {
        id = 101,
        name = "传说召唤券",
        macro_name = "",
        description = "可以在“传说英雄”卡池中免费进行一次召唤",
        item_type = 8,
        item_sub_type = 1,
        price = {{1, 10}},
        quality_type = 5,
        args = nil
    },
    [102] = {
        id = 102,
        name = "霸业召唤券",
        macro_name = "",
        description = "可以在霸业卡池“征服之军”、“整装待发”、“秩序重构”、“星战将起”、“战争号角”、“星球主宰”中免费进行一次召唤",
        item_type = 8,
        item_sub_type = 2,
        price = {{2, 100}},
        quality_type = 3,
        args = nil
    },
    [103] = {
        id = 103,
        name = "传说英雄卡",
        macro_name = "",
        description = "随机获得一个传说英雄",
        item_type = 7,
        item_sub_type = 1,
        price = {{3, 100}, {4, 100}, {5, 100}, {6, 100}},
        quality_type = 4,
        args = nil
    },
    [201] = {
        id = 201,
        name = "人族传说卡",
        macro_name = "",
        description = "随机获得一个人族的传说英雄",
        item_type = 7,
        item_sub_type = 2,
        price = {{3, 500}},
        quality_type = 5,
        args = nil
    },
    [202] = {
        id = 202,
        name = "兽族传说卡",
        macro_name = "",
        description = "随机获得一个兽族的传说英雄",
        item_type = 7,
        item_sub_type = 3,
        price = {{4, 500}},
        quality_type = 5,
        args = nil
    },
    [203] = {
        id = 203,
        name = "机械传说卡",
        macro_name = "",
        description = "随机获得一个机械族的传说英雄",
        item_type = 7,
        item_sub_type = 4,
        price = {{5, 500}},
        quality_type = 5,
        args = nil
    },
    [204] = {
        id = 204,
        name = "神族传说卡",
        macro_name = "",
        description = "随机获得一个神族的传说英雄",
        item_type = 7,
        item_sub_type = 5,
        price = {{6, 500}},
        quality_type = 5,
        args = nil
    },
}

return tab

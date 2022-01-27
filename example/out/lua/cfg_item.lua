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

--- @field ITEM_DIAMOND @ 钻石
tab.ITEM_DIAMOND = 1
--- @field ITEM_GOLD @ 金币
tab.ITEM_GOLD = 2
--- @field RES_CRYSTAL @ 水晶
tab.RES_CRYSTAL = 3
--- @field RES_METAL @ 金属
tab.RES_METAL = 4
--- @field RES_OIL @ 石油
tab.RES_OIL = 5
--- @field RES_FOOD @ 粮食
tab.RES_FOOD = 6


local config = {
    [1] = {id = 1, name = "钻石", macro_name = "ITEM_DIAMOND", description = "充值货币，可以通过充值、活动获得", item_type = 1, item_sub_type = 1, price = {}, quality_type = 5, args = true},
    [2] = {id = 2, name = "金币", macro_name = "ITEM_GOLD", description = "常规货币", item_type = 1, item_sub_type = 2, price = {}, quality_type = 3, args = {a,b}},
    [3] = {id = 3, name = "水晶", macro_name = "RES_CRYSTAL", description = "基础资源", item_type = 2, item_sub_type = 1, price = {}, quality_type = 1, args = nil},
    [4] = {id = 4, name = "金属", macro_name = "RES_METAL", description = "基础资源", item_type = 2, item_sub_type = 2, price = {}, quality_type = 1, args = nil},
    [5] = {id = 5, name = "石油", macro_name = "RES_OIL", description = "基础资源", item_type = 2, item_sub_type = 3, price = {}, quality_type = 1, args = nil},
    [6] = {id = 6, name = "粮食", macro_name = "RES_FOOD", description = "基础资源", item_type = 2, item_sub_type = 4, price = {}, quality_type = 1, args = nil},
    [101] = {id = 101, name = "传说召唤券", macro_name = nil, description = "可以在“传说英雄”卡池中免费进行一次召唤", item_type = 8, item_sub_type = 1, price = {{1, 10}}, quality_type = 5, args = nil},
    [102] = {id = 102, name = "霸业召唤券", macro_name = nil, description = "可以在霸业卡池“征服之军”、“整装待发”、“秩序重构”、“星战将起”、“战争号角”、“星球主宰”中免费进行一次召唤", item_type = 8, item_sub_type = 2, price = {{2, 100}}, quality_type = 3, args = nil},
    [103] = {id = 103, name = "传说英雄卡", macro_name = nil, description = "随机获得一个传说英雄", item_type = 7, item_sub_type = 1, price = {{3, 100}, {4, 100}, {5, 100}, {6, 100}}, quality_type = 4, args = nil},
    [201] = {id = 201, name = "人族传说卡", macro_name = nil, description = "随机获得一个人族的传说英雄", item_type = 7, item_sub_type = 2, price = {{3, 500}}, quality_type = 5, args = nil},
    [202] = {id = 202, name = "兽族传说卡", macro_name = nil, description = "随机获得一个兽族的传说英雄", item_type = 7, item_sub_type = 3, price = {{4, 500}}, quality_type = 5, args = nil},
    [203] = {id = 203, name = "机械传说卡", macro_name = nil, description = "随机获得一个机械族的传说英雄", item_type = 7, item_sub_type = 4, price = {{5, 500}}, quality_type = 5, args = nil},
    [204] = {id = 204, name = "神族传说卡", macro_name = nil, description = "随机获得一个神族的传说英雄", item_type = 7, item_sub_type = 5, price = {{6, 500}}, quality_type = 5, args = nil},
}

--- @type fun(id):cfg_item
tab.get = function(id)
    return config[id]
end


local item_type_config = {
    [1] = {1, 2},
    [2] = {3, 4, 5, 6},
    [8] = {101, 102},
    [7] = {103, 201, 202, 203, 204},
}

--- @type fun(item_type):number[]
tab.get_by_type = function(item_type)
    return item_type_config[item_type]
end


local item_type_item_sub_type_config = {
    [1] = {[1] = {1}},
    [1] = {[2] = {2}},
    [2] = {[1] = {3}},
    [2] = {[2] = {4}},
    [2] = {[3] = {5}},
    [2] = {[4] = {6}},
    [8] = {[1] = {101}},
    [8] = {[2] = {102}},
    [7] = {[1] = {103}},
    [7] = {[2] = {201}},
    [7] = {[3] = {202}},
    [7] = {[4] = {203}},
    [7] = {[5] = {204}},
}

--- @type fun(item_type, item_sub_type):number[]
tab.get_by_sub_type = function(item_type, item_sub_type)
    return item_type_item_sub_type_config[item_type][item_sub_type]
end

return tab

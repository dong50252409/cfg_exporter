-------------------------------------
--  AUTO GENERATE BY CFG_EXPORTER  --
-------------------------------------
--- @class cfg_drop
--- @field id 
--- @field world_level @ 世界等级
--- @field desc @ 描述
--- @field times @ 随机次数
--- @field drop_take @ 抽取掉落列表[(物品tid，数量，权重)]

local tab = {}



local config = {
    [1] = {[1] = {id = 1, world_level = 1, desc = "掉落1", times = 1, drop_take = {{1, 10, 100}, {2, 10, 200}}}},
    [2] = {[1] = {id = 2, world_level = 1, desc = "掉落2", times = 2, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}}}},
    [3] = {[1] = {id = 3, world_level = 1, desc = "掉落3", times = 3, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}}}},
    [4] = {[1] = {id = 4, world_level = 1, desc = "掉落4", times = 4, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}}}},
    [5] = {[1] = {id = 5, world_level = 1, desc = "掉落5", times = 5, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}, {6, 10, 200}}}},
    [6] = {[1] = {id = 6, world_level = 1, desc = "掉落6", times = 1, drop_take = {{101, 1, 100}, {102, 1, 200}, {103, 1, 200}}}},
    [7] = {[1] = {id = 7, world_level = 1, desc = "掉落7", times = 1, drop_take = {{201, 1, 100}, {202, 1, 200}}}},
    [8] = {[1] = {id = 8, world_level = 1, desc = "掉落8", times = 1, drop_take = {{203, 1, 100}, {204, 1, 200}}}},
    [1] = {[2] = {id = 1, world_level = 2, desc = "掉落1", times = 1, drop_take = {{1, 10, 100}, {2, 10, 200}}}},
    [2] = {[2] = {id = 2, world_level = 2, desc = "掉落2", times = 2, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}}}},
    [3] = {[2] = {id = 3, world_level = 2, desc = "掉落3", times = 3, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}}}},
    [4] = {[2] = {id = 4, world_level = 2, desc = "掉落4", times = 4, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}}}},
    [5] = {[2] = {id = 5, world_level = 2, desc = "掉落5", times = 5, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}, {6, 10, 200}}}},
    [6] = {[2] = {id = 6, world_level = 2, desc = "掉落6", times = 1, drop_take = {{101, 1, 100}, {102, 1, 200}, {103, 1, 200}}}},
    [7] = {[2] = {id = 7, world_level = 2, desc = "掉落7", times = 1, drop_take = {{201, 1, 100}, {202, 1, 200}}}},
    [8] = {[2] = {id = 8, world_level = 2, desc = "掉落8", times = 1, drop_take = {{203, 1, 100}, {204, 1, 200}}}},
    [1] = {[3] = {id = 1, world_level = 3, desc = "掉落1", times = 1, drop_take = {{1, 10, 100}, {2, 10, 200}}}},
    [2] = {[3] = {id = 2, world_level = 3, desc = "掉落2", times = 2, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}}}},
    [3] = {[3] = {id = 3, world_level = 3, desc = "掉落3", times = 3, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}}}},
    [4] = {[3] = {id = 4, world_level = 3, desc = "掉落4", times = 4, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}}}},
    [5] = {[3] = {id = 5, world_level = 3, desc = "掉落5", times = 5, drop_take = {{1, 10, 100}, {2, 10, 200}, {3, 10, 200}, {4, 10, 200}, {5, 10, 200}, {6, 10, 200}}}},
    [6] = {[3] = {id = 6, world_level = 3, desc = "掉落6", times = 1, drop_take = {{101, 1, 100}, {102, 1, 200}, {103, 1, 200}}}},
    [7] = {[3] = {id = 7, world_level = 3, desc = "掉落7", times = 1, drop_take = {{201, 1, 100}, {202, 1, 200}}}},
    [8] = {[3] = {id = 8, world_level = 3, desc = "掉落8", times = 1, drop_take = {{203, 1, 100}, {204, 1, 200}}}},
}

--- @type fun(id, world_level):cfg_drop
tab.get = function(id, world_level)
    return config[id][world_level]
end

return tab

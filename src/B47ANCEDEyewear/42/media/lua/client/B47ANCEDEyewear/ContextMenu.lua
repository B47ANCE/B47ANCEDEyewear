require 'TimedActions/ISTimedActionQueue'
require 'TimedActions/ISB47ANCEDEyewear'

B47ANCEDEyewear = B47ANCEDEyewear or {}
B47ANCEDEyewear.Menu = B47ANCEDEyewear.Menu or {}

local S = require 'B47ANCEDEyewear/Core'
local Menu = B47ANCEDEyewear.Menu
local NO_MATERIALS = 'ContextMenu_B47ANCEDEyewear_NoMaterials'

local function unwrap(entry)
    local ok, item = pcall(function() return entry.items and entry.items[1] or entry end)
    return ok and item or nil
end

-- Normalize the vanilla ArrayList and Lua tables used by compatibility callers.
local function selectedItems(rawItems)
    local result = {}
    if rawItems and type(rawItems.size) == 'function' and type(rawItems.get) == 'function' then
        local ok, size = pcall(rawItems.size, rawItems)
        if ok then
            for index = 0, (tonumber(size) or 0) - 1 do
                local read, entry = pcall(rawItems.get, rawItems, index)
                if read and entry then result[#result + 1] = entry end
            end
        end
    elseif type(rawItems) == 'table' then
        for _, entry in ipairs(rawItems) do result[#result + 1] = entry end
    end
    return result
end

local function eventPlayer(playerOrIndex)
    local kind = type(playerOrIndex)
    if (kind == 'table' or kind == 'userdata') and type(playerOrIndex.isDead) == 'function' then
        return playerOrIndex
    end
    if type(playerOrIndex) == 'number' and type(getSpecificPlayer) == 'function' then
        return getSpecificPlayer(playerOrIndex)
    end
    return nil
end

local function nameOf(item)
    for _, method in ipairs({ 'getDisplayName', 'getName', 'getFullType' }) do
        if item and type(item[method]) == 'function' then
            local ok, value = pcall(item[method], item)
            if ok and value and tostring(value) ~= '' then return tostring(value) end
        end
    end
    return getText('UI_B47ANCEDEyewear_Headwear')
end

local function inventoryItems(inventory)
    local result = {}
    if not inventory or type(inventory.getItems) ~= 'function' then return result end
    local ok, items = pcall(inventory.getItems, inventory)
    if not ok or not items then return result end
    if type(items.size) == 'function' and type(items.get) == 'function' then
        local read, size = pcall(items.size, items)
        if read then
            for index = 0, (tonumber(size) or 0) - 1 do
                local itemOk, item = pcall(items.get, items, index)
                if itemOk and item then result[#result + 1] = item end
            end
        end
    elseif type(items) == 'table' then
        for _, item in ipairs(items) do result[#result + 1] = item end
    end
    return result
end

local function canTie(player, item)
    if not player or not item or player:isDead() or not S.isTieable(item) or S.isTied(item) then return false end
    if type(player.isEquippedClothing) ~= 'function' or not player:isEquippedClothing(item) then return false end
    if type(item.isBroken) == 'function' and item:isBroken() then return false end
    if type(item.getChanceToFall) ~= 'function' then return false end
    local chance = item:getChanceToFall()
    return type(chance) == 'number' and chance > 0 and chance <= 100
end

local function canUntie(player,item)
    return player and item and not player:isDead() and S.isTied(item)
        and type(player.isEquippedClothing) == 'function' and player:isEquippedClothing(item)
end

local function materials(player)
    local available = {}
    for _, item in ipairs(inventoryItems(player:getInventory())) do
        if S.isMaterial(item) then available[#available + 1] = item end
    end
    return available
end

local function queueTie(player, headwear, material)
    if not S.valid(player, headwear, material, false) then return false end
    ISTimedActionQueue.add(ISB47ANCEDEyewear:new(player, headwear, material, false))
    return true
end

local function queueUntie(player,headwear)
    if not S.valid(player,headwear,nil,true) then return false end
    ISTimedActionQueue.add(ISB47ANCEDEyewear:new(player,headwear,nil,true))
    return true
end

local function existingItemMenu(context, name)
    local option = context:getOptionFromName(name)
    if option and option.subOption ~= nil then return option, context:getSubMenu(option.subOption) end
    return option, nil
end

local function disabledTooltip(text)
    -- ISContextMenu later calls setVisible/addToUIManager on this object.
    -- A plain {description=...} table crashes vanilla's context-menu render.
    if not ISWorldObjectContextMenu or type(ISWorldObjectContextMenu.addToolTip) ~= 'function' then return nil end
    local tooltip=ISWorldObjectContextMenu.addToolTip()
    tooltip.description=text
    return tooltip
end

function Menu.add(playerIndex, context, rawItems)
    if not context then return end
    local player = eventPlayer(playerIndex)
    if not player or player:isDead() then return end
    local headwear
    for _, entry in ipairs(selectedItems(rawItems)) do
        local item = unwrap(entry)
        if canTie(player,item) or canUntie(player,item) then headwear=item; break end
    end
    if not headwear then return end

    local name = nameOf(headwear)
    local itemOption, itemMenu = existingItemMenu(context, name)
    if not itemMenu then
        itemOption = itemOption or context:addOption(name, headwear, nil)
        itemMenu = ISContextMenu:getNew(context)
        context:addSubMenu(itemOption, itemMenu)
    end

    if canUntie(player,headwear) then
        return itemMenu:addOption(getText('ContextMenu_B47ANCEDEyewear_Untie'),player,queueUntie,headwear)
    end
    local tie = itemMenu:addOption(getText('ContextMenu_B47ANCEDEyewear_Tie'), headwear, nil)
    local available = materials(player)
    if #available == 0 then
        tie.notAvailable = true
        tie.toolTip = disabledTooltip(getText(NO_MATERIALS))
        return tie
    end
    local submenu = ISContextMenu:getNew(context)
    itemMenu:addSubMenu(tie, submenu)
    for _, material in ipairs(available) do
        submenu:addOption(nameOf(material), player, queueTie, headwear, material)
    end
    return tie
end

local reported = false
local function safeAdd(...)
    local ok, err = pcall(Menu.add, ...)
    if not ok and not reported then
        reported = true
        print('[B47ANCEDEyewear] Tie context menu failed safely: ' .. tostring(err))
    end
end

if Events and Events.OnFillInventoryObjectContextMenu then
    Events.OnFillInventoryObjectContextMenu.Add(safeAdd)
end

return Menu

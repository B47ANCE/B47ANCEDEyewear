require 'NPCs/BodyLocations'
local R = require 'B47ANCEDEyewear/Retention'
local M = require 'B47ANCEDEyewear/TieMaterials'
local T = {}
T.tapeKey = 'B47ANCEDEyewearRetainerTape'
T.types = { ['B47ANCEDEyewear.MakeshiftRetainer'] = true,
    ['B47ANCEDEyewear.EyewearRetainer'] = true,
    ['B47ANCEDEyewear.UnbreakableRetainer'] = true }
T.unbreakableType = 'B47ANCEDEyewear.UnbreakableRetainer'
T.slot = ItemBodyLocation.get(ResourceLocation.of('b47ancedeyewear:retainer'))
assert(T.slot, 'B47ANCEDEyewear retainer slot was not registered')
BodyLocations.getGroup('Human'):getOrCreateLocation(T.slot)

function T.isItem(item)
    return item ~= nil and T.types[item:getFullType()] == true
end

function T.isUnbreakable(item)
    return item ~= nil and item:getFullType() == T.unbreakableType
end

function T.isCrafted(item)
    return item ~= nil and (item:getFullType()=='B47ANCEDEyewear.MakeshiftRetainer'
        or item:getFullType()=='B47ANCEDEyewear.EyewearRetainer')
end

-- Read only. Missing data grants no bonus; malformed data cannot be overwritten
-- by another paid application. The record travels with this actual native item.
function T.tapeState(item)
    if not T.isCrafted(item) or not item:hasModData() then return nil end
    local data = item:getModData()[T.tapeKey]
    if type(data)~='table' or data.schema~=1 or data.revision~=1 or not M.tapes[data.tape]
        or not M.whole(data.bonus,1,M.tapes[data.tape]*5) then return nil end
    return data
end

function T.resistance(item)
    if not T.isCrafted(item) then return nil end
    local options = R.options()
    local base = item:getFullType()=='B47ANCEDEyewear.MakeshiftRetainer'
        and options.clothResistance or options.leatherResistance
    local tape = T.tapeState(item)
    return math.min(100,base+(tape and tape.bonus or 0)), base
end

function T.canTape(character,item,tape)
    if not character or character:isDead() or not T.isCrafted(item)
        or item:isBroken() or item:getCondition()<=0 or not R.options().wearable
        or not tape or not M.tapes[tape:getFullType()] or not M.usable(tape) then return false end
    local inventory = character:getInventory()
    if not inventory or item==tape or item:getContainer()~=inventory or tape:getContainer()~=inventory
        or not inventory:contains(item) or not inventory:contains(tape)
        or (item:hasModData() and item:getModData()[T.tapeKey]~=nil) then return false end
    local _,base = T.resistance(item)
    return base<100 -- No paid action when the server's native wear setting is already capped.
end

local notificationReported = false
function T.applyTape(character,item,tape)
    if isClient() or not T.canTape(character,item,tape) then return false end
    local container,uses = tape:getContainer(),tape:getCurrentUses()
    local metadata = item:getModData()
    local previous = metadata[T.tapeKey]
    local resistance = item:getConditionLowerChance()
    local function rollback()
        metadata[T.tapeKey]=previous
        item:setConditionLowerChance(resistance)
    end
    local changed,err = pcall(function()
        metadata[T.tapeKey]={schema=1,revision=1,tape=tape:getFullType(),
            bonus=M.contribution(M.tapes[tape:getFullType()],'RetainerTapeResistanceMultiplier')}
        local reinforcedResistance = T.resistance(item)
        item:setConditionLowerChance(reinforcedResistance)
    end)
    if not changed then
        rollback()
        print('[B47ANCEDEyewear] Retainer tape failed: '..tostring(err))
        return false
    end
    local paid,useError = pcall(M.consume,character,tape)
    local consumed = tape:getContainer()~=container or not container:contains(tape) or tape:getCurrentUses()<uses
    if not consumed then
        rollback()
        print('[B47ANCEDEyewear] Retainer tape was not consumed: '..tostring(useError))
        return false
    end
    if not paid then print('[B47ANCEDEyewear] Retainer tape paid; notification failed: '..tostring(useError)) end
    -- Do not undo a paid application because a later notification fails.
    local metadataSent,metadataError = pcall(syncItemModData,character,item)
    local fieldsSent,fieldsError = pcall(syncItemFields,character,item)
    if (not metadataSent or not fieldsSent) and not notificationReported then
        notificationReported=true
        print('[B47ANCEDEyewear] Retainer tape synchronization failed: '..tostring(metadataError or fieldsError))
    end
    return true
end

function T.configure(character)
    if isClient() or not character then return end
    local item = character:getWornItem(T.slot)
    if not T.isItem(item) or T.isUnbreakable(item)
        or item:getContainer() ~= character:getInventory() then return end
    local resistance = T.resistance(item)
    if item:getConditionLowerChance() ~= resistance then item:setConditionLowerChance(resistance) end
end

function T.worn(character)
    if not character or character:isDead() or not R.options().wearable then return nil end
    local item = character:getWornItem(T.slot)
    local inventory = character:getInventory()
    if not T.isItem(item) or item:isBroken() or not inventory
        or item:getContainer() ~= inventory then return nil end
    return item
end

-- One real worn retainer protects one untied pair, in vanilla worn-slot order.
-- This performs no inventory traversal, writes no ModData and never creates items.
function T.target(character, S)
    if not T.worn(character) then return nil end
    local worn, inventory = character:getWornItems(), character:getInventory()
    if not worn then return nil end
    for index = 0, worn:size() - 1 do
        local item = worn:get(index):getItem()
        if S.isGlasses(item) and not S.isMonocle(item) and not item:isBroken()
            and not S.hasActiveTie(character, item) and item:getContainer() == inventory then
            return item
        end
    end
    return nil
end

return T

-- Real native clothing items own tie condition; Lua never invents hit events.
require 'NPCs/BodyLocations'
local R = require 'B47ANCEDEyewear/Retention'
local M = require 'B47ANCEDEyewear/TieMaterials'
local D = { key = 'B47ANCEDEyewearTie', types = {}, slots = {} }
for suffix, name in pairs({Eyes='tieeyes', Face='tieface', Hat='tiehat'}) do
    local slot = ItemBodyLocation.get(ResourceLocation.of('b47ancedeyewear:' .. name))
    assert(slot, 'B47ANCEDEyewear tie slot was not registered')
    BodyLocations.getGroup('Human'):getOrCreateLocation(slot)
    D.types['B47ANCEDEyewear.ImprovisedTie' .. suffix] = slot
    D.types['B47ANCEDEyewear.LayeredTie' .. suffix] = slot
    D.slots[suffix] = slot
end

function D.isItem(item)
    return item ~= nil and D.types[item:getFullType()] ~= nil
end

local function definition(target, S, legacy)
    local suffix = S.isTieableHat(target) and 'Hat'
        or (target:getBodyLocation() == ItemBodyLocation.FACE and 'Face' or 'Eyes')
    return 'B47ANCEDEyewear.' .. (legacy and 'ImprovisedTie' or 'LayeredTie') .. suffix, D.slots[suffix]
end

function D.isLayered(item)
    return D.isItem(item) and item:getFullType():find('.LayeredTie',1,true) ~= nil
end

-- The native ceiling is fixed in the NEW item scripts, never changed per instance.
-- Actual condition is native; the installed capacity/contributions persist in ModData.
function D.state(tie)
    if not D.isLayered(tie) or not tie:hasModData() then return nil end
    local d = tie:getModData()[D.key]
    local material = type(d)=='table' and M.materials[d.material]
    if not material or d.schema~=1 or d.materialSchema~=1
        or not M.whole(d.revision,0,2147483646)
        or not M.whole(d.base,1,90) or not M.whole(d.strands,1,material.layers)
        or not M.whole(d.adhesive,1,5) or not M.whole(d.duct,1,10)
        or (d.tape and (not M.tapes[d.tape] or material.cutting)) then return nil end
    local tape = d.tape=='Base.DuctTape' and d.duct or d.tape and d.adhesive or 0
    if not M.whole(d.capacity,1,M.limit) or d.capacity~=d.base*d.strands+tape
        or not M.whole(tie:getCondition(),0,d.capacity) then return nil end
    return d
end

function D.canInstall(character, target, S)
    if not character or not target or not S.isTieable(target) then return false end
    local _, slot = definition(target, S)
    local inventory = character:getInventory()
    return inventory ~= nil and character:getWornItem(slot) == nil
        and inventory:hasRoomFor(character, 0.01)
end

-- IDs refer to actual native items, never serialized userdata or recreated eyewear.
function D.item(character, target, data)
    if not character or not target or not data or data.wearSchema ~= 1
        or type(data.tieId) ~= 'number' or data.tieId ~= math.floor(data.tieId)
        or data.tieId < -2147483648 or data.tieId > 2147483647 then return nil end
    local inventory = character:getInventory()
    if not inventory or target:getContainer() ~= inventory or not inventory:contains(target) then return nil end
    local tie = inventory:getItemById(data.tieId)
    if not D.isItem(tie) or tie:getContainer() ~= inventory or not tie:hasModData() then return nil end
    local link = tie:getModData()[D.key]
    if type(link) ~= 'table' or link.schema ~= 1 or link.targetId ~= target:getID()
        or link.material ~= data.material or (D.isLayered(tie) and not D.state(tie)) then return nil end
    return tie
end

function D.active(character, target, data)
    if not character or character:isDead() then return false end
    local tie = D.item(character, target, data)
    return tie ~= nil and not tie:isBroken() and tie:getCondition() > 0
        and character:getWornItem(D.types[tie:getFullType()]) == tie
        and character:isEquippedClothing(target)
end

-- Only remove an item allocated by this transaction or resolved by both link IDs.
function D.discard(character, tie)
    if isClient() or not D.isItem(tie) then return end
    local inventory = character:getInventory()
    if tie:getContainer() ~= inventory then return end
    if character:isEquippedClothing(tie) then character:removeWornItem(tie) end
    inventory:Remove(tie)
    sendRemoveItemFromContainer(inventory, tie)
end

function D.install(character, target, data, S, legacy)
    if isClient() or data.wearSchema ~= nil or data.tieId ~= nil or not S.materials[data.material]
        or not D.canInstall(character, target, S) then return nil end
    local kind, slot = definition(target, S, legacy)
    local inventory, tie = character:getInventory(), nil
    local ok, err = pcall(function()
        tie = inventory:AddItem(kind)
        assert(tie, 'Improvised tie item definition is unavailable')
        -- Native clothing assets load asynchronously. SyncClothing dereferences
        -- getVisual() for every worn item; never publish/equip an unresolved tie.
        -- Nothing has been linked or sent yet, so this is a local-only rollback.
        if not tie:getVisual() then
            inventory:Remove(tie)
            tie = nil
            return
        end
        local link = {schema=1, targetId=target:getID(), material=data.material}
        if not legacy then
            link.materialSchema, link.revision, link.strands = 1, 0, 1
            link.base = M.contribution(M.materials[data.material].durability)
            link.capacity, link.adhesive, link.duct = link.base, M.contribution(1), M.contribution(2)
            tie:setConditionNoSound(link.capacity)
        end
        tie:getModData()[D.key] = link
        tie:setName(getText('UI_B47ANCEDEyewear_ImprovisedTieName', getItemNameFromFullType(data.material)))
        tie:setCustomName(true)
        tie:setConditionLowerChance(R.options().tieResistance)
        data.wearSchema, data.tieId = 1, tie:getID()
        sendAddItemToContainer(inventory, tie)
        -- The native setter sends SyncClothing; do not duplicate it with a custom packet.
        character:setWornItem(slot, tie)
    end)
    if not ok then
        data.wearSchema, data.tieId = nil, nil
        D.discard(character, tie)
        error(err, 0)
    end
    return tie
end

function D.configure(character)
    if isClient() or not character then return end
    local resistance = R.options().tieResistance
    for _, slot in pairs(D.slots) do
        local tie = character:getWornItem(slot)
        if D.isItem(tie) and tie:getContainer() == character:getInventory()
            and tie:getConditionLowerChance() ~= resistance then
            tie:setConditionLowerChance(resistance)
        end
    end
end

return D

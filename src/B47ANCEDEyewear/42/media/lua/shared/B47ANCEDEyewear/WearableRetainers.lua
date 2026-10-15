require 'NPCs/BodyLocations'
local R = require 'B47ANCEDEyewear/Retention'
local T = {}
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

function T.configure(character)
    if isClient() or not character then return end
    local item = character:getWornItem(T.slot)
    if not T.isItem(item) or T.isUnbreakable(item)
        or item:getContainer() ~= character:getInventory() then return end
    local options = R.options()
    local resistance = item:getFullType() == 'B47ANCEDEyewear.MakeshiftRetainer'
        and options.clothResistance or options.leatherResistance
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

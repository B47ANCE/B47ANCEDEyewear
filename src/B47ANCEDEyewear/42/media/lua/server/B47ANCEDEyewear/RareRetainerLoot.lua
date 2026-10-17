-- Runs only inside vanilla's authoritative container-fill callback.
local R = require 'B47ANCEDEyewear/Retention'
local ITEM = 'B47ANCEDEyewear.UnbreakableRetainer'
local lockers = { locker = true }
local optical = { counter = true, displaycase = true, desk = true, other = true }
local pharmacy = { counter = true, shelves = true }
local locations = {
    elementaryschool = lockers, secondaryhall = lockers,
    glassesstore = optical, optometrist = optical, opthroom = optical,
    pharmacy = pharmacy,
}

local function addRareRetainer(roomName, containerType, container)
    if isClient() or not container then return end
    local eligible = locations[roomName]
    if not eligible or not eligible[containerType] then return end
    local options = R.options()
    if not options.wearable or options.rareLootChance <= 0 then return end
    -- Percentage represented in basis points: default 0.25% = 25/10000.
    local threshold = math.floor(options.rareLootChance * 100 + 0.5)
    if threshold <= 0 then return end
    local definition = getScriptManager():FindItem(ITEM)
    if not definition or not container:hasRoomFor(nil, definition:getActualWeight()) then return end
    -- Do not duplicate an existing rare retainer in this fill/respawn event.
    -- Only this one eligible container is inspected; no nested/world traversal.
    local items = container:getItems()
    for index = 0, items:size() - 1 do
        if items:get(index):getFullType() == ITEM then return end
    end
    if ZombRand(10000) < threshold then container:AddItem(ITEM) end
end

-- Replace our own listener on a Lua reload; never multiply the loot rolls.
local S = B47ANCEDEyewear
if S.rareRetainerLootHandler then Events.OnFillContainer.Remove(S.rareRetainerLootHandler) end
S.rareRetainerLootHandler = addRareRetainer
Events.OnFillContainer.Add(addRareRetainer)

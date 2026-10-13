B47ANCEDEyewear = B47ANCEDEyewear or {}
local S = B47ANCEDEyewear
local R = require 'B47ANCEDEyewear/Retention'
local F = require 'B47ANCEDEyewear/Retainers'
S.materials = { ['Base.Twine'] = true, ['Base.RubberBand'] = true,
    ['Base.DentalFloss'] = true, ['Base.Thread'] = true,
    ['Base.Thread_Aramid'] = true, ['Base.Thread_Sinew'] = true }

-- Hats that share the string/tether mechanic. Begin with the straw hat and the
-- summer sun hat; compatibility can extend this through the same list.
S.tieableHats = { ['Base.Hat_StrawHat'] = true, ['Base.Hat_SummerHat'] = true }
S.monocles = {
    ['Base.Glasses_MonocleLeft'] = true,
    ['Base.Glasses_MonocleRight'] = true,
    ['Base.Glasses_Cosmetic_MonocleLeft'] = true,
    ['Base.Glasses_Cosmetic_MonocleRight'] = true,
}

-- Tieable hats are "loose" until tied: they keep their vanilla fall chance and
-- restore it on untie. Registration makes the classification extendable.
for kind in pairs(S.tieableHats) do R.register(kind, 'loose') end

function S.isGlasses(item)
    if not item or not instanceof(item, 'Clothing') then return false end
    local kind = item:getFullType()
    if type(kind) ~= 'string' then return false end
    local name = kind:match('%.(.+)$')
    if not name then return false end
    name = name:lower()
    if name:find('eyepatch', 1, true) or name:find('mask', 1, true)
        or name:find('blindfold', 1, true) or name:find('clownnose', 1, true)
        or name:find('nose', 1, true) or name:find('bandana', 1, true)
        or name:find('balaclava', 1, true) or name:find('scarf', 1, true) then return false end
    if kind == 'Base.Glasses' or kind == 'Base.ReadingGlasses' or kind:match('^Base%.Glasses_') then return true end
    local location=item:getBodyLocation()
    local eyes=ItemBodyLocation ~= nil and location == ItemBodyLocation.EYES
    local face=ItemBodyLocation ~= nil and location == ItemBodyLocation.FACE
    -- Build 42 places several eyewear definitions in FACE rather than EYES.
    -- Accept that eyewear category without imposing English naming on authors;
    -- the exclusions above keep non-eyewear face props out.
    if face then return true end
    return eyes and name:find('glasses', 1, true) ~= nil
end

function S.isTieableHat(item)
    if not item or not instanceof(item, 'Clothing') then return false end
    local kind = item:getFullType()
    return type(kind) == 'string' and S.tieableHats[kind] == true
end

function S.isMonocle(item)
    if not item or type(item.getFullType) ~= 'function' then return false end
    return S.monocles[item:getFullType()] == true
end

-- Eyewear plus compatible headwear that can gain a retaining string.
function S.isTieable(item)
    return (S.isGlasses(item) and not S.isMonocle(item)) or S.isTieableHat(item)
end

local function validState(data)
    if type(data) ~= 'table' or data.version ~= 1
        or type(data.original) ~= 'number' or data.original ~= data.original
        or data.original < 0 or data.original > 100
        or type(data.tied) ~= 'boolean' then return nil end
    return data
end

function S.state(item)
    if not item or not item:hasModData() then return nil end
    local modData = item:getModData()
    -- Compatibility read only: clients never migrate shared persistent state.
    -- Any canonical value (including a retirement marker) prevents resurrection.
    local data = modData.B47ANCEDEyewear
    if data == nil then data = modData.StayPutGlasses end
    return validState(data)
end

function S.isTied(item)
    local data = S.state(item)
    return data ~= nil and data.tied
end

function S.isMaterial(item)
    return item ~= nil and S.materials[item:getFullType()] == true
        and (not instanceof(item, 'DrainableComboItem') or item:getCurrentUses() >= 1)
end

-- Keep the existing item, model, texture and instance ID.  Only its displayed
-- name changes while tied, and a pre-existing custom name is restored on untie.
function S.captureName(item)
    if not item or not item.getName then return nil, false end
    local ok,name=pcall(item.getName,item)
    if not ok or type(name) ~= "string" or name == "" then return nil, false end
    local custom=false
    if item.isCustomName then
        local customOk,value=pcall(item.isCustomName,item)
        custom=customOk and value == true
    end
    return name,custom
end

function S.applyTiedName(item,data)
    if not item or not data or type(data.name) ~= "string" or not item.setName then return end
    item:setName(data.name .. " (Tied)")
    if item.setCustomName then item:setCustomName(true) end
end

function S.restoreName(item,data)
    if not item or not data or type(data.name) ~= "string" or not item.setName then return end
    item:setName(data.name)
    if item.setCustomName then item:setCustomName(data.customName == true) end
end

function S.valid(character, item, material, untie)
    if not character or character:isDead() or not S.isTieable(item) then return false end
    local inventory = character:getInventory()
    if not inventory:contains(item) or not character:isEquippedClothing(item) then return false end
    -- Finite eyewear uses revisioned retainer intents, never the legacy unlimited-tie recipe.
    if S.isGlasses(item) and (F.available() or F.state(item)) then return false end
    if untie then return S.isTied(item) end
    return not item:isBroken() and not S.isTied(item)
        and item:getChanceToFall() > 0 and item:getChanceToFall() <= 100
        and S.isMaterial(material) and inventory:contains(material)
end

local function syncChangedItem(character,item)
    syncItemModData(character,item)
    -- ModData sync alone does not include display name or clothing fields.
    -- Build 42 exposes syncItemFields for those changes in multiplayer.
    if type(syncItemFields) == "function" then syncItemFields(character,item) end
end

function S.migrateState(character, item)
    if isClient() or not character or not item or not item:hasModData() then return false end
    local modData = item:getModData()
    if modData.B47ANCEDEyewear ~= nil then return false end
    local legacy = validState(modData.StayPutGlasses)
    if not legacy then return false end
    -- Independent copy: retain the old save record unchanged for recovery.
    local migrated = {}
    for key, value in pairs(legacy) do migrated[key] = value end
    modData.B47ANCEDEyewear = migrated
    syncChangedItem(character, item)
    return true
end

-- Monocles were tieable in older builds. They are now intentionally unsupported:
-- restore their prior display name, discard only this obsolete mod state, and let
-- the monocle profile supply its 70-point untied retention value.
local function clearLegacyMonocleState(character, item)
    if not S.isMonocle(item) or isClient() then return false end
    local data = S.state(item)
    if not data then return false end
    if data.tied then S.restoreName(item, data) end
    -- Preserve legacy data, but prevent an obsolete monocle tie from resurfacing.
    item:getModData().B47ANCEDEyewear = { retired = true }
    syncChangedItem(character, item)
    return true
end

function S.tie(character, item, material)
    if isClient() or not S.valid(character, item, material, false) then return false end
    local name,customName=S.captureName(item)
    local data={version=1,tied=true,original=item:getChanceToFall(),material=material:getFullType(),name=name,customName=customName}
    -- Complete the retained item mutation before consuming the material. This
    -- prevents a later item-update failure from charging the material without
    -- leaving the glasses tied.
    item:getModData().B47ANCEDEyewear=data
    S.applyTiedName(item,data)
    item:setChanceToFall(0)
    syncChangedItem(character,item)
    material:UseAndSync()
    return true
end

function S.untie(character, item)
    if isClient() or not S.valid(character, item, nil, true) then return false end
    S.migrateState(character, item)
    local data=S.state(item)
    data.tied=false
    S.restoreName(item,data)
    S.applyChance(item, character)
    syncChangedItem(character,item)
    return true
end

-- Apply the retention-derived ChanceToFall to one worn item. `chance = nil`
-- means "leave vanilla unchanged".
function S.applyChance(item, character)
    if not item or not instanceof(item, 'Clothing') then return end
    S.migrateState(character, item)
    clearLegacyMonocleState(character, item)
    F.migrateLegacy(character,item)
    local data = S.state(item)
    local tied = data ~= nil and data.tied or false
    local chance = R.chanceFor(item, tied, data and data.original)
    if chance ~= nil and item:getChanceToFall() ~= chance then
        item:setChanceToFall(chance)
    end
end

local function craftTieable(data)
    if not data or not data.getAllInputItems then return nil end
    local ok,items=pcall(data.getAllInputItems,data)
    if not ok or not items then return nil end
    for i=0,items:size()-1 do
        local item=items:get(i)
        if S.isTieable(item) then return item end
    end
end

local function craftMaterial(data)
    if not data or not data.getAllConsumedItems then return nil end
    local ok,items=pcall(data.getAllConsumedItems,data)
    if not ok or not items then return nil end
    for i=0,items:size()-1 do
        local item=items:get(i)
        if S.isMaterial(item) then return item end
    end
end

function S.onCraftTest(data)
    local character=data and data.getCharacter and data:getCharacter()
    return S.valid(character,craftTieable(data),craftMaterial(data),false)
end

function S.onCraftCreate(data)
    if isClient() then return end
    local character=data and data.getCharacter and data:getCharacter()
    local item,material=craftTieable(data),craftMaterial(data)
    S.tie(character,item,material)
end

function S.refresh(character)
    if not character then return end
    local worn = character:getWornItems()
    if not worn then return end
    for i = 0, worn:size() - 1 do
        S.applyChance(worn:get(i):getItem(), character)
    end
end

R.isEyewear = S.isGlasses
R.isMonocle = S.isMonocle

Events.OnClothingUpdated.Add(S.refresh)
Events.OnPlayerUpdate.Add(S.refresh)
Events.OnCreatePlayer.Add(function(_, character) S.refresh(character) end)
return S

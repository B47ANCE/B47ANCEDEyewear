B47ANCEDEyewear = B47ANCEDEyewear or {}
local S = B47ANCEDEyewear
local R = require 'B47ANCEDEyewear/Retention'
local T = require 'B47ANCEDEyewear/WearableRetainers'
S.RetainerItems = T
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
    item:setName(getText('UI_B47ANCEDEyewear_TiedName', data.name))
    if item.setCustomName then item:setCustomName(true) end
end

function S.restoreName(item,data)
    if not item or not data or type(data.name) ~= "string" or not item.setName then return end
    item:setName(data.name)
    if item.setCustomName then item:setCustomName(data.customName == true) end
end

local function ownsWornItem(character, item)
    if not character or character:isDead() or not S.isTieable(item) then return false end
    local inventory = character:getInventory()
    return inventory ~= nil and item:getContainer() == inventory and inventory:contains(item)
        and character:isEquippedClothing(item)
end

-- Item-only eligibility also supports vanilla crafting previews without a player.
function S.isReadyToTie(item)
    return S.isTieable(item) and R.options().tying
        and not item:isBroken() and not S.isTied(item)
        and item:getChanceToFall() > 0 and item:getChanceToFall() <= 100
end

function S.canTie(character, item)
    return ownsWornItem(character, item) and S.isReadyToTie(item)
end

function S.canUseMaterial(character, material)
    if not character or character:isDead() or not S.isMaterial(material) then return false end
    local inventory = character:getInventory()
    return inventory ~= nil and material:getContainer() == inventory and inventory:contains(material)
end

function S.valid(character, item, material, untie)
    if untie then return ownsWornItem(character, item) and S.isTied(item) end
    return S.canTie(character, item) and S.canUseMaterial(character, material)
end

local syncFailureReported = false
local function syncChangedItem(character,item)
    local ok,err=pcall(function()
        syncItemModData(character,item)
        if type(syncItemFields)=='function' then syncItemFields(character,item) end
    end)
    if not ok and not syncFailureReported then
        syncFailureReported=true
        print('[B47ANCEDEyewear] Item synchronization failed: '..tostring(err))
    end
    return ok
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
    local modData=item:getModData()
    local previous=modData.B47ANCEDEyewear
    local original=item:getChanceToFall()
    local container,uses=material:getContainer(),material:getCurrentUses()
    local data={version=1,tied=true,original=original,material=material:getFullType(),name=name,customName=customName}
    local function rollback()
        modData.B47ANCEDEyewear=previous
        if name then item:setName(name);item:setCustomName(customName) end
        item:setChanceToFall(original)
    end
    local changed,changeError=pcall(function()
        modData.B47ANCEDEyewear=data
        S.applyTiedName(item,data)
        item:setChanceToFall(0)
    end)
    if not changed then
        rollback()
        print('[B47ANCEDEyewear] Tie failed: '..tostring(changeError))
        return false
    end
    -- UseAndSync can consume successfully before its network notification throws.
    local paid,useError=pcall(material.UseAndSync,material)
    local consumed=material:getContainer()~=container or material:getCurrentUses()<uses
    if not consumed then
        rollback()
        print('[B47ANCEDEyewear] Material use did not consume a use: '..tostring(useError))
        return false
    end
    if not paid then print('[B47ANCEDEyewear] Material consumed; use notification failed: '..tostring(useError)) end
    syncChangedItem(character,item)
    return true
end

function S.untie(character, item)
    if isClient() or not S.valid(character, item, nil, true) then return false end
    S.migrateState(character,item)
    local data=S.state(item)
    local name,customName=S.captureName(item)
    local previousChance=item:getChanceToFall()
    local ok,err=pcall(function()
        data.tied=false
        S.restoreName(item,data)
        S.applyChance(item,character)
    end)
    if not ok then
        data.tied=true
        if name then item:setName(name);item:setCustomName(customName) end
        item:setChanceToFall(previousChance)
        print('[B47ANCEDEyewear] Untie failed: '..tostring(err))
        return false
    end
    syncChangedItem(character,item)
    return true
end

-- Apply the retention-derived ChanceToFall to one worn item. `chance = nil`
-- means "leave vanilla unchanged".
function S.applyChance(item, character, retained)
    if not item or not instanceof(item, 'Clothing') then return end
    S.migrateState(character, item)
    clearLegacyMonocleState(character, item)
    local data = S.state(item)
    local tied = data ~= nil and data.tied or false
    local chance = R.chanceFor(item, tied, data and data.original)
    if retained == nil then retained = T.target(character, S) == item end
    if retained and not tied then chance = R.options().retainerChance end
    if chance ~= nil and item:getChanceToFall() ~= chance then
        item:setChanceToFall(chance)
        if not isClient() and character then syncChangedItem(character,item) end
    end
end

function S.refresh(character)
    if not character then return end
    local worn = character:getWornItems()
    if not worn then return end
    local retained = T.target(character, S)
    for i = 0, worn:size() - 1 do
        local item = worn:get(i):getItem()
        S.applyChance(item, character, item == retained)
    end
end

R.isEyewear = S.isGlasses
R.isMonocle = S.isMonocle

Events.OnClothingUpdated.Add(S.refresh)
Events.OnPlayerUpdate.Add(S.refresh)
Events.OnCreatePlayer.Add(function(_, character) S.refresh(character) end)
return S

-- Verified Build 42.21 vanilla FullTypes. Values are mod balance, not hit counts.
local M = { materials = {
    ['Base.RubberBand'] = {durability=2, layers=1},
    ['Base.Thread'] = {durability=2, layers=3},
    ['Base.DentalFloss'] = {durability=2, layers=3},
    ['Base.RippedSheets'] = {durability=4, layers=1},
    ['Base.DenimStrips'] = {durability=6, layers=1},
    ['Base.Twine'] = {durability=6, layers=1},
    ['Base.Thread_Sinew'] = {durability=3, layers=3},
    ['Base.LeatherStrips'] = {durability=10, layers=1},
    ['Base.FishingLine'] = {durability=4, layers=3},
    ['Base.ElectricWire'] = {durability=12, layers=1},
    ['Base.Wire'] = {durability=14, layers=1},
    ['Base.PremiumFishingLine'] = {durability=5, layers=3},
    ['Base.Zipties'] = {durability=16, layers=1, cutting=true},
    ['Base.Thread_Aramid'] = {durability=6, layers=3},
}, tapes = {['Base.Scotchtape']=1, ['Base.DuctTape']=2}, limit = 100 }

function M.whole(value, low, high)
    return type(value)=='number' and value==value and value>=low and value<=high
        and value==math.floor(value)
end

function M.usable(item)
    return item ~= nil and (not instanceof(item, 'DrainableComboItem') or item:getCurrentUses()>=1)
end

function M.consume(character, material)
    if isClient() then return end
    if instanceof(material, 'DrainableComboItem') then
        material:UseAndSync()
    else
        -- Clean fabric's UseAndSync creates dirty fabric via ReplaceOnUse.
        -- Tying spends the entire strip, so remove/sync the exact item instead.
        local inventory = character:getInventory()
        inventory:Remove(material)
        sendRemoveItemFromContainer(inventory,material)
    end
end

function M.contribution(points)
    local raw = SandboxVars and SandboxVars.B47ANCEDEyewear or {}
    local multiplier = raw.ImprovisedTieDurabilityMultiplier
    if type(multiplier)~='number' or multiplier~=multiplier or multiplier<0.25 or multiplier>5 then
        multiplier = 1
    end
    return math.max(1, math.floor(points*multiplier+0.5))
end

-- Same tags and IsNotDull rule as native crafting, plus usable condition.
-- Tool stays in inventory; never trust a client-provided "sharp" flag.
function M.cutter(character, tool)
    if not character or not tool or character:isDead() then return false end
    local inventory = character:getInventory()
    return inventory ~= nil and tool:getContainer()==inventory and inventory:contains(tool)
        and tool:getCondition()>0 and not tool:isBroken()
        and (tool:hasTag(ItemTag.SHARP_KNIFE) or tool:hasTag(ItemTag.SCISSORS))
        and (not tool:hasSharpness() or not tool:isDull())
        and (not tool:hasHeadCondition() or tool:getHeadCondition()>0)
end

return M

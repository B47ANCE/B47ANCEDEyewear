local S = require 'B47ANCEDEyewear/Core'

-- Vanilla CraftRecipe OnTest is a production input-eligibility hook. It runs
-- for each candidate item on both sides; no state is changed here.
function S.canCraftTie(item, character)
    if S.isMaterial(item) then
        return character == nil or S.canUseMaterial(character, item)
    end
    -- Vanilla's item-preview helper omits the player. Recipe flags still require
    -- worn headwear; ownership is always enforced again when the action completes.
    if character == nil then return S.isReadyToTie(item) end
    return S.canTie(character, item)
end

function S.craftTie(recipeData, character)
    if isClient() or not recipeData or not character then return false end
    local inputs = recipeData:getAllInputItems()
    if not inputs or inputs:size() ~= 2 then return false end
    local headwear, material
    for index = 0, inputs:size() - 1 do
        local item = inputs:get(index)
        if S.isTieable(item) then
            if headwear then return false end
            headwear = item
        elseif S.isMaterial(item) then
            if material then return false end
            material = item
        else
            return false
        end
    end
    -- Both recipe inputs are kept by vanilla. Only this server/SP transaction
    -- consumes a use, and only from the selected pair after final validation.
    return S.tie(character, headwear, material)
end

return S

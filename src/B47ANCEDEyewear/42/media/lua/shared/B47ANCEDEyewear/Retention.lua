B47ANCEDEyewear = B47ANCEDEyewear or {}
local R = {}
B47ANCEDEyewear.Retention = R

-- Centralized, tunable retention categories. `chance = nil` means "keep the
-- item's vanilla ChanceToFall" (no override). Probabilities are 0..100.
R.categories = {
    loose = { chance = nil },
    fitted = { chance = 15 },
    monocle = { chance = 70 },
    strapped = { chance = 0 },
    tethered = { chance = 0 },
}

-- Gameplay settings use the synchronized server sandbox; profiles remain defaults.
function R.options()
    local raw=SandboxVars and SandboxVars.B47ANCEDEyewear or {}
    local function number(key,default,low,high)
        local n=raw[key]
        return type(n)=='number' and n==n and n>=low and n<=high and n or default
    end
    return {tying=raw.TyingEnabled~=false,
        wearable=raw.WearableRetainersEnabled~=false,
        retainerChance=math.floor(number('WearableRetainerFallChance',0,0,100)),
        multiplier=number('EyewearFallMultiplier',1,0.25,5),
        headwear=math.floor(number('StrappedHeadwearFallChance',0,0,100))}
end
local function eyewearChance(chance) return math.min(100,math.ceil(chance*R.options().multiplier)) end

-- Exact item-type overrides, populated through `register`. Names are keyed by
-- the full type (e.g. "Base.Hat_Army") so compatibility patches can classify
-- third-party items without editing gameplay code.
R.overrides = {}

-- Vanilla eyewear profiles are deliberately item-specific. A value is the
-- effective untied ChanceToFall while B47ANCE'd Eyewear manages a worn item.
-- Unknown/modded eyewear keeps the legacy fitted fallback unless a compatibility
-- patch supplies an explicit registration.
R.eyewearProfiles = {
    ['Base.Glasses_SkiGoggles'] = 2, ['Base.Glasses_SwimmingGoggles'] = 2,
    ['Base.Glasses_SafetyGoggles'] = 5,
    ['Base.Glasses_Shooting'] = 8, ['Base.Glasses_Prescription_Shooting'] = 8,
    ['Base.Glasses_OldWeldingGoggles'] = 8,
    ['Base.Glasses'] = 10, ['Base.Glasses_Prescription'] = 10,
    ['Base.Glasses_Aviators'] = 15, ['Base.Glasses_Prescription_Aviators'] = 15,
    ['Base.Glasses_Normal_HornRimmed'] = 15, ['Base.Glasses_Cosmetic_Normal_HornRimmed'] = 15,
    ['Base.Glasses_CatsEye'] = 18, ['Base.Glasses_CatsEye_Sun'] = 18,
    ['Base.Glasses_Cosmetic_CatsEye'] = 18, ['Base.Glasses_Prescription_CatsEye_Sun'] = 18,
    ['Base.Glasses_Normal'] = 20, ['Base.Glasses_Cosmetic_Normal'] = 20,
    ['Base.Glasses_Sun'] = 20, ['Base.Glasses_Prescription_Sun'] = 20,
    ['Base.Glasses_Round_Normal'] = 20, ['Base.Glasses_Round_Shades'] = 20,
    ['Base.Glasses_Cosmetic_Round_Normal'] = 20, ['Base.Glasses_Prescription_Round_Shades'] = 20,
    ['Base.Glasses_70s_Gold'] = 20, ['Base.Glasses_Cosmetic_70s_Gold'] = 20,
    ['Base.Glasses_Macho'] = 20,
    ['Base.Glasses_Reading'] = 25, ['Base.Glasses_JackieO'] = 25,
    ['Base.Glasses_Prescription_JackieO'] = 25,
    ['Base.Glasses_HalfMoon'] = 30, ['Base.Glasses_Cosmetic_HalfMoon'] = 30,
    ['Base.Glasses_SunCheap'] = 30, ['Base.Glasses_NewWave'] = 30,
    ['Base.Glasses_Round_HoloSkulls'] = 30,
    ['Base.Glasses_3dGlasses'] = 35, ['Base.Glasses_Groucho'] = 35,
    ['Base.Glasses_Venetian'] = 35, ['Base.Glasses_Novelty_Xray'] = 35,
    ['Base.Glasses_MonocleLeft'] = 70, ['Base.Glasses_MonocleRight'] = 70,
    ['Base.Glasses_Cosmetic_MonocleLeft'] = 70, ['Base.Glasses_Cosmetic_MonocleRight'] = 70,
}

-- Name substrings that unambiguously describe protective headgear held on by a
-- chin strap or equivalent retention, not loose headwear. "helmet" covers
-- Crash/Riot/Hockey/SPH helmets; "hardhat" and "fireman" cover those; the
-- "hat_army" prefix covers the military helmets (Hat_Army, Hat_ArmyWWII,
-- Hat_ArmyDesert) without matching Hat_PeakedCapArmy or Hat_BeretArmy.
local STRAPPED = { 'helmet', 'hardhat', 'fireman', 'hat_army' }

-- Set by Core.lua to its nuanced eyewear predicate so masks, eyepatches and
-- other FACE props are never misclassified as fitted.
R.isEyewear = nil
R.isMonocle = nil

function R.register(itemType, category)
    if type(itemType) ~= 'string' or itemType == '' then return false end
    if not R.categories[category] then return false end
    R.overrides[itemType] = category
    return true
end

function R.registerEyewearProfile(itemType, chance)
    if type(itemType) ~= 'string' or itemType == '' then return false end
    if type(chance) ~= 'number' or chance ~= chance or chance < 0 or chance > 100 then return false end
    R.eyewearProfiles[itemType] = chance
    return true
end

function R.baseName(kind)
    if type(kind) ~= 'string' then return nil end
    local name = kind:match('%.(.+)$') or kind
    return name:lower()
end

-- Classify a clothing item into a retention category, or nil to leave vanilla.
function R.classify(item)
    if not item then return nil end
    local kind = item:getFullType()
    if type(kind) ~= 'string' then return nil end
    if R.overrides[kind] then return R.overrides[kind] end
    local name = R.baseName(kind)
    if not name then return nil end
    for _, pattern in ipairs(STRAPPED) do
        if name:find(pattern, 1, true) then return 'strapped' end
    end
    if R.isMonocle and R.isMonocle(item) then return 'monocle' end
    if R.isEyewear and R.isEyewear(item) then return 'fitted' end
    return nil
end

-- Effective ChanceToFall for a worn item, or nil to leave vanilla unchanged.
-- A tied item is tethered regardless of its base category. `original` is the
-- stored pre-tie vanilla chance used to restore loose items on untie.
function R.chanceFor(item, tied, original)
    if tied then return R.categories.tethered.chance end
    local kind = item and item:getFullType()
    local profile = type(kind) == 'string' and R.eyewearProfiles[kind] or nil
    if profile ~= nil then return eyewearChance(profile) end
    local category = R.classify(item)
    if not category then return nil end
    if category=='strapped' then return R.options().headwear end
    local def = R.categories[category]
    if category=='fitted' or category=='monocle' then return eyewearChance(def.chance) end
    if def and def.chance ~= nil then return def.chance end
    -- chance = nil means "keep vanilla"; restore the recorded vanilla chance
    -- when it is known (a previously tied loose item), otherwise leave it.
    return original
end

return R

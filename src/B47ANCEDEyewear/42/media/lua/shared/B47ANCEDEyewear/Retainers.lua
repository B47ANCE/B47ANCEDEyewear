-- Authoritative finite-retainer rules. Native code alone commits a successful catch.
local R = { key = 'B47ANCEDEyewearRetainer', schema = 2 }
B47ANCEDEyewear = B47ANCEDEyewear or {}
B47ANCEDEyewear.Retainers = R
R.materials = {
    ['Base.RubberBand']={dur=2,layers=1}, ['Base.Thread']={dur=2,layers=3},
    ['Base.DentalFloss']={dur=2,layers=3}, ['Base.RippedSheets']={dur=4,layers=1},
    ['Base.DenimStrips']={dur=6,layers=1}, ['Base.Twine']={dur=6,layers=1},
    ['Base.Thread_Sinew']={dur=3,layers=3}, ['Base.LeatherStrips']={dur=10,layers=1},
    ['Base.FishingLine']={dur=4,layers=3}, ['Base.ElectricWire']={dur=12,layers=1},
    ['Base.Wire']={dur=14,layers=1}, ['Base.PremiumFishingLine']={dur=5,layers=3},
    ['Base.Zipties']={dur=16,layers=1,noTape=true}, ['Base.Thread_Aramid']={dur=6,layers=3},
}
R.tapes = { ['Base.Scotchtape']=1, ['Base.DuctTape']=2 }
local function finite(n) return type(n)=='number' and n==n and n>-math.huge and n<math.huge end
local function whole(n,low,high) return finite(n) and n==math.floor(n) and n>=low and n<=high end
function R.options()
    local raw = SandboxVars and SandboxVars.B47ANCEDEyewear or {}
    local function number(key,default,low,high)
        local n=raw[key]; return finite(n) and n>=low and n<=high and n or default
    end
    return { enabled=type(raw.MakeshiftRetainersEnabled)~='boolean' or raw.MakeshiftRetainersEnabled,
        permanent=type(raw.PermanentRetainerEnabled)~='boolean' or raw.PermanentRetainerEnabled,
        durability=number('RetainerDurabilityMultiplier',1,0.25,10),
        damage=number('RetainerImpactDamageMultiplier',1,0.25,10),
        rarity=number('PermanentRetainerRarity',2,1,3) }
end
function R.available()
    return type(B47ANCEDEyewearBridgeReady)=='function' and B47ANCEDEyewearBridgeReady()==true
end
function R.compatible(item)
    local S=B47ANCEDEyewear
    return item and S.isGlasses(item) and not S.isMonocle(item)
end
function R.state(item)
    if not item or not item:hasModData() then return nil end
    local d=item:getModData()[R.key]
    if type(d)~='table' or d.schema~=2 or d.kind~='makeshift' or not R.materials[d.material]
        or not whole(d.revision,0,2147483646) or not whole(d.maximum,1,1000)
        or not whole(d.current,0,d.maximum) or not whole(d.strands,1,R.materials[d.material].layers)
        or not whole(d.contribution,1,160) or (d.tape~=nil and not R.tapes[d.tape]) then return nil end
    if (R.materials[d.material].noTape and d.tape) or
        d.maximum~=d.contribution*d.strands+(R.tapes[d.tape] or 0) then return nil end
    return d
end
local function copy(d) local n={} for k,v in pairs(d) do n[k]=v end return n end
function R.active(item) local d=R.state(item); return d and d.current>0 and d end
function R.validOwner(character,item)
    return character and not character:isDead() and R.compatible(item)
        and item:getContainer()==character:getInventory() and character:isEquippedClothing(item)
        and not item:isBroken()
end
local function usable(character,material)
    return material and material:getContainer()==character:getInventory()
        and (not instanceof(material,'DrainableComboItem') or material:getCurrentUses()>=1)
end
-- Exactly one script use; verified vanilla UseAndSync owns consumption/replication.
local function consume(material) material:UseAndSync() end
local function sync(character,item)
    syncItemModData(character,item)
    if type(syncItemFields)=='function' then syncItemFields(character,item) end
end
R.sync=sync
local function commitAction(character,item,material,state)
    local previous=item:getModData()[R.key]
    local before=instanceof(material,'DrainableComboItem') and material:getCurrentUses() or nil
    item:getModData()[R.key]=state
    local ok=pcall(consume,material)
    if not ok and material:getContainer()==character:getInventory()
        and (before==nil or material:getCurrentUses()==before) then
        item:getModData()[R.key]=previous;return false
    end
    -- A network notification failure after consumption must not erase a committed retainer.
    pcall(sync,character,item);return true
end
function R.install(character,item,material,revision)
    if isClient() or not R.available() or not R.options().enabled or not R.validOwner(character,item)
        or R.active(item) or not usable(character,material) then return false end
    local spec=R.materials[material:getFullType()]; if not spec then return false end
    local previous=R.state(item)
    if item:hasModData() and item:getModData()[R.key]~=nil and not previous then return false end
    local currentRevision=previous and previous.revision or 0
    if currentRevision>=2147483646 then return false end
    if revision~=currentRevision then return false end
    local contribution=math.max(1,math.ceil(spec.dur*R.options().durability))
    local state={schema=2,kind='makeshift',material=material:getFullType(),strands=1,
        contribution=contribution,current=contribution,maximum=contribution,revision=currentRevision+1}
    return commitAction(character,item,material,state)
end
function R.reinforce(character,item,material,revision)
    local d=R.active(item)
    if isClient() or not R.available() or not R.options().enabled or not R.validOwner(character,item)
        or not d or d.revision>=2147483646 or d.revision~=revision or not usable(character,material)
        or material:getFullType()~=d.material or d.strands>=R.materials[d.material].layers then return false end
    local n=copy(d);n.strands=n.strands+1;n.current=n.current+d.contribution
    n.maximum=n.maximum+d.contribution;n.revision=n.revision+1
    return commitAction(character,item,material,n)
end
function R.applyTape(character,item,material,revision)
    local d=R.active(item)
    if isClient() or not R.available() or not R.options().enabled or not R.validOwner(character,item)
        or not d or d.revision>=2147483646 or d.revision~=revision or d.tape or R.materials[d.material].noTape
        or not usable(character,material) then return false end
    local bonus=R.tapes[material:getFullType()];if not bonus then return false end
    local n=copy(d);n.tape=material:getFullType();n.current=n.current+bonus;n.maximum=n.maximum+bonus;n.revision=n.revision+1
    return commitAction(character,item,material,n)
end
function R.cuttingTool(character,tool)
    return tool and tool:getContainer()==character:getInventory() and tool:getCondition()>0
        and ItemTag and (tool:hasTag(ItemTag.SHARP_KNIFE) or tool:hasTag(ItemTag.SCISSORS))
        and not tool:isDull()
end
function R.remove(character,item,revision,tool)
    local d=R.state(item)
    if isClient() or not R.validOwner(character,item) or not d or d.revision>=2147483646 or d.current<=0 or d.revision~=revision then return false end
    if d.material=='Base.Zipties' then
        if not R.cuttingTool(character,tool) then return false end
    end
    local n=copy(d);n.current=0;n.revision=n.revision+1
    item:getModData()[R.key]=n;pcall(sync,character,item);return true
end
-- Pure proposal: no mutation, RNG, consumption, networking or item replacement.
function R.prepareCatch(character,item,location,hitHead,authority)
    if isClient() or (authority~='SERVER' and authority~='SP') or not R.options().enabled
        or not R.validOwner(character,item) then return nil end
    local d=R.active(item);if not d or d.revision>=2147483646 then return nil end
    local n=copy(d);n.current=math.max(0,d.current-math.max(1,math.ceil(R.options().damage)))
    n.revision=d.revision+1
    return n -- current=0 still represents a successful breaking catch.
end
B47ANCEDEyewearPrepareCatch=R.prepareCatch
B47ANCEDEyewearCatchCommitted=function(character,item) pcall(sync,character,item) end
function R.migrateLegacy(character,item)
    local S=B47ANCEDEyewear
    if isClient() or not R.available() or not R.validOwner(character,item) or R.state(item) then return false end
    local legacy=S.state(item)
    if not legacy or not legacy.tied or not R.materials[legacy.material] then return false end
    local contribution=math.max(1,math.ceil(R.materials[legacy.material].dur*R.options().durability))
    local n={schema=2,kind='makeshift',material=legacy.material,strands=1,contribution=contribution,
        current=contribution,maximum=contribution,revision=1}
    local retired=copy(legacy);retired.tied=false
    item:getModData()[R.key]=n;item:getModData().B47ANCEDEyewear=retired
    S.restoreName(item,legacy);pcall(sync,character,item);return true
end
function R.describe(item)
    local d=R.active(item);if not d then return nil end
    return getText('UI_B47ANCEDEyewear_Durability',d.current,d.maximum) .. ' / ' ..
        getItemNameFromFullType(d.material) .. ' / ' .. getText('UI_B47ANCEDEyewear_Strands',d.strands) ..
        (d.tape and (' / '..getItemNameFromFullType(d.tape)) or '')
end
return R

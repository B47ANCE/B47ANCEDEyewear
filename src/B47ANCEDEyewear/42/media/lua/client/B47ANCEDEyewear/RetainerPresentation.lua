-- Read-only projection of replicated item metadata. Never migrates or repairs state.
local R=require 'B47ANCEDEyewear/RetainerState'
local P={}
local function text(key,...) return getText('UI_B47ANCEDEyewear_'..key,...) end
local function finite(n) return type(n)=='number' and n==n and n>-math.huge and n<math.huge end
local function whole(n,lo,hi) return finite(n) and n==math.floor(n) and n>=lo and n<=hi end
local function unknown() return {unavailable=true,lines={text('RetainerTitle'),text('Unavailable')}} end
local function conditionModel(item, lines, installedMaximum)
    local current, maximum = item:getCondition(), installedMaximum or item:getConditionMax()
    if not whole(maximum,1,127) or not whole(current,0,maximum) then return unknown() end
    lines[#lines+1] = text('Condition',text(current == 0 and 'Broken'
        or current / maximum <= 0.25 and 'AboutToBreak'
        or current < maximum and 'Worn' or 'Secure'))
    lines[#lines+1] = text('Durability',current,maximum)
    local ratio = current / maximum
    return {lines=lines,barAfter=#lines,ratio=ratio,percent=math.floor(ratio*100+0.5),
        current=current,maximum=maximum}
end
function P.model(item)
    if not item then return nil end
    local S=B47ANCEDEyewear
    local T=S and S.RetainerItems
    local D=S and S.TieDurability
    if D and D.isItem(item) then
        local link = D.state(item)
        if D.isLayered(item) and not link then return unknown() end
        local lines = {text('RetainerTitle'),item:getName(),text('ImprovisedTieInstructions')}
        if not link then lines[#lines+1]=text('LegacyTie') end
        local model = conditionModel(item,lines,link and link.capacity)
        if not link or model.unavailable then return model end
        lines[#lines+1]=text('Material',getItemNameFromFullType(link.material))
        lines[#lines+1]=text('Strands',link.strands)
        if link.strands>1 or link.tape then
            lines[#lines+1]=text('Modifiers')
            if link.strands>1 then lines[#lines+1]=text('StrandModifier',link.strands,(link.strands-1)*link.base) end
            if link.tape then lines[#lines+1]=text('TapeModifier',getItemNameFromFullType(link.tape),link.capacity-link.base*link.strands) end
        end
        lines[#lines+1]=text('BaseDurability',link.base)
        lines[#lines+1]=text('MaximumDurability',link.capacity)
        if link.material=='Base.Zipties' then lines[#lines+1]=text('ZipCutting') end
        return model
    end
    if T and T.isItem(item) then
        if T.isUnbreakable(item) then
            return {lines={text('RetainerTitle'),getItemNameFromFullType(item:getFullType()),
                text('UnbreakableInstructions'),text('UnbreakableCondition')}}
        end
        local tape = T.tapeState(item)
        if item:hasModData() and item:getModData()[T.tapeKey]~=nil and not tape then return unknown() end
        local lines = {text('RetainerTitle'),getItemNameFromFullType(item:getFullType()),
            text('WearableInstructions'),text('WearableDurability'),text('RetainerTapeInstructions')}
        local model = conditionModel(item,lines)
        if model.unavailable then return model end
        local resistance,base = T.resistance(item)
        lines[#lines+1]=text('WearResistance',resistance)
        if tape then
            if resistance>base then
                lines[#lines+1]=text('Modifiers')
                lines[#lines+1]=text('TapeWearModifier',getItemNameFromFullType(tape.tape),resistance-base)
            else lines[#lines+1]=text('TapeInstalled',getItemNameFromFullType(tape.tape)) end
        end
        return model
    end
    if T then
        local owner=item:getEquipParent()
        if owner and T.target(owner,S)==item then
            local retainer=T.worn(owner)
            if T.isUnbreakable(retainer) then
                return {lines={text('RetainerTitle'),text('WearableProtection'),text('UnbreakableCondition')}}
            end
            local model = P.model(retainer)
            if not model or model.unavailable then return unknown() end
            model.lines[#model.lines+1]=text('WearableProtection')
            return model
        end
    end
    if not item:hasModData() then return nil end
    local tied=S and S.state and S.state(item)
    if tied and tied.tied then
        if type(tied.material)~='string' then return unknown() end
        local owner=item:getEquipParent()
        local tie=D and D.item(owner,item,tied)
        local lines={text('RetainerTitle'),text('Material',getItemNameFromFullType(tied.material)),text('TiedAttachment')}
        if tie then
            local model = P.model(tie)
            if not model or model.unavailable then return unknown() end
            model.lines[#model.lines+1]=text(D.active(owner,item,tied) and 'TieActive' or 'TieInactive')
            return model
        end
        lines[#lines+1]=text('TieInactive')
        return {lines=lines}
    end
    local raw=item:getModData()[R.key]
    if raw==nil then return nil end
    if not R.compatible(item) or type(raw)~='table' or raw.schema~=R.schema then return unknown() end
    -- Stored historical records are displayed as inactive; no protection is implied.
    if raw.kind=='permanent' then
        if raw.material~='B47ANCEDEyewear.EyewearRetainer' or raw.permanent~=true
            or not whole(raw.revision,0,2147483646) or raw.current~=nil or raw.maximum~=nil
            or raw.strands~=nil or raw.tape~=nil or raw.contribution~=nil then return unknown() end
        return {permanent=true,lines={text('RetainerTitle'),text('InactiveProtection'),
            text('Material',text('PermanentMaterial')),text('Condition',text('Permanent')),text('InfiniteDurability')}}
    end
    local d=R.state(item)
    if not d or raw.permanent==true then return unknown() end
    -- Destructive removal and a breaking catch both leave zero-DUR tombstones.
    -- Schema 2 cannot distinguish them; label their protection as Broken until replaced.
    local ratio=d.current/d.maximum
    local condition
    if ratio==0 then condition='Broken'
    elseif ratio<=0.25 then condition='AboutToBreak'
    elseif ratio<=0.5 then
        if d.material=='Base.RubberBand' then condition='Stretched'
        elseif d.material=='Base.ElectricWire' or d.material=='Base.Wire' or d.material=='Base.Zipties' then condition='Damaged'
        else condition='Fraying' end
    elseif ratio<=0.75 then condition='Worn' else condition='Secure' end
    local strandBonus=(d.strands-1)*d.contribution
    -- Infer installed tape contribution from the authoritative maximum; never use a new sandbox value.
    local tapeBonus=d.maximum-d.contribution*d.strands
    local lines={text('RetainerTitle'),text('InactiveProtection'),text('Material',getItemNameFromFullType(d.material)),
        text('Condition',text(condition)),text('Durability',d.current,d.maximum)}
    local barAfter=#lines
    if strandBonus>0 or d.tape then
        lines[#lines+1]=text('Modifiers')
        if strandBonus>0 then lines[#lines+1]=text('StrandModifier',d.strands,strandBonus) end
        if d.tape then lines[#lines+1]=text('TapeModifier',getItemNameFromFullType(d.tape),tapeBonus) end
    end
    lines[#lines+1]=text('BaseDurability',d.contribution)
    lines[#lines+1]=text('MaximumDurability',d.maximum)
    return {lines=lines,barAfter=barAfter,ratio=ratio,percent=math.floor(ratio*100+0.5),
        current=d.current,maximum=d.maximum,base=d.contribution,strandBonus=strandBonus,tapeBonus=tapeBonus}
end
-- Wrap by UTF-8 characters, including long single-word translations.
function P.wrap(line,width,measure)
    local rows,current={},''
    for character in line:gmatch('[%z\1-\127\194-\244][\128-\191]*') do
        if current~='' and measure(current..character)>width then rows[#rows+1]=current;current='' end
        current=current..character
    end
    if current~='' then rows[#rows+1]=current end
    return rows
end
function P.position(x,y,w,h,pw,ph,sw,sh)
    if pw>sw or ph>sh or pw<=0 or ph<=0 then return nil end
    if y+h+ph+4<=sh then return math.max(0,math.min(x,sw-pw)),y+h+4 end
    if x+w+pw+4<=sw then return x+w+4,math.max(0,math.min(y,sh-ph)) end
    if x-pw-4>=0 then return x-pw-4,math.max(0,math.min(y,sh-ph)) end
    if y-ph-4>=0 then return math.max(0,math.min(x,sw-pw)),y-ph-4 end
    return nil -- No non-overlapping placement: leave vanilla intact.
end
return P

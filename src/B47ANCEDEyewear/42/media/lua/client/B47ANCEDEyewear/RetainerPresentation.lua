-- Read-only projection of replicated item metadata. Never migrates or repairs state.
local R=require 'B47ANCEDEyewear/RetainerState'
local P={}
local function text(key,...) return getText('UI_B47ANCEDEyewear_'..key,...) end
local function finite(n) return type(n)=='number' and n==n and n>-math.huge and n<math.huge end
local function whole(n,lo,hi) return finite(n) and n==math.floor(n) and n>=lo and n<=hi end
local function unknown() return {unavailable=true,lines={text('RetainerTitle'),text('Unavailable')}} end
function P.model(item)
    if not item or not item:hasModData() then return nil end
    local S=B47ANCEDEyewear
    local tied=S and S.state and S.state(item)
    if tied and tied.tied then
        if type(tied.material)~='string' then return unknown() end
        return {lines={text('RetainerTitle'),text('Material',getItemNameFromFullType(tied.material)),
            text('Condition',text('Secure')),text('TiedAttachment')}}
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

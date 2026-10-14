-- Read-only compatibility reader for retired schema-2 records. No gameplay authority.
local R={key='B47ANCEDEyewearRetainer',schema=2}
local layers={['Base.RubberBand']=1,['Base.Thread']=3,['Base.DentalFloss']=3,
    ['Base.RippedSheets']=1,['Base.DenimStrips']=1,['Base.Twine']=1,['Base.Thread_Sinew']=3,
    ['Base.LeatherStrips']=1,['Base.FishingLine']=3,['Base.ElectricWire']=1,['Base.Wire']=1,
    ['Base.PremiumFishingLine']=3,['Base.Zipties']=1,['Base.Thread_Aramid']=3}
local tape={['Base.Scotchtape']=1,['Base.DuctTape']=2}
local function whole(n,low,high)
    return type(n)=='number' and n==n and n>=low and n<=high and n==math.floor(n)
end
function R.compatible(item)
    local S=B47ANCEDEyewear
    return S and S.isGlasses and S.isGlasses(item) and not S.isMonocle(item)
end
function R.state(item)
    if not item or not item:hasModData() then return nil end
    local d=item:getModData()[R.key]
    if type(d)~='table' or d.schema~=2 or d.kind~='makeshift' or not layers[d.material]
        or not whole(d.revision,0,2147483646) or not whole(d.maximum,1,1000)
        or not whole(d.current,0,d.maximum) or not whole(d.strands,1,layers[d.material])
        or not whole(d.contribution,1,160) or (d.tape and not tape[d.tape])
        or (d.material=='Base.Zipties' and d.tape)
        or d.maximum~=d.contribution*d.strands+(tape[d.tape] or 0) then return nil end
    return d
end
return R

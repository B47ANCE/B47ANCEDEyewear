-- Build 42 runs this entry point before loading item scripts.
local name = 'b47ancedeyewear:retainer'
if not ItemBodyLocation.get(ResourceLocation.of(name)) then
    ItemBodyLocation.register(name)
end

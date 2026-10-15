-- Build 42 runs this entry point before loading item scripts.
for _, name in ipairs({'retainer', 'tieeyes', 'tieface', 'tiehat'}) do
    name = 'b47ancedeyewear:' .. name
    if not ItemBodyLocation.get(ResourceLocation.of(name)) then
        ItemBodyLocation.register(name)
    end
end

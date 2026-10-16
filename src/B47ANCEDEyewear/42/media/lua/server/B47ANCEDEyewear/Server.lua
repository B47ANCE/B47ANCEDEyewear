local S=require 'B47ANCEDEyewear/Core'
local Server={}
local function itemById(player,id)
    if not player or type(id)~='number' or id~=id or id< -2147483648 or id>2147483647
        or id~=math.floor(id) then return nil end
    local inventory=player:getInventory()
    if not inventory then return nil end
    local ok,item=pcall(inventory.getItemById,inventory,id)
    return ok and item or nil
end
function Server.onClientCommand(module,command,player,args)
    if module~='B47ANCEDEyewear' or type(args)~='table' or not player then return false end
    if isClient() or (command~='Tie' and command~='Untie' and command~='Reinforce' and command~='Tape') then return false end
    local item=itemById(player,args.itemId)
    if not S.matchesRequest(player,item,args) then return false end
    if command=='Untie' then return S.untie(player,item,itemById(player,args.toolId)) end
    if command=='Reinforce' or command=='Tape' then
        return S.reinforce(player,item,itemById(player,args.materialId),command=='Tape')
    end
    return S.tie(player,item,itemById(player,args.materialId))
end
if Events and Events.OnClientCommand then Events.OnClientCommand.Add(Server.onClientCommand) end
B47ANCEDEyewear.Server=Server
return Server

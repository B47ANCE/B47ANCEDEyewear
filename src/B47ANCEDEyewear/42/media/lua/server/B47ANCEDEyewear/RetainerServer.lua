local R=require 'B47ANCEDEyewear/Retainers'
local operations={Install=R.install,Reinforce=R.reinforce,Tape=R.applyTape,Remove=R.remove}
local function resolve(player,id)
    if type(id)~='number' or id~=math.floor(id) then return nil end
    return player:getInventory():getItemById(id)
end
function R.onClientCommand(module,command,player,args)
    if module~='B47ANCEDEyewear' or command~='Retainer' or type(args)~='table' or not player then return false end
    local action=operations[args.operation]
    if not action or type(args.revision)~='number' then return false end
    local item=resolve(player,args.itemId);if not item then return false end
    if args.operation=='Remove' then return R.remove(player,item,args.revision,resolve(player,args.toolId)) end
    return action(player,item,resolve(player,args.materialId),args.revision)
end
if Events.OnClientCommand then Events.OnClientCommand.Add(R.onClientCommand) end
return R

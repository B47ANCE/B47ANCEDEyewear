local S = require 'B47ANCEDEyewear/Core'

local Server = {}
local MODULE, COMMAND = 'B47ANCEDEyewear', 'Tie'

local function itemById(player, id)
    if not player or type(player.getInventory) ~= 'function' then return nil end
    local inventory = player:getInventory()
    if not inventory or type(inventory.getItemById) ~= 'function' then return nil end
    local numeric = tonumber(id)
    if not numeric then return nil end
    local ok, item = pcall(inventory.getItemById, inventory, numeric)
    return ok and item or nil
end

function Server.onClientCommand(module, command, player, args)
    if module ~= MODULE or command ~= COMMAND or type(args) ~= 'table' then return false end
    local headwear, material = itemById(player, args.itemId), itemById(player, args.materialId)
    return S.tie(player, headwear, material)
end

if Events and Events.OnClientCommand then Events.OnClientCommand.Add(Server.onClientCommand) end
B47ANCEDEyewear = B47ANCEDEyewear or {}
B47ANCEDEyewear.Server = Server
return Server

-- Vanilla timed-action completion is authoritative on the server/SP.
if isClient() then return end
require 'TimedActions/ISWearClothing'
require 'TimedActions/ISUnequipAction'
local S = require 'B47ANCEDEyewear/Core'
local function wrap(action)
    if action.B47ANCEDEyewearRefresh then return end
    action.B47ANCEDEyewearRefresh = true
    local complete = action.complete
    function action:complete()
        local result = complete(self)
        if result then S.refresh(self.character) end
        return result
    end
end
wrap(ISWearClothing)
wrap(ISUnequipAction)

-- Bounded dedicated fallback for reconnects, config changes and external moves.
-- Do not depend on local-player clothing notifications on a headless server.
if isServer() then
    local ticks = 0
    Events.OnTick.Add(function()
        ticks = ticks + 1
        if ticks < 30 then return end
        ticks = 0
        local players = getOnlinePlayers()
        if not players then return end
        for index = 0, players:size() - 1 do S.refresh(players:get(index)) end
    end)
end

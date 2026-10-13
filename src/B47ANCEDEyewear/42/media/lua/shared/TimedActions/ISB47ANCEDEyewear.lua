require 'TimedActions/ISBaseTimedAction'
local S = require 'B47ANCEDEyewear/Core'
ISB47ANCEDEyewear = ISBaseTimedAction:derive('ISB47ANCEDEyewear')

function ISB47ANCEDEyewear:isValid()
    -- The server can sync consumption/tie state before the client animation ends.
    -- Keep presentation alive; complete() always performs strict authority checks.
    if isClient() and self.started then
        return self.character ~= nil and not self.character:isDead()
            and self.glasses ~= nil and self.character:isEquippedClothing(self.glasses)
    end
    return S.valid(self.character, self.glasses, self.material, self.untie)
end

function ISB47ANCEDEyewear:start()
    if isClient() then
        local inventory = self.character:getInventory()
        if self.glasses then self.glasses = inventory:getItemById(self.glasses:getID()) end
        if self.material then self.material = inventory:getItemById(self.material:getID()) end
    end
    if not self.glasses then return end
    self.started = true
    self:setActionAnim('SewingCloth')
end

function ISB47ANCEDEyewear:stop()
    self.started = false
    ISBaseTimedAction.stop(self)
end

function ISB47ANCEDEyewear:perform()
    self.started = false
    if not self.submitted then
        self.submitted = true
        if isClient() and not self.untie and self.glasses and self.material
            and type(sendClientCommand) == 'function'
            and type(self.glasses.getID) == 'function' and type(self.material.getID) == 'function' then
            sendClientCommand(self.character, 'B47ANCEDEyewear', 'Tie', {
                itemId = self.glasses:getID(), materialId = self.material:getID()
            })
        elseif not isClient() then
            self:complete()
        end
    end
    ISBaseTimedAction.perform(self)
end

function ISB47ANCEDEyewear:complete()
    if isClient() then return false end
    if self.untie then return S.untie(self.character, self.glasses) end
    return S.tie(self.character, self.glasses, self.material)
end

function ISB47ANCEDEyewear:getDuration()
    if not self.character or not self.glasses then return 0 end
    return self.character:isTimedActionInstant() and 1 or 80
end

function ISB47ANCEDEyewear:new(character, glasses, material, untie)
    local o = ISBaseTimedAction.new(self, character)
    o.glasses, o.material, o.untie = glasses, material, untie == true
    o.stopOnWalk, o.stopOnRun = true, true
    o.maxTime = o:getDuration()
    return o
end

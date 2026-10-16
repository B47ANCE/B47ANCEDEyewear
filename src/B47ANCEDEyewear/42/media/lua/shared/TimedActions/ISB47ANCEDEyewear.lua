require 'TimedActions/ISBaseTimedAction'
local S = require 'B47ANCEDEyewear/Core'
ISB47ANCEDEyewear = ISBaseTimedAction:derive('ISB47ANCEDEyewear')

local function expected(action)
    return {tieId=action.expectedTieId,revision=action.expectedRevision,tied=action.expectedTied}
end

function ISB47ANCEDEyewear:isValid()
    -- The server can sync consumption/tie state before the client animation ends.
    -- Keep presentation alive; complete() always performs strict authority checks.
    if isClient() and self.started then
        if not self.character or self.character:isDead() or not self.glasses then return false end
        if self.operation=='RetainerTape' then
            local inventory = self.character:getInventory()
            return self.glasses:getContainer()==inventory and inventory:contains(self.glasses)
        end
        return self.character:isEquippedClothing(self.glasses)
    end
    return S.matchesRequest(self.character,self.glasses,expected(self))
        and S.validAction(self.character,self.glasses,self.material,self.operation,self.tool)
end

function ISB47ANCEDEyewear:start()
    if isClient() then
        local inventory = self.character:getInventory()
        if self.glasses then self.glasses = inventory:getItemById(self.glasses:getID()) end
        if self.material then self.material = inventory:getItemById(self.material:getID()) end
        if self.tool then self.tool = inventory:getItemById(self.tool:getID()) end
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
        if isClient() and self.glasses
            and type(sendClientCommand)=='function' then
            sendClientCommand(self.character,'B47ANCEDEyewear',self.operation,{
                itemId=self.glasses:getID(),materialId=self.material and self.material:getID(),
                toolId=self.tool and self.tool:getID(),tieId=self.expectedTieId,
                revision=self.expectedRevision,tied=self.expectedTied
            })
        elseif not isClient() then
            self:complete()
        end
    end
    ISBaseTimedAction.perform(self)
end

function ISB47ANCEDEyewear:complete()
    -- Multiplayer commits travel only through validated server commands.
    if isServer() then return true end -- Completion acknowledgement only; command handler owns MP mutation.
    if isClient() or self.completed then return false end
    self.completed=true
    if not S.matchesRequest(self.character,self.glasses,expected(self)) then return false end
    if self.operation=='RetainerTape' then
        return S.RetainerItems.applyTape(self.character,self.glasses,self.material)
    end
    if self.operation=='Untie' then return S.untie(self.character, self.glasses, self.tool) end
    if self.operation=='Reinforce' or self.operation=='Tape' then
        return S.reinforce(self.character,self.glasses,self.material,self.operation=='Tape')
    end
    if self.operation=='Tie' then return S.tie(self.character, self.glasses, self.material) end
    return false
end

function ISB47ANCEDEyewear:getDuration()
    if not self.character or not self.glasses then return 0 end
    return self.character:isTimedActionInstant() and 1 or 80
end

function ISB47ANCEDEyewear:new(character, glasses, material, untie, operation, tool)
    local o = ISBaseTimedAction.new(self, character)
    o.glasses, o.material, o.untie = glasses, material, untie == true
    o.operation = operation or (o.untie and 'Untie' or 'Tie')
    o.tool = tool
    local snapshot = S.snapshot(character,glasses)
    o.expectedTieId, o.expectedRevision, o.expectedTied = snapshot.tieId, snapshot.revision, snapshot.tied
    o.stopOnWalk, o.stopOnRun = true, true
    o.maxTime = o:getDuration()
    return o
end

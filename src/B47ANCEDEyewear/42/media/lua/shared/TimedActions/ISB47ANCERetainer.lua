require 'TimedActions/ISBaseTimedAction'
local R=require 'B47ANCEDEyewear/Retainers'
ISB47ANCERetainer=ISBaseTimedAction:derive('ISB47ANCERetainer')
function ISB47ANCERetainer:isValid()
    local d=R.state(self.glasses)
    return R.validOwner(self.character,self.glasses) and (d and d.revision or 0)==self.revision
        and (not self.material or self.material:getContainer()==self.character:getInventory())
end
function ISB47ANCERetainer:start() self:setActionAnim('SewingCloth') end
function ISB47ANCERetainer:perform()
    if not self.submitted and self:isValid() then
        self.submitted=true
        if isClient() then
            sendClientCommand(self.character,'B47ANCEDEyewear','Retainer',{operation=self.operation,
                itemId=self.glasses:getID(),materialId=self.material and self.material:getID(),
                toolId=self.operation=='Remove' and self.material and self.material:getID(),revision=self.revision})
        else self:complete() end
    end
    ISBaseTimedAction.perform(self)
end
function ISB47ANCERetainer:complete()
    if isClient() or self.committed then return false end
    self.committed=true
    if self.operation=='Remove' then return R.remove(self.character,self.glasses,self.revision,self.material) end
    local action=({Install=R.install,Reinforce=R.reinforce,Tape=R.applyTape})[self.operation]
    return action and action(self.character,self.glasses,self.material,self.revision) or false
end
function ISB47ANCERetainer:getDuration() return self.character:isTimedActionInstant() and 1 or 80 end
function ISB47ANCERetainer:new(character,glasses,material,operation)
    local o=ISBaseTimedAction.new(self,character)
    o.glasses,o.material,o.operation=glasses,material,operation
    local d=R.state(glasses);o.revision=d and d.revision or 0
    o.stopOnWalk,o.stopOnRun=true,true;o.maxTime=o:getDuration();return o
end

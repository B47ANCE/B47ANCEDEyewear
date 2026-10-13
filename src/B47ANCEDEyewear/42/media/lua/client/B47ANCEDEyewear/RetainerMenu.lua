require 'TimedActions/ISTimedActionQueue'
require 'TimedActions/ISB47ANCERetainer'
local R=require 'B47ANCEDEyewear/Retainers'
local function queue(character,item,material,operation)
    ISTimedActionQueue.add(ISB47ANCERetainer:new(character,item,material,operation))
end
local function selected(raw)
    local items={}
    if raw and type(raw.size)=='function' then for i=0,raw:size()-1 do items[#items+1]=raw:get(i) end
    elseif type(raw)=='table' then items=raw end
    return items
end
local function tooltip(text)
    local t=ISWorldObjectContextMenu.addToolTip();t.description=text;return t
end
local function fill(index,context,raw)
    local player=getSpecificPlayer(index);if not player or player:isDead() then return end
    for _,entry in ipairs(selected(raw)) do
        local item=entry
        if type(entry)=='table' and entry.items then item=entry.items[1] end
        if R.validOwner(player,item) and (R.available() or R.state(item)) then
            local owner=context:getOptionFromName(item:getName())
            local itemMenu=owner and owner.subOption and context:getSubMenu(owner.subOption)
            if not itemMenu then
                owner=owner or context:addOption(item:getName(),item,nil)
                itemMenu=ISContextMenu:getNew(context);context:addSubMenu(owner,itemMenu)
            end
            if itemMenu:getOptionFromName(getText('ContextMenu_B47ANCEDEyewear_Retainer')) then return end
            local top=itemMenu:addOption(getText('ContextMenu_B47ANCEDEyewear_Retainer'),item,nil)
            local menu=ISContextMenu:getNew(itemMenu);itemMenu:addSubMenu(top,menu)
            local d=R.active(item)
            if d then
                top.toolTip=tooltip(R.describe(item))
                if d.material~='Base.Zipties' then menu:addOption(getText('ContextMenu_B47ANCEDEyewear_RemoveRetainer'),player,queue,item,nil,'Remove')
                else
                    local tools=player:getInventory():getItems();local cutMenu
                    for i=0,tools:size()-1 do local tool=tools:get(i)
                        if R.cuttingTool(player,tool) then
                            if not cutMenu then
                                local cut=menu:addOption(getText('ContextMenu_B47ANCEDEyewear_CutRetainer'),item,nil)
                                cutMenu=ISContextMenu:getNew(menu);menu:addSubMenu(cut,cutMenu)
                            end
                            cutMenu:addOption(tool:getName(),player,queue,item,tool,'Remove')
                        end
                    end
                end
            end
            if R.available() and R.options().enabled then
                local inventory=player:getInventory():getItems()
                local options={}
                for i=0,inventory:size()-1 do
                    local material=inventory:get(i);local kind=material:getFullType()
                    if not instanceof(material,'DrainableComboItem') or material:getCurrentUses()>=1 then
                        local operation,label
                        if not d and R.materials[kind] then operation='Install';label='ContextMenu_B47ANCEDEyewear_MakeRetainer'
                        elseif d and kind==d.material and d.strands<R.materials[kind].layers then operation='Reinforce';label='ContextMenu_B47ANCEDEyewear_ReinforceRetainer'
                        elseif d and not d.tape and not R.materials[d.material].noTape and R.tapes[kind] then operation='Tape';label='ContextMenu_B47ANCEDEyewear_TapeRetainer' end
                        if operation then
                            if not options[operation] then
                                local o=menu:addOption(getText(label),item,nil)
                                options[operation]=ISContextMenu:getNew(menu);menu:addSubMenu(o,options[operation])
                            end
                            options[operation]:addOption(material:getName(),player,queue,item,material,operation)
                        end
                    end
                end
            end
            return
        end
    end
end
if Events.OnFillInventoryObjectContextMenu then Events.OnFillInventoryObjectContextMenu.Add(fill) end
return R

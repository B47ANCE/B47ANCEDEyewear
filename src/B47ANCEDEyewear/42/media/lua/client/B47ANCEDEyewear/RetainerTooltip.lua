require 'ISUI/ISToolTipInv'
require 'ISUI/ISPanel'
local P=require 'B47ANCEDEyewear/RetainerPresentation'
local Panel=ISPanel:derive('ISB47ANCERetainerTooltip')
function Panel:prerender()
    if not self.owner:isReallyVisible() then
        self:setVisible(false);self:removeFromUIManager();self.owner.b47ancePanel=nil
    elseif ISContextMenu.instance and ISContextMenu.instance.visibleCheck then self:setVisible(false) end
end
function Panel:onMouseDown() return false end
function Panel:onMouseUp() return false end
function Panel:onRightMouseDown() return false end
function Panel:onRightMouseUp() return false end
function Panel:render()
    if not self.model then return end
    self:drawRect(0,0,self.width,self.height,0.95,0.05,0.05,0.05)
    self:drawRectBorder(0,0,self.width,self.height,1,0.4,0.4,0.4)
    local y=8
    for _,row in ipairs(self.rows) do
        if row.bar then
            self:drawRect(8,y,self.width-16,self.lineHeight,1,0.2,0.2,0.2)
            self:drawRect(8,y,(self.width-16)*self.model.ratio,self.lineHeight,1,
                1-self.model.ratio,self.model.ratio,0.15)
            self:drawTextCentre(tostring(self.model.percent)..'%',self.width/2,y,1,1,1,1,UIFont.Small)
        else self:drawText(row.text,8,y,1,1,1,1,UIFont.Small) end
        y=y+self.lineHeight
    end
end
local previous=ISToolTipInv.render
if not ISToolTipInv.B47ANCERetainerWrapped then
    ISToolTipInv.B47ANCERetainerWrapped=true
    function ISToolTipInv:render(...)
        if self.b47ancePanel then self.b47ancePanel:setVisible(false) end
        local result=previous(self,...)
        if ISContextMenu.instance and ISContextMenu.instance.visibleCheck then return result end
        local ok,model=pcall(P.model,self.item)
        if not ok or not model then return result end
        if model.unavailable and not self.b47anceInvalidReported then
            self.b47anceInvalidReported=true
            print('[B47ANCEDEyewear][Tooltip] Invalid or unavailable retainer metadata; read-only fallback.')
        end
        local core=getCore();local sw,sh=core:getScreenWidth(),core:getScreenHeight()
        local tm=getTextManager();local lh=tm:getFontHeight(UIFont.Small)+2
        local width=math.min(sw,math.max(220,tm:MeasureStringX(UIFont.Small,model.lines[1])+16))
        local rows={}
        for i,line in ipairs(model.lines) do
            for _,row in ipairs(P.wrap(line,width-16,function(s) return tm:MeasureStringX(UIFont.Small,s) end)) do
                rows[#rows+1]={text=row}
            end
            if i==model.barAfter then rows[#rows+1]={bar=true} end
        end
        local height=16+#rows*lh
        local x,y=P.position(self:getX(),self:getY(),self:getWidth(),self:getHeight(),width,height,sw,sh)
        if not x then return result end
        if not self.b47ancePanel then
            local panel=Panel:new(x,y,width,height);panel.owner=self;panel:initialise()
            panel:instantiate();panel:addToUIManager();self.b47ancePanel=panel
        end
        local panel=self.b47ancePanel
        panel.model,panel.rows,panel.lineHeight=model,rows,lh
        panel:setX(x);panel:setY(y);panel:setWidth(width);panel:setHeight(height);panel:setVisible(true)
        return result
    end
end
return P

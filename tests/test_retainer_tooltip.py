import json
import unittest
import test_glasses


class TooltipTests(unittest.TestCase):
    def setUp(self):
        fixture=test_glasses.GlassesTests();fixture.setUp();self.lua=fixture.lua
        path=str(test_glasses.ROOT/'client/?.lua').replace('\\','/')
        self.lua.execute('package.path='+repr(path)+"..';'..package.path")
        self.lua.execute('''
            function getText(key,...)
                local t={key};for _,v in ipairs({...}) do t[#t+1]=tostring(v) end
                return table.concat(t,'|')
            end
            function getItemNameFromFullType(kind) return kind end
            P=require 'B47ANCEDEyewear/RetainerPresentation'
            d={schema=2,kind='makeshift',material='Base.DentalFloss',strands=3,
                contribution=2,current=4,maximum=8,tape='Base.DuctTape',revision=3}
            g.data.B47ANCEDEyewearRetainer=d
        ''')

    def test_percent_and_real_modifiers_without_mutation(self):
        self.lua.execute('''local v=P.model(g)
            assert(v.ratio==0.5 and v.percent==50 and v.strandBonus==4 and v.tapeBonus==2)
            assert(v.maximum==8 and v.base==2 and d.current==4 and d.revision==3)
            assert(g.data.B47ANCEDEyewearRetainer==d)
            assert(v.lines[3]:find('Fraying'))
        ''')

    def test_snapshot_contribution_and_reinforcement_not_repair(self):
        self.lua.execute('''d.material='Base.FishingLine';d.contribution=7;d.maximum=23;d.current=11
            SandboxVars={B47ANCEDEyewear={RetainerDurabilityMultiplier=10}}
            local v=P.model(g);assert(v.base==7 and v.strandBonus==14 and v.tapeBonus==2)
            assert(v.current==11 and d.current==11 and v.maximum==23)
        ''')

    def test_conditions_and_broken_are_live(self):
        self.lua.execute('''for _,entry in ipairs({{8,'Secure'},{6,'Worn'},{4,'Fraying'},{2,'AboutToBreak'},{0,'Broken'}}) do
            d.current=entry[1];assert(P.model(g).lines[3]:find(entry[2])) end
            d.material='Base.RubberBand';d.strands=1;d.maximum=4;d.current=2
            assert(P.model(g).lines[3]:find('Stretched'))
        ''')

    def test_single_strand_without_tape_has_no_modifiers(self):
        self.lua.execute('''d.strands=1;d.tape=nil;d.maximum=2;d.current=1
            local v=P.model(g);assert(#v.lines==6 and v.strandBonus==0 and v.tapeBonus==0)
        ''')

    def test_permanent_is_distinct_and_inconsistent_data_unavailable(self):
        self.lua.execute('''g.data.B47ANCEDEyewearRetainer={schema=2,kind='permanent',permanent=true,
            material='B47ANCEDEyewear.EyewearRetainer',revision=1}
            local v=P.model(g);assert(v.permanent and not v.barAfter and not v.maximum)
            g.data.B47ANCEDEyewearRetainer.current=999
            assert(P.model(g).unavailable)
        ''')

    def test_missing_and_malformed_never_mutate(self):
        self.lua.execute('''g.data={};assert(P.model(g)==nil)
            for _,bad in ipairs({false,'bad',{schema=2,kind='makeshift',material='unknown'}}) do
                g.data.B47ANCEDEyewearRetainer=bad;assert(P.model(g).unavailable)
                assert(g.data.B47ANCEDEyewearRetainer==bad)
            end
        ''')

    def test_wrapping_and_placement(self):
        self.lua.execute('''local rows=P.wrap('Dental Floss ×3',5,string.len)
            assert(table.concat(rows)=='Dental Floss ×3')
            for _,row in ipairs(rows) do assert(#row<=5) end
            local x,y=P.position(700,650,100,80,220,250,1024,768)
            assert(x>=0 and y>=0 and x+220<=1024 and y+250<=768)
            assert(P.position(0,0,100,100,200,200,100,100)==nil)
        ''')

    def test_all_languages_and_placeholders_match(self):
        root=test_glasses.ROOT/'shared/Translate'
        en=json.loads((root/'EN/UI.json').read_text(encoding='utf-8'))
        folders=list(root.glob('*/UI.json'));self.assertEqual(len(folders),29)
        for path in folders:
            translated=json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(set(translated),set(en),path)
            for key,value in en.items():
                import re
                self.assertEqual(re.findall(r'%\d',value),re.findall(r'%\d',translated[key]),(path,key))

    def test_renderer_chains_vanilla_and_refreshes_only_current_item(self):
        self.lua.execute('''
            ISPanel={};function ISPanel:derive() local t={};t.__index=t;return setmetatable(t,{__index=self}) end
            function ISPanel:new(x,y,w,h) local t=setmetatable({x=x,y=y,width=w,height=h},self);self.__index=self;return t end
            function ISPanel:initialise() end;function ISPanel:instantiate() end;function ISPanel:addToUIManager() end
            function ISPanel:setVisible(v) self.visible=v end
            function ISPanel:setX(v) self.x=v end;function ISPanel:setY(v) self.y=v end
            function ISPanel:setWidth(v) self.width=v end;function ISPanel:setHeight(v) self.height=v end
            package.preload['ISUI/ISPanel']=function() return ISPanel end
            ISToolTipInv={render=function(self) self.vanillaCalls=(self.vanillaCalls or 0)+1;return 'vanilla' end}
            package.preload['ISUI/ISToolTipInv']=function() return ISToolTipInv end
            ISContextMenu={};UIFont={Small=1}
            function getCore() return {getScreenWidth=function() return 1024 end,getScreenHeight=function() return 768 end} end
            function getTextManager() return {getFontHeight=function() return 14 end,
                MeasureStringX=function(_,font,s) return #s*6 end} end
            require 'B47ANCEDEyewear/RetainerTooltip'
            local tip=setmetatable({item=g,getX=function() return 10 end,getY=function() return 10 end,
                getWidth=function() return 100 end,getHeight=function() return 100 end},{__index=ISToolTipInv})
            assert(tip:render()=='vanilla');assert(tip.vanillaCalls==1 and tip.b47ancePanel.visible)
            d.current=1;tip:render();assert(tip.b47ancePanel.model.current==1)
            g.data={};tip:render();assert(not tip.b47ancePanel.visible and tip.vanillaCalls==3)
        ''')

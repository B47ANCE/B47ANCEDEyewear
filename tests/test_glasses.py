from pathlib import Path
import json
import re
import unittest
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[1] / 'src/B47ANCEDEyewear/42/media/lua'


class GlassesTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('''
            Events = setmetatable({}, {__index=function(t,k)
                local e={Add=function(f) end}; rawset(t,k,e); return e end})
            function instanceof(o,c) return type(o)=='table' and o.class==c end
            function isClient() return false end
            function syncItemModData() syncs=syncs+1 end
            syncs=0
            ItemBodyLocation={EYES='base:eyes',FACE='base:face'}
            ISBaseTimedAction={}
            function ISBaseTimedAction:derive() local c={}; c.__index=c
                return setmetatable(c,{__index=self}) end
            function ISBaseTimedAction.new(c,p) return setmetatable({character=p},c) end
            function ISBaseTimedAction.perform() end
            function ISBaseTimedAction.stop() end
            function ISBaseTimedAction:setActionAnim() end
            package.preload['TimedActions/ISBaseTimedAction']=function() return ISBaseTimedAction end
            function makeItem(kind, class)
                local o={kind=kind,class=class or 'Clothing',chance=50,data={},uses=2,name='Prescription Glasses'}
                function o:getFullType() return self.kind end
                function o:getName() return self.name end
                function o:setName(name) self.name=name end
                function o:isCustomName() return self.customName or false end
                function o:setCustomName(value) self.customName=value end
                function o:getBodyLocation() return self.location or 'base:eyes' end
                function o:getChanceToFall() return self.chance end
                function o:setChanceToFall(v) self.chance=v end
                function o:hasModData() return next(self.data)~=nil end
                function o:getModData() return self.data end
                function o:getCurrentUses() return self.uses end
                function o:isBroken() return self.broken or false end
                function o:UseAndSync() self.uses=self.uses-1 end
                return o
            end
            g=makeItem('Base.Glasses_Prescription')
            m=makeItem('Base.Twine','DrainableComboItem')
            inv={}
            function inv:contains(i) return (i==g and not missingGlasses) or (i==m and not missingMaterial) end
            worn={size=function() return 1 end,get=function() return {getItem=function() return g end} end}
            p={getInventory=function() return inv end,isDead=function() return dead or false end,
                isEquippedClothing=function(_,i) return i==g and not unworn end,
                isTimedActionInstant=function() return false end,getWornItems=function() return worn end}
        ''')
        self.lua.execute("package.path = " + repr(str(ROOT / 'shared/?.lua').replace('\\', '/')) + " .. ';' .. package.path")
        self.lua.execute((ROOT / 'shared/TimedActions/ISB47ANCEDEyewear.lua').read_text())

    def run_lua(self, code):
        self.lua.execute(code)

    def test_tie_preserves_identity_consumes_once(self):
        self.run_lua('''local original=g
            local a=ISB47ANCEDEyewear:new(p,g,m,false)
            assert(a:complete()); assert(g==original and g.chance==0 and m.uses==1)
            assert(g.name=='Prescription Glasses (Tied)' and g.customName)
            assert(not a:complete()); assert(m.uses==1 and syncs==1)
        ''')

    def test_untie_restore_no_refund_and_retie(self):
        self.run_lua('''assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
            local a=ISB47ANCEDEyewear:new(p,g,nil,true)
            assert(a:complete()); assert(g.chance==10 and m.uses==1)
            assert(not a:complete()); assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
            assert(g.chance==0 and m.uses==0 and g.name=='Prescription Glasses (Tied)')
        ''')

    def test_monocles_are_unsupported_and_migrate_obsolete_tied_state(self):
        self.run_lua('''
            for _,kind in ipairs({'Base.Glasses_MonocleLeft','Base.Glasses_MonocleRight',
                'Base.Glasses_Cosmetic_MonocleLeft','Base.Glasses_Cosmetic_MonocleRight'}) do
                local untied=makeItem(kind); untied.chance=15
                assert(B47ANCEDEyewear.isGlasses(untied))
                assert(not B47ANCEDEyewear.isTieable(untied))
                assert(not B47ANCEDEyewear.valid(p,untied,m,false))
                B47ANCEDEyewear.applyChance(untied,p)
                assert(untied.chance==70)
            end
            local monocle=makeItem('Base.Glasses_MonocleLeft')
            monocle.chance=0
            monocle.name='Prescription Monocle (Tied)'
            monocle.customName=true
            monocle.data.B47ANCEDEyewear={version=1,tied=true,original=50,
                material='Base.Twine',name='Prescription Monocle',customName=false}
            assert(B47ANCEDEyewear.isGlasses(monocle))
            assert(not B47ANCEDEyewear.isTieable(monocle))
            assert(not B47ANCEDEyewear.valid(p,monocle,m,false))
            B47ANCEDEyewear.applyChance(monocle,p)
            assert(monocle.chance==70 and monocle.data.B47ANCEDEyewear.retired)
            assert(monocle.name=='Prescription Monocle' and not monocle.customName)
            assert(m.uses==2)
        ''')

    def test_tie_renames_same_item_and_untie_restores_custom_name(self):
        self.run_lua('''
            g.name='Aviators'; g.customName=true
            local original=g
            assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
            assert(g==original and g.name=='Aviators (Tied)' and g.customName)
            assert(ISB47ANCEDEyewear:new(p,g,nil,true):complete())
            assert(g==original and g.name=='Aviators' and g.customName)
        ''')

    def test_reject_invalid_state_without_consumption(self):
        for flag in ['missingGlasses', 'missingMaterial', 'unworn', 'dead']:
            with self.subTest(flag=flag):
                self.run_lua(f'''{flag}=true
                    assert(not ISB47ANCEDEyewear:new(p,g,m,false):complete())
                    assert(g.chance==50 and m.uses==2); {flag}=false''')
        self.run_lua('''g.broken=true
            assert(not ISB47ANCEDEyewear:new(p,g,m,false):complete())
            assert(m.uses==2)''')

    def test_material_allowlist_and_empty_spool(self):
        self.run_lua('''for kind in pairs(B47ANCEDEyewear.materials) do
                assert(B47ANCEDEyewear.isMaterial(makeItem(kind,'DrainableComboItem'))) end
            assert(not B47ANCEDEyewear.isMaterial(makeItem('Base.Rope','InventoryItem')))
            m.uses=0; assert(not ISB47ANCEDEyewear:new(p,g,m,false):complete())
            assert(g.chance==50)
        ''')

    def test_excludes_unrelated_clothing(self):
        self.run_lua('''for _,kind in ipairs({'Base.Hat_BaseballCap','Base.Glasses_Eyepatch_Left','Other.Blindfold'}) do
                assert(not B47ANCEDEyewear.isGlasses(makeItem(kind))) end
            assert(not B47ANCEDEyewear.isGlasses(nil))
            assert(not B47ANCEDEyewear.isGlasses(makeItem('Base.Glasses','InventoryItem')))
        ''')

    def test_reading_glasses_in_face_slot_are_eligible(self):
        self.run_lua('''
            local reading=makeItem('Base.ReadingGlasses')
            reading.location='base:face'
            assert(B47ANCEDEyewear.isGlasses(reading))
            g=reading; m.uses=2
            assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
            assert(g.chance==0 and m.uses==1)
        ''')

    def test_face_slot_eyewear_without_glasses_in_its_type_is_eligible(self):
        self.run_lua('''
            local eyewear=makeItem('ExampleMod.AviatorVisor')
            eyewear.location='base:face'
            assert(B47ANCEDEyewear.isGlasses(eyewear))
            local faceMask=makeItem('ExampleMod.FaceMask')
            faceMask.location='base:face'
            assert(not B47ANCEDEyewear.isGlasses(faceMask))
        ''')

    def test_modded_eyewear_tie_restore(self):
        # These six identifiers/slots are shared by original and Faded 42.20.2.1.
        self.run_lua('''
            for _,kind in ipairs({'AuthenticZClothing.Glasses_AviatorsSunset',
                'AuthenticZClothing.Glasses_Cheese', 'AuthenticZClothing.Glasses_ReadingBlack',
                'AuthenticZClothing.Glasses_Popeyes', 'AuthenticZClothing.Glasses_AZ_Sunglasses1',
                'AuthenticZClothing.Glasses_AZ_Sunglasses2', 'TestMod.Custom_Glasses'}) do
                g=makeItem(kind); m.uses=2
                assert(B47ANCEDEyewear.isGlasses(g))
                assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
                assert(g.chance==0 and m.uses==1)
                g.chance=50; B47ANCEDEyewear.refresh(p); assert(g.chance==0)
                assert(ISB47ANCEDEyewear:new(p,g,nil,true):complete())
                assert(g.chance==15 and m.uses==1)
            end
            g.location='base:hat'; assert(not B47ANCEDEyewear.isGlasses(g))
            g.location='base:eyes'; g.class='InventoryItem'
            assert(not B47ANCEDEyewear.isGlasses(g))
        ''')

    def test_client_cannot_commit_and_tolerates_server_sync(self):
        self.run_lua('''
            function isClient() return true end
            local action=ISB47ANCEDEyewear:new(p,g,m,false)
            action.started=true
            assert(not action:complete()); assert(m.uses==2 and g.chance==50 and syncs==0)
            missingMaterial=true; g.data.B47ANCEDEyewear={version=1,tied=true,original=50}
            assert(action:isValid())
            unworn=true; assert(not action:isValid()); unworn=false
            action:stop(); assert(not action.started and not action:isValid())
        ''')

    def test_server_ignores_client_started_bypass(self):
        self.run_lua('''
            local action=ISB47ANCEDEyewear:new(p,g,m,false); action.started=true
            missingMaterial=true
            assert(not action:complete()); assert(m.uses==2 and g.chance==50)
            missingMaterial=false; missingGlasses=true
            assert(not action:complete()); assert(syncs==0)
        ''')

    def test_separate_peer_restore_and_untie(self):
        # Separate objects model deserialized item data, not shared Lua references.
        self.run_lua('''
            assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
            local serverItem=g
            g=makeItem(serverItem.kind)
            g.data.B47ANCEDEyewear={version=1,tied=true,original=50}
            B47ANCEDEyewear.refresh(p); assert(g.chance==0)
            local clientItem=g; g=serverItem
            assert(ISB47ANCEDEyewear:new(p,g,nil,true):complete())
            g=clientItem; g.data.B47ANCEDEyewear={version=1,tied=false,original=50}
            B47ANCEDEyewear.refresh(p); assert(g.chance==10)
        ''')

    def test_missing_client_item_start(self):
        self.run_lua('''
            function isClient() return true end
            function g:getID() return 1 end
            function m:getID() return 2 end
            function inv:getItemById() return nil end
            local action=ISB47ANCEDEyewear:new(p,g,m,false)
            action:start(); assert(not action:isValid())
            assert(not action:complete() and syncs==0)
        ''')

    def test_faded_accessories_are_not_glasses(self):
        self.run_lua('''
            for _,kind in ipairs({'AuthenticZClothing.ClownNose',
                'AuthenticZClothing.ClownNoseTINT', 'AuthenticZClothing.Hat_GasMask',
                'AuthenticZClothing.Hat_GasMask_nofilter', 'AuthenticZClothing.RaveMask'}) do
                g=makeItem(kind)
                assert(not B47ANCEDEyewear.isGlasses(g))
                assert(not ISB47ANCEDEyewear:new(p,g,m,false):complete())
                assert(m.uses==2 and g.chance==50)
            end
        ''')

    def test_load_and_remote_untie_restoration(self):
        self.run_lua('''assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
            g.chance=50; B47ANCEDEyewear.refresh(p); assert(g.chance==0)
            g.data.B47ANCEDEyewear.tied=false
            B47ANCEDEyewear.refresh(p); assert(g.chance==10)
            g.data.B47ANCEDEyewear={version=1,original='invalid',tied=true}
            B47ANCEDEyewear.refresh(p); assert(g.chance==10)
            B47ANCEDEyewear.refresh(nil)
        ''')

    def test_cancelled_action_does_not_mutate(self):
        self.run_lua('''ISB47ANCEDEyewear:new(p,g,m,false):stop()
            assert(g.chance==50 and m.uses==2 and syncs==0)''')

    def test_single_player_action_perform_commits_once(self):
        self.run_lua('''
            local action=ISB47ANCEDEyewear:new(p,g,m,false)
            action:perform()
            assert(g.chance==0 and m.uses==1 and syncs==1)
            action:perform()
            assert(m.uses==1 and syncs==1)
        ''')

    def test_all_lua_parses(self):
        parse = self.lua.eval('function(s) local f,e=load(s); assert(f,e) end')
        for path in ROOT.rglob('*.lua'):
            with self.subTest(path=path.name):
                parse(path.read_text())

    def test_test_kit_grants_supported_items_once_and_reports_missing_items(self):
        self.run_lua('''
            granted={}; kitData={}
            function inv:AddItem(kind)
                if kind=='AuthenticZClothing.Glasses_Cheese' then return nil end
                granted[#granted+1]=kind; return makeItem(kind)
            end
            p.getModData=function() return kitData end
            function getSpecificPlayer(index) if index==0 then return p end end
        ''')
        self.lua.execute((ROOT / 'client/B47ANCEDEyewear/TestKit.lua').read_text())
        self.run_lua('''
            local ok,result=B47ANCEDEyewearTestKit()
            assert(ok and result.granted==62 and #result.missing==1)
            local have={}; for _,kind in ipairs(granted) do have[kind]=true end
            assert(have['Base.Glasses_Prescription'] and have['Base.Hat_StrawHat'])
            assert(have['Base.Twine'] and have['Base.Thread_Sinew'])
            assert(B47ANCEDEyewearTestKit()==false and #granted==62)
            assert(B47ANCEDEyewearTestKit(true) and #granted==124)
            function isClient() return true end
            assert(B47ANCEDEyewearTestKit(true)==false and #granted==124)
        ''')

    def test_context_menu_lists_only_available_materials_and_queues_tie(self):
        self.run_lua('''
            queued=nil
            function getText(key)
                if key=='ContextMenu_B47ANCEDEyewear_Tie' then return 'Tie' end
                if key=='ContextMenu_B47ANCEDEyewear_Untie' then return 'Untie' end
                if key=='ContextMenu_B47ANCEDEyewear_NoMaterials' then return 'You do not have any materials to tie this with.' end
                return key
            end
            ISWorldObjectContextMenu={addToolTip=function()
                return {setVisible=function() end,addToUIManager=function() end,removeFromUIManager=function() end}
            end}
            ISTimedActionQueue={add=function(action) queued=action end}
            package.preload['TimedActions/ISTimedActionQueue']=function() return ISTimedActionQueue end
            package.preload['TimedActions/ISB47ANCEDEyewear']=function() return ISB47ANCEDEyewear end
            function menu()
                local value={options={}}
                function value:addOption(name,target,callback,...)
                    local option={name=name,target=target,onSelect=callback,args={...}}
                    self.options[#self.options+1]=option; return option
                end
                function value:addSubMenu(option,sub) option.subOption=sub end
                function value:getSubMenu(sub) return sub end
                function value:getOptionFromName(name)
                    for _,option in ipairs(self.options) do if option.name==name then return option end end
                end
                return value
            end
            ISContextMenu={getNew=function() return menu() end}
            function getSpecificPlayer(index) if index==0 then return p end end
            function inv:getItems() return {size=function() return 2 end,get=function(_,i) return i==0 and m or makeItem('Base.Rope') end} end
            p.getInventory=function() return inv end
        ''')
        self.lua.execute((ROOT / 'client/B47ANCEDEyewear/ContextMenu.lua').read_text())
        self.run_lua('''
            local javaItems={size=function() return 1 end,get=function(_, index) return index==0 and g or nil end}
            local context=menu(); local tie=B47ANCEDEyewear.Menu.add(p,context,javaItems)
            assert(tie and not tie.notAvailable and #tie.subOption.options==1)
            local material=tie.subOption.options[1]
            assert(material.name=='Prescription Glasses' or material.name=='Base.Twine')
            assert(material.onSelect(material.target,table.unpack(material.args)))
            assert(queued and queued.glasses==g and queued.material==m)
            function inv:getItems() return {size=function() return 0 end,get=function() end} end
            local empty=menu(); local disabled=B47ANCEDEyewear.Menu.add(0,empty,{g})
            assert(disabled.notAvailable and disabled.toolTip.description=='You do not have any materials to tie this with.')
            assert(type(disabled.toolTip.setVisible)=='function' and type(disabled.toolTip.addToUIManager)=='function')
            assert(disabled.subOption==nil)
            g.data.B47ANCEDEyewear={version=1,tied=true,original=50,name='Prescription Glasses',customName=false}
            local tiedMenu=menu(); local untie=B47ANCEDEyewear.Menu.add(0,tiedMenu,{g})
            assert(untie.name=='Untie' and untie.subOption==nil and not untie.notAvailable)
            queued=nil; assert(untie.onSelect(untie.target,table.unpack(untie.args)))
            assert(queued and queued.untie and queued.glasses==g and queued.material==nil)
        ''')

    def test_multiplayer_tie_command_is_server_authoritative(self):
        self.run_lua('''
            function g:getID() return 101 end; function m:getID() return 102 end
            function inv:getItemById(id) return id==101 and g or id==102 and m or nil end
            function inv:getItems() return {size=function() return 1 end,get=function() return m end} end
            function p:getModData() return {} end
            sent=nil; function sendClientCommand(player,module,command,args) sent={player,module,command,args} end
        ''')
        self.run_lua('''
            function isClient() return true end
            local action=ISB47ANCEDEyewear:new(p,g,m,false); action:perform()
            assert(sent[1]==p and sent[2]=='B47ANCEDEyewear' and sent[3]=='Tie')
            assert(sent[4].itemId==101 and sent[4].materialId==102)
        ''')
        self.lua.execute((ROOT / 'server/B47ANCEDEyewear/Server.lua').read_text())
        self.run_lua('''
            function isClient() return false end
            assert(B47ANCEDEyewear.Server.onClientCommand('B47ANCEDEyewear','Tie',p,{itemId=101,materialId=102}))
            assert(g.chance==0 and m.uses==1 and g.data.B47ANCEDEyewear.tied)
            assert(not B47ANCEDEyewear.Server.onClientCommand('B47ANCEDEyewear','Tie',p,{itemId=999,materialId=102}))
            assert(not B47ANCEDEyewear.Server.onClientCommand('other','Tie',p,{itemId=101,materialId=102}))
        ''')
    def test_crafting_callbacks_keep_the_selected_glasses_and_consume_material(self):
        self.run_lua('''
            local recipe={
                getCharacter=function() return p end,
                getAllInputItems=function() return {size=function() return 2 end,
                    get=function(_,i) return i==0 and g or m end} end,
                getAllConsumedItems=function() return {size=function() return 1 end,
                    get=function() return m end} end,
            }
            assert(B47ANCEDEyewear.onCraftTest(recipe))
            local original=g
            B47ANCEDEyewear.onCraftCreate(recipe)
            assert(g==original and g.chance==0 and g.data.B47ANCEDEyewear.tied and syncs==1)
            assert(not B47ANCEDEyewear.onCraftTest(recipe))
            assert(B47ANCEDEyewear.untie(p,g))
            assert(g.chance==10 and not g.data.B47ANCEDEyewear.tied and syncs==2)
        ''')

    def test_crafting_callbacks_reject_invalid_or_missing_inputs(self):
        self.run_lua('''
            local recipe={
                getCharacter=function() return p end,
                getAllInputItems=function() return {size=function() return 1 end,
                    get=function() return g end} end,
                getAllConsumedItems=function() return {size=function() return 1 end,
                    get=function() return m end} end,
            }
            missingMaterial=true; assert(not B47ANCEDEyewear.onCraftTest(recipe)); missingMaterial=false
            g.broken=true; assert(not B47ANCEDEyewear.onCraftTest(recipe)); g.broken=false
            assert(not B47ANCEDEyewear.onCraftTest({getCharacter=function() return p end}))
        ''')

    def test_client_crafting_callbacks_do_not_mutate(self):
        self.run_lua('''
            function isClient() return true end
            local recipe={
                getCharacter=function() return p end,
                getAllInputItems=function() return {size=function() return 1 end,
                    get=function() return g end} end,
                getAllConsumedItems=function() return {size=function() return 1 end,
                    get=function() return m end} end,
            }
            B47ANCEDEyewear.onCraftCreate(recipe)
            assert(g.chance==50 and syncs==0)
        ''')

    def test_crafting_recipe_lists_all_supported_identifiers(self):
        recipe = (ROOT.parents[0] / 'scripts/B47ANCEDEyewear_Crafting.txt').read_text()
        self.assertIn('craftRecipe TieGlasses', recipe)
        self.assertNotIn('craftRecipe UntieGlasses', recipe)
        self.assertIn('mode:keep,', recipe)
        self.assertNotIn('flags[Tieable]', recipe)
        self.assertIn('OnCreate = B47ANCEDEyewear.onCraftCreate', recipe)
        self.assertNotIn('OnTest = B47ANCEDEyewear.onCraftTest', recipe)
        for item in ('Base.Glasses_MonocleLeft', 'Base.Glasses_MonocleRight',
                     'Base.Glasses_Cosmetic_MonocleLeft', 'Base.Glasses_Cosmetic_MonocleRight'):
            self.assertNotIn(item, recipe)
        for item in ('Base.Glasses', 'Base.Glasses_Prescription',
                     'Base.Glasses_Novelty_Xray',
                     'AuthenticZClothing.Glasses_AviatorsSunset',
                     'AuthenticZClothing.Glasses_AZ_Sunglasses2',
                     'Base.Hat_StrawHat', 'Base.Hat_SummerHat'):
            self.assertEqual(len(re.findall(re.escape(item) + r'(?![A-Za-z0-9_])', recipe)), 1, item)

    def test_metadata_and_layout(self):
        project = ROOT.parents[4]
        info = (ROOT.parents[1] / 'mod.info').read_text()
        self.assertIn('id=B47ANCEDEyewear', info)
        self.assertNotIn('require=', info)
        self.assertTrue((project / 'src/B47ANCEDEyewear/common').is_dir())
        description = (project / 'WORKSHOP_DESCRIPTION.txt').read_bytes()
        self.assertLess(len(description), 8000)
        notes = (project / 'WORKSHOP_CHANGE_NOTE.txt').read_text(encoding='utf-8')
        version = (project / 'VERSION').read_text().strip()
        self.assertTrue(notes.startswith(f'[b]Version {version}[/b]'))
        self.assertIn(f'modversion={version}', info)
        self.assertIn("name=B47ANCE'd Eyewear", info)
        locales = ('AR','CA','CH','CN','CS','DA','DE','EN','ES','ES_CL','ES_MX','FI','FR','HU','ID','IT','JP','KO','NL','NO','PL','PT','PTBR','RO','RU','STREW','TH','TR','UA')
        translations = ROOT / 'shared/Translate'
        english_context = json.loads((translations / 'EN/ContextMenu.json').read_text(encoding='utf-8'))
        english_recipes = json.loads((translations / 'EN/Recipes.json').read_text(encoding='utf-8'))
        for locale in locales:
            self.assertEqual(json.loads((translations / locale / 'ContextMenu.json').read_text(encoding='utf-8')), english_context)
            self.assertEqual(json.loads((translations / locale / 'Recipes.json').read_text(encoding='utf-8')), english_recipes)

    def test_legacy_item_migrates_once_preserves_record_and_unties(self):
        self.run_lua('''
            local old={version=1,tied=true,original=50,name='Legacy glasses',
                material='Base.Twine',customName=true}
            g.data.StayPutGlasses=old; g.name='Legacy glasses (Tied)'
            assert(B47ANCEDEyewear.state(g)==old)
            B47ANCEDEyewear.refresh(p)
            local current=g.data.B47ANCEDEyewear
            assert(current~=old and current.tied and current.name==old.name)
            assert(g.data.StayPutGlasses==old and old.tied and g.chance==0)
            assert(syncs==1 and m.uses==2)
            B47ANCEDEyewear.refresh(p); assert(syncs==1)
            assert(B47ANCEDEyewear.untie(p,g))
            assert(not current.tied and old.tied and g.name=='Legacy glasses')
            assert(g.chance==10 and m.uses==2)
            B47ANCEDEyewear.refresh(p); assert(not current.tied)
        ''')

    def test_client_legacy_fallback_never_migrates_or_overrides_new_state(self):
        self.run_lua('''
            local old={version=1,tied=true,original=50}
            g.data.StayPutGlasses=old
            function isClient() return true end
            B47ANCEDEyewear.refresh(p)
            assert(g.chance==0 and g.data.B47ANCEDEyewear==nil and syncs==0)
            assert(not B47ANCEDEyewear.migrateState(p,g))
            assert(not B47ANCEDEyewear.untie(p,g) and old.tied)
            local current={version=1,tied=false,original=50}
            g.data.B47ANCEDEyewear=current
            B47ANCEDEyewear.refresh(p)
            assert(g.chance==10 and B47ANCEDEyewear.state(g)==current)
            g.data.B47ANCEDEyewear={retired=true}
            assert(B47ANCEDEyewear.state(g)==nil)
            assert(syncs==0 and m.uses==2)
        ''')

    def test_invalid_legacy_and_canonical_records_are_not_replaced(self):
        self.run_lua('''
            g.data.StayPutGlasses={version=1,tied=true,original=101}
            assert(not B47ANCEDEyewear.migrateState(p,g))
            assert(g.data.B47ANCEDEyewear==nil and syncs==0)
            g.data.StayPutGlasses={version=1,tied=true,original=50}
            local canonical={version=2,tied=true,original=50}
            g.data.B47ANCEDEyewear=canonical
            assert(not B47ANCEDEyewear.migrateState(p,g))
            assert(B47ANCEDEyewear.state(g)==nil and g.data.B47ANCEDEyewear==canonical)
            assert(syncs==0 and m.uses==2)
        ''')

    def test_legacy_monocle_retirement_never_resurrects_or_deletes_old_data(self):
        self.run_lua('''
            g=makeItem('Base.Glasses_MonocleLeft')
            local old={version=1,tied=true,original=50,name='Old monocle',customName=false}
            g.data.StayPutGlasses=old; g.name='Old monocle (Tied)'
            B47ANCEDEyewear.refresh(p)
            assert(g.chance==70 and g.name=='Old monocle')
            assert(g.data.StayPutGlasses==old and old.tied)
            assert(g.data.B47ANCEDEyewear.retired and not B47ANCEDEyewear.isTied(g))
            local before=syncs; B47ANCEDEyewear.refresh(p)
            assert(syncs==before and not B47ANCEDEyewear.isTieable(g) and m.uses==2)
        ''')

    def test_legacy_test_kit_marker_prevents_duplicate_grant(self):
        self.run_lua('''
            kitData={['GlassesStayPut.TestKitVersion']='1'}; grants=0
            p.getModData=function() return kitData end
            function getSpecificPlayer() return p end
            function inv:AddItem(kind) grants=grants+1; return makeItem(kind) end
        ''')
        self.lua.execute((ROOT / 'client/B47ANCEDEyewear/TestKit.lua').read_text())
        self.run_lua('''
            assert(not B47ANCEDEyewearTestKit() and grants==0)
            assert(kitData['B47ANCEDEyewear.TestKitVersion']=='1')
            assert(kitData['GlassesStayPut.TestKitVersion']=='1')
            assert(B47ANCEDEyewearTestKit(true) and grants>0)
            kitData['B47ANCEDEyewear.TestKitVersion']=nil
            function isClient() return true end
            assert(not B47ANCEDEyewearTestKit(true))
            assert(kitData['B47ANCEDEyewear.TestKitVersion']==nil)
        ''')

    def test_network_rejects_deprecated_channel(self):
        self.lua.execute((ROOT / 'server/B47ANCEDEyewear/Server.lua').read_text())
        self.run_lua('''
            function inv:getItemById(id) return id==1 and g or (id==2 and m or nil) end
            local server=B47ANCEDEyewear.Server
            assert(not server.onClientCommand('GlassesStayPut','Tie',p,{itemId=1,materialId=2}))
            assert(g.chance==50 and m.uses==2 and syncs==0)
            assert(server.onClientCommand('B47ANCEDEyewear','Tie',p,{itemId=1,materialId=2}))
            assert(g.chance==0 and m.uses==1)
        ''')

    def test_internal_requires_exact_case_and_translation_callsite_coverage(self):
        modules = {str(path.relative_to(ROOT / side)).replace('\\','/')[:-4]
                   for side in ('shared','server','client')
                   for path in (ROOT / side).rglob('*.lua')}
        vanilla = {'TimedActions/ISBaseTimedAction', 'TimedActions/ISTimedActionQueue', 'ISUI/ISPanel', 'ISUI/ISToolTipInv'}
        used = set()
        for path in ROOT.rglob('*.lua'):
            source = path.read_text()
            for require in re.findall(r"require\s*(?:\(\s*)?['\"]([^'\"]+)['\"]", source):
                self.assertIn(require, modules | vanilla, (path, require))
            used.update(re.findall(r"['\"](ContextMenu_B47ANCEDEyewear_[^'\"]+)['\"]", source))
        context = json.loads((ROOT / 'shared/Translate/EN/ContextMenu.json').read_text())
        self.assertEqual(used, set(context))
        self.assertFalse(any('StayPut' in module for module in modules))

    def test_retention_classifies_helmets_eyewear_and_hats(self):
        self.run_lua('''
            local R=B47ANCEDEyewear.Retention
            assert(R.classify(makeItem('Base.Hat_Army'))=='strapped')
            assert(R.classify(makeItem('Base.Hat_ArmyWWII'))=='strapped')
            assert(R.classify(makeItem('Base.Hat_CrashHelmetFULL_Spiked'))=='strapped')
            assert(R.classify(makeItem('Base.Hat_HardHat_Miner'))=='strapped')
            assert(R.classify(makeItem('Base.Hat_Fireman'))=='strapped')
            assert(R.classify(makeItem('Base.Hat_BaseballCap'))==nil)
            assert(R.classify(makeItem('Base.Hat_Beany'))==nil)
            assert(R.classify(makeItem('Base.Hat_StrawHat'))=='loose')
            assert(R.classify(makeItem('Base.Hat_SummerHat'))=='loose')
            assert(R.classify(makeItem('Base.Glasses_Prescription'))=='fitted')
            assert(R.classify(makeItem('Base.Glasses_MonocleLeft'))=='monocle')
            assert(R.classify(makeItem('Base.Hat_PeakedCapArmy'))==nil)
            assert(R.classify(makeItem('Base.Hat_BeretArmy'))==nil)
            assert(R.classify(makeItem('ExampleMod.SkiMask'))==nil)
            assert(R.chanceFor(makeItem('Base.Hat_Army'),false)==0)
            assert(R.chanceFor(makeItem('Base.Hat_BaseballCap'),false)==nil)
            assert(R.chanceFor(makeItem('Base.Glasses_Prescription'),false)==10)
            assert(R.chanceFor(makeItem('Base.Glasses_MonocleLeft'),false)==70)
            assert(R.chanceFor(makeItem('Base.Hat_StrawHat'),false,80)==80)
            assert(R.chanceFor(makeItem('Base.Hat_StrawHat'),true,80)==0)
            assert(R.register('Modded.BoogieHat','strapped'))
            assert(R.classify(makeItem('Modded.BoogieHat'))=='strapped')
        ''')

    def test_vanilla_eyewear_profiles_replace_blanket_fifteen_and_restore_after_untie(self):
        self.run_lua('''
            local R=B47ANCEDEyewear.Retention
            local expected={
                ['Base.Glasses_SkiGoggles']=2, ['Base.Glasses_SwimmingGoggles']=2,
                ['Base.Glasses_SafetyGoggles']=5, ['Base.Glasses_Shooting']=8,
                ['Base.Glasses_Prescription_Shooting']=8, ['Base.Glasses_OldWeldingGoggles']=8,
                ['Base.Glasses']=10, ['Base.Glasses_Prescription']=10,
                ['Base.Glasses_Aviators']=15, ['Base.Glasses_Prescription_Aviators']=15,
                ['Base.Glasses_Normal_HornRimmed']=15, ['Base.Glasses_Cosmetic_Normal_HornRimmed']=15,
                ['Base.Glasses_CatsEye']=18, ['Base.Glasses_CatsEye_Sun']=18,
                ['Base.Glasses_Cosmetic_CatsEye']=18, ['Base.Glasses_Prescription_CatsEye_Sun']=18,
                ['Base.Glasses_Normal']=20, ['Base.Glasses_Cosmetic_Normal']=20,
                ['Base.Glasses_Sun']=20, ['Base.Glasses_Prescription_Sun']=20,
                ['Base.Glasses_Round_Normal']=20, ['Base.Glasses_Round_Shades']=20,
                ['Base.Glasses_Cosmetic_Round_Normal']=20, ['Base.Glasses_Prescription_Round_Shades']=20,
                ['Base.Glasses_70s_Gold']=20, ['Base.Glasses_Cosmetic_70s_Gold']=20,
                ['Base.Glasses_Macho']=20, ['Base.Glasses_Reading']=25,
                ['Base.Glasses_JackieO']=25, ['Base.Glasses_Prescription_JackieO']=25,
                ['Base.Glasses_HalfMoon']=30, ['Base.Glasses_Cosmetic_HalfMoon']=30,
                ['Base.Glasses_SunCheap']=30, ['Base.Glasses_NewWave']=30,
                ['Base.Glasses_Round_HoloSkulls']=30, ['Base.Glasses_3dGlasses']=35,
                ['Base.Glasses_Groucho']=35, ['Base.Glasses_Venetian']=35,
                ['Base.Glasses_Novelty_Xray']=35,
            }
            for kind,chance in pairs(expected) do
                local item=makeItem(kind); item.chance=15
                B47ANCEDEyewear.applyChance(item,p)
                assert(item.chance==chance and R.chanceFor(item,false)==chance)
            end
            local item=makeItem('Base.Glasses_Reading'); item.chance=15; g=item; m.uses=2
            assert(B47ANCEDEyewear.tie(p,item,m) and item.chance==0)
            assert(B47ANCEDEyewear.untie(p,item) and item.chance==25)
        ''')

    def test_helmet_refresh_sets_zero_chance(self):
        self.run_lua('''
            local helmet=makeItem('Base.Hat_Army'); helmet.chance=10
            worn={size=function() return 1 end,get=function() return {getItem=function() return helmet end} end}
            B47ANCEDEyewear.refresh(p); assert(helmet.chance==0)
            local cap=makeItem('Base.Hat_BaseballCap'); cap.chance=60
            worn={size=function() return 1 end,get=function() return {getItem=function() return cap end} end}
            B47ANCEDEyewear.refresh(p); assert(cap.chance==60)
        ''')

    def test_straw_hat_ties_and_restores(self):
        self.run_lua('''
            g=makeItem('Base.Hat_StrawHat'); g.chance=80; m.uses=2
            assert(B47ANCEDEyewear.isTieable(g) and not B47ANCEDEyewear.isGlasses(g))
            assert(ISB47ANCEDEyewear:new(p,g,m,false):complete())
            assert(g.chance==0 and g.data.B47ANCEDEyewear.tied and m.uses==1)
            g.chance=80; B47ANCEDEyewear.refresh(p); assert(g.chance==0)
            assert(ISB47ANCEDEyewear:new(p,g,nil,true):complete())
            assert(g.chance==80 and not g.data.B47ANCEDEyewear.tied and m.uses==1)
        ''')


if __name__ == '__main__':
    unittest.main()

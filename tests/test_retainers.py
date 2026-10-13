import unittest
import test_glasses


class RetainerTests(unittest.TestCase):
    def setUp(self):
        fixture = test_glasses.GlassesTests()
        fixture.setUp()
        self.lua = fixture.lua
        self.lua.execute('''
            R=require 'B47ANCEDEyewear/Retainers'
            function B47ANCEDEyewearBridgeReady() return true end
            function g:getContainer() return inv end
            function m:getContainer() return inv end
            ItemTag={SHARP_KNIFE='knife',SCISSORS='scissors'}
        ''')

    def test_catalog_and_consumption(self):
        self.lua.execute('''local count=0
            for kind,spec in pairs(R.materials) do
                g.data={};m.kind=kind;m.uses=2
                assert(R.install(p,g,m,0));count=count+1
                assert(R.state(g).current==spec.dur and m.uses==1)
                assert(not R.install(p,g,m,0) and m.uses==1)
            end
            assert(count==14)
        ''')

    def test_reinforcement_preserves_wear_and_caps(self):
        self.lua.execute('''m.kind='Base.Thread';m.uses=8
            assert(R.install(p,g,m,0));local d=R.state(g);d.current=1
            assert(R.reinforce(p,g,m,1));assert(R.state(g).current==3)
            assert(R.state(g).maximum==4)
            assert(R.reinforce(p,g,m,2));assert(not R.reinforce(p,g,m,3))
            assert(m.uses==5)
            m.kind='Base.FishingLine';assert(not R.reinforce(p,g,m,3))
        ''')

    def test_tape_and_zip_exclusion(self):
        self.lua.execute('''assert(R.install(p,g,m,0));m.kind='Base.DuctTape'
            assert(R.applyTape(p,g,m,1));assert(R.state(g).maximum==8)
            assert(not R.applyTape(p,g,m,2))
            g.data={};m.kind='Base.Zipties';m.uses=3
            assert(R.install(p,g,m,0));m.kind='Base.Scotchtape'
            assert(not R.applyTape(p,g,m,1))
        ''')

    def test_breaking_proposal_is_pure_then_exhausted(self):
        self.lua.execute('''assert(R.install(p,g,m,0));R.state(g).current=1
            local original=R.state(g)
            local proposal=R.prepareCatch(p,g,nil,false,'SERVER')
            assert(proposal.current==0 and proposal.revision==2)
            assert(R.state(g)==original and original.current==1)
            g.data[R.key]=proposal
            assert(R.prepareCatch(p,g,nil,false,'SERVER')==nil)
        ''')

    def test_owner_client_revision_and_disable_rejections(self):
        self.lua.execute('''unworn=true;assert(not R.install(p,g,m,0));unworn=false
            function isClient() return true end
            assert(not R.install(p,g,m,0));function isClient() return false end
            assert(R.install(p,g,m,0));assert(not R.remove(p,g,0))
            SandboxVars={B47ANCEDEyewear={MakeshiftRetainersEnabled=false}}
            assert(R.prepareCatch(p,g,nil,false,'SERVER')==nil)
            assert(R.remove(p,g,1));assert(m.uses==1)
        ''')

    def test_consumption_failure_rolls_back_and_sync_failure_retains(self):
        self.lua.execute('''function m:UseAndSync() error('before use') end
            assert(not R.install(p,g,m,0));assert(R.state(g)==nil and m.uses==2)
            function m:UseAndSync() self.uses=self.uses-1 end
            function syncItemModData() error('notification') end
            assert(R.install(p,g,m,0));assert(R.state(g).current==6 and m.uses==1)
        ''')

    def test_malformed_formula_is_rejected(self):
        self.lua.execute('''assert(R.install(p,g,m,0));R.state(g).maximum=7
            assert(R.state(g)==nil)
            assert(not R.install(p,g,m,0) and m.uses==1)
        ''')

    def test_zip_cut_requires_usable_owned_tool(self):
        self.lua.execute('''m.kind='Base.Zipties';assert(R.install(p,g,m,0))
            assert(not R.remove(p,g,1))
            local tool={getContainer=function() return inv end,
                getCondition=function() return 1 end,hasTag=function(_,tag) return tag=='knife' end,
                isDull=function() return true end}
            assert(not R.remove(p,g,1,tool))
            tool.isDull=function() return false end
            assert(R.remove(p,g,1,tool));assert(m.uses==1)
        ''')

    def test_server_resolves_ids_and_rejects_duplicate_command(self):
        self.lua.execute('''
            function inv:getItemById(id) if id==10 then return g elseif id==20 then return m end end
        ''')
        from pathlib import Path
        source = Path(test_glasses.ROOT) / 'server/B47ANCEDEyewear/RetainerServer.lua'
        self.lua.execute(source.read_text(encoding='utf-8'))
        self.lua.execute('''local args={operation='Install',itemId=10,materialId=20,revision=0}
            assert(R.onClientCommand('B47ANCEDEyewear','Retainer',p,args))
            assert(not R.onClientCommand('B47ANCEDEyewear','Retainer',p,args))
            assert(m.uses==1)
            args.operation='unknown';assert(not R.onClientCommand('B47ANCEDEyewear','Retainer',p,args))
        ''')

    def test_legacy_migration_is_finite_once_without_consumption(self):
        self.lua.execute('''g.data.B47ANCEDEyewear={version=1,tied=true,original=50,
                material='Base.Twine',name='Prescription Glasses',customName=false}
            g.chance=0
            assert(R.migrateLegacy(p,g));assert(R.state(g).current==6)
            assert(not g.data.B47ANCEDEyewear.tied and m.uses==2)
            assert(not R.migrateLegacy(p,g))
            B47ANCEDEyewear.applyChance(g,p);assert(g.chance>0)
        ''')

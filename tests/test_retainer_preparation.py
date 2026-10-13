"""Audit/source-asset checks only. These do not test a runtime retainer feature."""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import struct
import tempfile
import unittest
from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
ASSETS = PROJECT / 'assets/retainers'


class RetainerPreparationTests(unittest.TestCase):
    def test_material_sources_and_balance_are_explicit(self):
        audit = json.loads((PROJECT/'research/retainers/vanilla-audit.json').read_text())
        rows = {row['full_type']:row for row in audit['materials']}
        self.assertEqual(len(rows),16)
        for row in rows.values():
            self.assertTrue(row['source'].startswith('media/scripts/'))
            self.assertGreater(row['line'],0)
            self.assertEqual(row['module']+'.'+row['id'],row['full_type'])
            self.assertEqual(row['drainable'],row['fields']['ItemType']=='base:drainable')
            self.assertEqual(row['maximum_base'],row['contribution']*row['layers'])
        self.assertEqual(rows['Base.RubberBand']['layers'],1)
        self.assertEqual(rows['Base.Thread_Aramid']['maximum_base'],18)
        self.assertEqual(rows['Base.PremiumFishingLine']['maximum_base'],15)
        self.assertEqual(rows['Base.Zipties']['layers'],1)
        self.assertFalse(rows['Base.Zipties']['tape_compatible'])
        self.assertEqual(rows['Base.Scotchtape']['layers'],0)
        self.assertFalse(rows['Base.Scotchtape']['drainable'])
        self.assertTrue(rows['Base.DuctTape']['drainable'])

    def test_eyewear_has_model_evidence_and_monocles_are_excluded(self):
        audit=json.loads((PROJECT/'research/retainers/vanilla-audit.json').read_text())
        rows=audit['eyewear']
        self.assertEqual(len(rows),45)
        monocles=[r for r in rows if 'Monocle' in r['id']]
        self.assertEqual(len(monocles),4)
        self.assertTrue(all(r['decision']=='RETAINER INCOMPATIBLE' for r in monocles))
        self.assertTrue(all(r['model']['m_AttachBone']=='Bip01_Head' for r in rows if r['decision']=='RETAINER COMPATIBLE'))
        self.assertTrue(all(r['decision']=='REQUIRES REVIEW' for r in rows if r['id'] in ['Glasses_SkiGoggles','Glasses_SwimmingGoggles']))

    def test_source_parser_excludes_comments_and_preserves_line_evidence(self):
        spec=importlib.util.spec_from_file_location('retainer_audit',PROJECT/'scripts/audit_retainer_sources.py')
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'fixture.txt'
            source.write_text('module Test {\n/*\n item Fake { ItemType = base:normal, }\n*/\n item Real\n {\n ItemType = base:drainable,\n UseDelta = 0.2,\n Tags = base:thread,\n }\n}\n')
            rows=module.items(source)
        self.assertEqual([r['full_type'] for r in rows],['Test.Real'])
        self.assertEqual(rows[0]['fields']['UseDelta'],'0.2')
        self.assertGreater(rows[0]['line'],3)

    def test_asset_hashes_dimensions_transparency_and_exact_case(self):
        manifest=json.loads((ASSETS/'asset-manifest.json').read_text())
        names={p.name for p in ASSETS.iterdir()}
        for name,digest in manifest['files'].items():
            self.assertIn(name,names)
            self.assertEqual(hashlib.sha256((ASSETS/name).read_bytes()).hexdigest(),digest)
        with Image.open(ASSETS/'Item_B47ANCEDEyewearRetainer.png') as icon:
            self.assertEqual(icon.size,(64,64)); self.assertEqual(icon.mode,'RGBA')
            alpha=icon.getchannel('A')
            self.assertEqual(alpha.getextrema()[0],0)
            self.assertGreater(alpha.getextrema()[1],200)
            self.assertGreater(sum(a>100 for a in alpha.tobytes()),150)
        with Image.open(ASSETS/'B47ANCEDEyewearRetainer_Texture.png') as texture:
            self.assertEqual(texture.size,(128,32))
        material=(ASSETS/'B47ANCEDEyewearRetainer.mtl').read_text()
        self.assertIn('map_Kd B47ANCEDEyewearRetainer_Texture.png',material)

    def test_original_model_has_valid_geometry_and_outward_winding(self):
        lines=(ASSETS/'B47ANCEDEyewearRetainer.obj').read_text().splitlines()
        vertices=[tuple(map(float,l.split()[1:])) for l in lines if l.startswith('v ')]
        normals=[tuple(map(float,l.split()[1:])) for l in lines if l.startswith('vn ')]
        faces=[tuple(int(i.split('/')[0])-1 for i in l.split()[1:]) for l in lines if l.startswith('f ')]
        self.assertEqual(len(vertices),354); self.assertEqual(len(faces),488)
        for a,b,c in faces:
            self.assertTrue(all(0<=index<len(vertices) for index in (a,b,c)))
            u=[vertices[b][k]-vertices[a][k] for k in range(3)]
            v=[vertices[c][k]-vertices[a][k] for k in range(3)]
            cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
            self.assertGreater(sum(x*x for x in cross),1e-20)
            dot=sum(cross[k]*(normals[a][k]+normals[b][k]+normals[c][k]) for k in range(3))
            self.assertGreater(dot,0)
        self.assertTrue(all(abs(math.sqrt(sum(x*x for x in n))-1)<1e-6 for n in normals))

    def test_glb_buffer_lengths_and_model_payload(self):
        blob=(ASSETS/'B47ANCEDEyewearRetainer.glb').read_bytes()
        magic,version,length=struct.unpack_from('<III',blob)
        self.assertEqual((magic,version,length),(0x46546C67,2,len(blob)))
        size,kind=struct.unpack_from('<II',blob,12); self.assertEqual(kind,0x4E4F534A)
        model=json.loads(blob[20:20+size])
        binary_offset=20+size
        bin_size,kind=struct.unpack_from('<II',blob,binary_offset)
        self.assertEqual(kind,0x004E4942)
        self.assertEqual(binary_offset+8+bin_size,len(blob))
        self.assertEqual(model['accessors'][0]['count'],354)
        self.assertEqual(model['accessors'][3]['count'],488*3)
        for view in model['bufferViews']:
            self.assertLessEqual(view['byteOffset']+view['byteLength'],model['buffers'][0]['byteLength'])
        self.assertEqual(model['images'][0]['mimeType'],'image/png')


if __name__=='__main__':
    unittest.main()

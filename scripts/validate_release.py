"""Production source/package preflight. No gameplay fixtures or test execution."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import sys
import stat
import subprocess
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/B47ANCEDEyewear/42'
LANGUAGES = 'AR CA CH CN CS DA DE EN ES ES_CL ES_MX FI FR HU ID IT JP KO NL NO PL PT PTBR RO RU STREW TH TR UA'.split()
VANILLA = {'TimedActions/ISBaseTimedAction', 'TimedActions/ISTimedActionQueue', 'ISUI/ISToolTipInv', 'ISUI/ISPanel',
           'NPCs/BodyLocations', 'TimedActions/ISWearClothing', 'TimedActions/ISUnequipAction'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def validate_clothing_registry(files):
    """Native OutfitManager resolves clothing through the file GUID table."""
    import uuid
    table_path = 'media/fileGuidTable.xml'
    if table_path not in files:
        raise ValueError('Missing native clothing file GUID table')
    table = ET.fromstring(files[table_path])
    if table.tag != 'fileGuidTable':
        raise ValueError('Invalid file GUID table root')
    registered = {}
    guids = set()
    for entry in table:
        path, guid = entry.findtext('path'), entry.findtext('guid')
        if entry.tag != 'files' or path not in files or not guid:
            raise ValueError('Invalid or case-incorrect clothing GUID entry')
        canonical_guid = str(uuid.UUID(guid))
        if path in registered or canonical_guid in guids:
            raise ValueError('Duplicate clothing GUID or path')
        registered[path] = canonical_guid
        guids.add(canonical_guid)
    expected = {name: str(uuid.UUID(ET.fromstring(data).findtext('m_GUID')))
                for name, data in files.items()
                if name.startswith('media/clothing/clothingItems/') and name.endswith('.xml')}
    if registered != expected:
        raise ValueError('Clothing XML GUID registrations are incomplete or mismatched')
    for name, data in files.items():
        if name.startswith('media/scripts/') and name.endswith('.txt'):
            for clothing in re.findall(r'\bClothingItem\s*=\s*([^,\s]+)\s*,', data.decode('utf-8')):
                if 'media/clothing/clothingItems/' + clothing + '.xml' not in registered:
                    raise ValueError('Unregistered or case-incorrect ClothingItem: ' + clothing)
    print('Native clothing GUID registry, unique identities and case-correct bindings PASS:', len(expected))


def validate_worn_models(files, improvised=False):
    import assimp_py
    import math
    import uuid
    directory = ROOT / ('assets/retainers/improvised' if improvised else 'assets/retainers/worn')
    manifest = json.loads((directory / ('improvised-models.json' if improvised else 'worn-models.json')).read_text(encoding='utf-8'))
    if manifest['version'] != (ROOT / 'VERSION').read_text(encoding='utf-8').strip():
        raise ValueError('Worn asset manifest version differs from canonical version')
    for name, expected in manifest['authoring_files'].items():
        if Path(name).name != name or digest((directory / name).read_bytes()) != expected:
            raise ValueError('Worn authoring provenance mismatch: ' + name)
    generator = 'build_improvised_tie_models.py' if improvised else 'build_retainer_worn_models.py'
    helpers = manifest['helper_sha256'] if improvised else {'build_retainer_ground_models.py': manifest['helper_sha256']}
    for filename, expected in {generator: manifest['generator_sha256'], **helpers}.items():
        if Path(filename).name != filename or digest((ROOT / 'scripts' / filename).read_bytes()) != expected:
            raise ValueError('Worn asset generator/helper changed without export review')
    entries = manifest['entries']
    kinds = ('Eyes', 'Face', 'Hat') if improvised else ('Cloth', 'Leather', 'Unbreakable')
    kind_key = 'slot' if improvised else 'kind'
    expected_pairs = {(kind, body) for kind in kinds for body in ('M', 'F')}
    if len(entries) != 6 or {(e[kind_key], e['body']) for e in entries} != expected_pairs:
        raise ValueError('Worn male/female retainer inventory mismatch')
    items = dict(re.findall(r'\bitem\s+(\w+)\s*\{([^{}]*)\}', files['media/scripts/B47ANCEDEyewear_Items.txt'].decode('utf-8'), re.S))
    guids = set()
    bindings = [(kind, 'ImprovisedTie' + kind) for kind in kinds] if improvised else [('Cloth', 'MakeshiftRetainer'), ('Leather', 'EyewearRetainer'), ('Unbreakable', 'UnbreakableRetainer')]
    for kind, item in bindings:
        clothing = 'B47ANCEDEyewearImprovisedTie' + kind + 'Worn' if improvised else 'B47ANCEDEyewear' + kind + 'RetainerWorn'
        if not re.search(r'\bClothingItem\s*=\s*' + clothing + r'\s*,', items[item]):
            raise ValueError('Retainer worn clothing binding mismatch')
        if improvised and not re.search(r'\bBodyLocation\s*=\s*b47ancedeyewear:tie' + kind.lower() + r'\s*,', items[item]):
            raise ValueError('Improvised tie native worn slot changed')
        xml = ET.fromstring(files['media/clothing/clothingItems/' + clothing + '.xml'])
        guid = str(uuid.UUID(xml.findtext('m_GUID')))
        if guid in guids:
            raise ValueError('Duplicate worn clothing GUID')
        guids.add(guid)
        for field, value in {'m_Static':'true', 'm_AttachBone':'Bip01_Head', 'm_MasksFolder':'none',
                             'm_AllowRandomHue':'false', 'm_AllowRandomTint':'false'}.items():
            if xml.findtext(field) != value:
                raise ValueError('Worn head attachment invariant failed: ' + field)
        for entry in (e for e in entries if e[kind_key] == kind):
            model = xml.findtext('m_MaleModel' if entry['body'] == 'M' else 'm_FemaleModel')
            if 'media/models_X/' + model + '.x' != entry['mesh']:
                raise ValueError('Worn XML/model case mismatch')
            if 'media/textures/' + xml.findtext('textureChoices') + '.png' != entry['texture']:
                raise ValueError('Worn XML/texture case mismatch')
            for key in ('mesh', 'texture'):
                path = PurePosixPath(entry[key])
                if path.is_absolute() or '..' in path.parts or ':' in str(path) or '\\' in str(path):
                    raise ValueError('Unsafe worn asset path')
                if entry[key] not in files or digest(files[entry[key]]) != entry[key + '_sha256']:
                    raise ValueError('Worn asset path/hash mismatch')
            data = files[entry['mesh']]
            if not data.startswith(b'xof 0303txt 0032\n') or b'SkinWeights' in data or b'AnimationSet' in data:
                raise ValueError('Worn mesh must be static DirectX text')
            scene = assimp_py.import_file(str(SOURCE / entry['mesh']), assimp_py.Process_Triangulate | assimp_py.Process_ValidateDataStructure)
            if len(scene.meshes) != 1:
                raise ValueError('Worn export must import as one static mesh')
            mesh = scene.meshes[0]
            if mesh.num_faces != entry['triangles'] or mesh.num_vertices != entry['vertices'] or not 0 < mesh.num_faces <= 3000:
                raise ValueError('Worn import geometry inventory mismatch')
            if mesh.num_uv_components != [2] or mesh.normals is None or len(mesh.normals) != mesh.num_vertices * 3:
                raise ValueError('Worn import lacks UVs/normals')
            coords = list(mesh.vertices)
            if not all(math.isfinite(v) for v in coords + list(mesh.normals) + list(mesh.texcoords[0])):
                raise ValueError('Nonfinite worn geometry')
            bounds = [max(coords[axis::3]) - min(coords[axis::3]) for axis in (0, 1, 2)]
            if not all(0.005 < size < 0.25 for size in bounds):
                raise ValueError('Worn import dimensions outside authored head-local scale')
    print(('Improvised ties' if improvised else 'Retainers') + ': six worn meshes, Assimp import/geometry/UV/normals, XML/head attachments and provenance PASS')

def validate_ground_models(files):
    """Validate shipped asset identity and case-correct native model bindings."""
    from PIL import Image
    import io
    directory = ROOT / 'assets/retainers/ground'
    manifest = json.loads((directory / 'ground-models.json').read_text(encoding='utf-8'))
    if manifest['version'] != (ROOT / 'VERSION').read_text(encoding='utf-8').strip():
        raise ValueError('Ground asset manifest version differs from canonical version')
    if digest((ROOT / 'scripts/build_retainer_ground_models.py').read_bytes()) != manifest['generator_sha256']:
        raise ValueError('Ground asset generator differs from recorded export')
    for name, expected in manifest['authoring_files'].items():
        if Path(name).name != name or digest((directory / name).read_bytes()) != expected:
            raise ValueError('Ground authoring asset provenance mismatch: ' + name)
    script = files['media/scripts/B47ANCEDEyewear_Models.txt'].decode('utf-8')
    models = dict(re.findall(r'\bmodel\s+(\w+)\s*\{([^{}]*)\}', script, re.S))
    items = dict(re.findall(r'\bitem\s+(\w+)\s*\{([^{}]*)\}', files['media/scripts/B47ANCEDEyewear_Items.txt'].decode('utf-8'), re.S))
    expected_items = {'B47ANCEDEyewear.MakeshiftRetainer', 'B47ANCEDEyewear.EyewearRetainer', 'B47ANCEDEyewear.UnbreakableRetainer'}
    entries = manifest['entries']
    if len(entries) != 3 or {e['item'] for e in entries} != expected_items or len(models) != 3:
        raise ValueError('Ground retainer item/model inventory mismatch')
    crafted = [e for e in entries if e['item'] != 'B47ANCEDEyewear.UnbreakableRetainer']
    rare = next(e for e in entries if e['item'] == 'B47ANCEDEyewear.UnbreakableRetainer')
    for axis in (0, 1):
        target = sum(e['roundtrip_dimensions_metres'][axis] for e in crafted) / len(crafted)
        if abs(rare['roundtrip_dimensions_metres'][axis] - target) > 0.00001:
            raise ValueError('Black-cord footprint differs from the crafted retainer mean')
    for entry in entries:
        for key in ('mesh', 'texture'):
            path = PurePosixPath(entry[key])
            if path.is_absolute() or '..' in path.parts or ':' in str(path) or '\\' in str(path):
                raise ValueError('Unsafe ground asset path')
            if entry[key] not in files or digest(files[entry[key]]) != entry[key + '_sha256']:
                raise ValueError('Ground asset hash or path-case mismatch: ' + entry[key])
        if not files[entry['mesh']].startswith(b'Kaydara FBX Binary  \x00\x1a\x00'):
            raise ValueError('Ground mesh is not binary FBX')
        with Image.open(io.BytesIO(files[entry['texture']])) as image:
            image.verify()
        body = models[entry['model'].split('.')[1]]
        for field, path, prefix, suffix in [('mesh', entry['mesh'], 'media/models_X/', '.fbx'),
                                            ('texture', entry['texture'], 'media/textures/', '.png')]:
            value = path.removeprefix(prefix).removesuffix(suffix)
            if not path.startswith(prefix) or not path.endswith(suffix) or not re.search(r'\b' + field + r'\s*=\s*' + re.escape(value) + r'\s*,', body):
                raise ValueError('Ground model script asset lookup mismatch')
        if not re.search(r'\bstatic\s*=\s*true\s*,', body) or not re.search(r'\bscale\s*=\s*0\.6\s*,', body):
            raise ValueError('Ground model static/scale contract changed without asset review')
        if not re.search(r'\bWorldStaticModel\s*=\s*' + re.escape(entry['model']) + r'\s*,', items[entry['item'].split('.')[1]]):
            raise ValueError('Retainer WorldStaticModel binding mismatch')
        if entry['fbx_roundtrip'] != 'PASS' or not 0 < entry['triangles'] <= 3000 or not entry['uv_layers']:
            raise ValueError('Ground export lacks recorded Blender geometry validation')
    print('Three ground FBX/texture bindings and authoring/export provenance PASS')

def inventory():
    files = {}
    folded = set()
    for path in SOURCE.rglob('*'):
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise ValueError('Reparse point in runtime source')
        if not path.is_file():
            continue
        name = path.relative_to(SOURCE).as_posix()
        if name.lower() in folded:
            raise ValueError('Runtime filename case collision: ' + name)
        folded.add(name.lower())
        if path.suffix.lower() not in {'.lua', '.json', '.txt', '.info', '.png', '.dds', '.xml', '.fbx', '.x'}:
            raise ValueError('Unexpected runtime file: ' + name)
        if re.search(r'(?i)(?:testkit|fixture|(?:^|[/_])(?:test|debug)(?:[/_.]|$))', name):
            raise ValueError('Development-only runtime file: ' + name)
        files[name] = path.read_bytes()
    return files

def validate_mod_icon(files):
    from PIL import Image
    manifest = json.loads((ROOT / 'assets/branding/mod-icon.json').read_text(encoding='utf-8'))
    if manifest['project_version'] != (ROOT / 'VERSION').read_text().strip():
        raise ValueError('Mod icon manifest version differs from canonical version')
    runtime = 'media/ui/B47ANCEDEyewear_icon.png'
    if manifest['runtime'] != 'src/B47ANCEDEyewear/42/' + runtime:
        raise ValueError('Mod icon manifest points to an unexpected runtime file')
    if digest(files[runtime]) != manifest['runtime_sha256']:
        raise ValueError('Runtime mod icon differs from the selected export')
    metadata = dict(line.split('=', 1) for line in files['mod.info'].decode('utf-8').splitlines() if '=' in line)
    if metadata.get('icon') != runtime:
        raise ValueError('Mod icon binding is missing or case incorrect')
    master = ROOT / 'assets/branding/Eyewear_Icon_Transparent.png'
    if digest(master.read_bytes()) != manifest['master_sha256']:
        raise ValueError('Selected mod icon master changed')
    with Image.open(master) as image, Image.open(SOURCE / runtime) as icon:
        if icon.size != (64, 64) or icon.mode != 'RGBA' or icon.getchannel('A').getextrema() != (0, 255):
            raise ValueError('Mod icon must be a transparent 64x64 RGBA PNG')
        if image.resize((64, 64), Image.Resampling.LANCZOS).tobytes() != icon.tobytes():
            raise ValueError('Mod icon pixels differ from the selected master export')
        if any(icon.getpixel(p)[3] for p in ((0, 0), (63, 0), (0, 63), (63, 63))):
            raise ValueError('Mod icon contains background fill at a canvas corner')
    if digest((ROOT / 'thumbnail.png').read_bytes()) != manifest['thumbnail_sha256'] or digest(files['poster.png']) != manifest['poster_sha256']:
        raise ValueError('Thumbnail or poster changed during the mod-icon-only iteration')
    print('Selected 64px RGBA mod icon, master/export pixels, binding and preserved thumbnail/poster PASS')


def validate_source(files):
    validate_mod_icon(files)
    script = files['media/scripts/B47ANCEDEyewear_Items.txt'].decode('utf-8')
    definitions = dict(re.findall(r'\bitem\s+(\w+)\s*\{([^}]*)\}', script, re.S))
    for suffix in ('Eyes', 'Face', 'Hat'):
        old, new = 'ImprovisedTie' + suffix, 'LayeredTie' + suffix
        if old not in definitions or new not in definitions:
            raise ValueError('Missing legacy/layered tie item: ' + suffix)
        if definitions[old].replace('ConditionMax = 10,', 'ConditionMax = 100,') != definitions[new]:
            raise ValueError('Layered tie must preserve its legacy clothing/slot/wear properties: ' + new)
    catalogue = files['media/lua/shared/B47ANCEDEyewear/TieMaterials.lua'].decode('utf-8')
    materials = set(re.findall(r"\['(Base\.[^']+)'\]\s*=\s*\{durability=", catalogue))
    recipe = files['media/scripts/B47ANCEDEyewear_Crafting.txt'].decode('utf-8')
    selection = re.search(r'item 1 \[([^]]*Base\.Twine[^]]*)\] mode:keep', recipe)
    if len(materials) != 14 or not selection or set(selection[1].split(';')) != materials:
        raise ValueError('Direct Tie recipe and fourteen-material catalogue differ')
    validate_clothing_registry(files)
    validate_ground_models(files)
    validate_worn_models(files)
    validate_worn_models(files, improvised=True)
    from lupa.lua51 import LuaRuntime
    lua = LuaRuntime()
    compile_only = lua.eval('function(code,name) local f,e=loadstring(code,name); if not f then error(e) end end')
    modules = {name.split('/lua/', 1)[1].split('/', 1)[1][:-4] for name in files if name.endswith('.lua') and '/lua/' in name}
    for name, data in files.items():
        if name.endswith('.lua'):
            source = data.decode('utf-8')
            compile_only(source, '@' + name)
            if re.search(r'B47ANCEDEyewearBridgeReady|B47ANCEDEyewearPrepareCatch|javaagent|luajava', source):
                raise ValueError('Prohibited runtime bridge dependency: ' + name)
            for module in re.findall(r"\brequire\s*\(?\s*['\"]([^'\"]+)['\"]", source):
                if module not in modules | VANILLA:
                    raise ValueError('Missing or case-incorrect Lua require: ' + module)
        if name.endswith('.json'):
            json.loads(data)
        if name.endswith('.xml'):
            ET.fromstring(data)
    translated = SOURCE / 'media/lua/shared/Translate'
    actual = {p.name for p in translated.iterdir() if p.is_dir()}
    if actual != set(LANGUAGES):
        raise ValueError('Translation language inventory mismatch')
    english = {}
    for category in ('UI', 'ContextMenu', 'Sandbox', 'Recipes', 'ItemName'):
        reference = json.loads((translated / 'EN' / (category + '.json')).read_text(encoding='utf-8'))
        english.update(reference)
        for language in LANGUAGES:
            table = json.loads((translated / language / (category + '.json')).read_text(encoding='utf-8'))
            if table.keys() != reference.keys():
                raise ValueError('Translation key mismatch: ' + language + '/' + category)
            for key, value in table.items():
                if not isinstance(value, str) or not value.strip():
                    raise ValueError('Empty translation: ' + key)
                if sorted(re.findall(r'%\d+', value)) != sorted(re.findall(r'%\d+', reference[key])):
                    raise ValueError('Translation placeholder mismatch: ' + key)
    for name, data in files.items():
        if name.endswith('.lua'):
            for key in re.findall(r"\bgetText\(\s*['\"]((?:UI|ContextMenu)_B47ANCEDEyewear_[^'\"]+)['\"]", data.decode('utf-8')):
                if key not in english:
                    raise ValueError('Untranslated Lua label: ' + key)
        if name.startswith('media/scripts/') and name.endswith('.txt'):
            script = data.decode('utf-8')
            for recipe in re.findall(r'\bcraftRecipe\s+(\w+)', script):
                if recipe not in english:
                    raise ValueError('Untranslated crafting recipe: ' + recipe)
            for outputs in re.findall(r'\boutputs\s*\{([^}]*)\}', script, re.S):
                if 'B47ANCEDEyewear.UnbreakableRetainer' in outputs:
                    raise ValueError('Loot-only unbreakable retainer cannot be a crafting output')
                if 'B47ANCEDEyewear.ImprovisedTie' in outputs or 'B47ANCEDEyewear.LayeredTie' in outputs:
                    raise ValueError('Linked ties must be created only by the authoritative paid Tie transaction')
            for key in re.findall(r'\bTooltip\s*=\s*(\w+)\s*,', script):
                if key not in english:
                    raise ValueError('Untranslated recipe instructions: ' + key)
            for item in re.findall(r'\bitem\s+(\w+)\s*\{', script):
                if 'B47ANCEDEyewear.' + item not in english:
                    raise ValueError('Untranslated item: ' + item)
            for icon in re.findall(r'\bIcon\s*=\s*(\w+)\s*,', script):
                if 'media/textures/Item_' + icon + '.png' not in files:
                    raise ValueError('Missing item icon or incorrect path case: ' + icon)
            for clothing in re.findall(r'\bClothingItem\s*=\s*(\w+)\s*,', script):
                if 'media/clothing/clothingItems/' + clothing + '.xml' not in files:
                    raise ValueError('Missing clothing definition or incorrect path case: ' + clothing)
            for item, body in re.findall(r'\bitem\s+(\w+)\s*\{([^}]*)\}', script, re.S):
                if item in {'MakeshiftRetainer', 'EyewearRetainer', 'ImprovisedTieEyes', 'ImprovisedTieFace', 'ImprovisedTieHat',
                            'LayeredTieEyes', 'LayeredTieFace', 'LayeredTieHat'}:
                    for field, expected in {'BloodLocation':'Head', 'CanHaveHoles':'false', 'RemoveOnBroken':'true',
                                            'ConditionMax':'100' if item.startswith('LayeredTie') else '10', 'ChanceToFall':'0', 'Cosmetic':'true',
                                            'ConditionLowerChance':str({'MakeshiftRetainer':2, 'EyewearRetainer':4}.get(item,1))}.items():
                        if not re.search(r'\b' + field + r'\s*=\s*' + expected + r'\s*,', body):
                            raise ValueError('Finite tie/retainer native-wear invariant failed: ' + item + '/' + field)
                if item == 'UnbreakableRetainer':
                    if re.search(r'\bBloodLocation\s*=', body):
                        raise ValueError('Rare unbreakable retainer must not gain a damage layer')
                    for field, expected in {'CanHaveHoles':'false', 'RemoveOnBroken':'false', 'ChanceToFall':'0'}.items():
                        if not re.search(r'\b' + field + r'\s*=\s*' + expected + r'\s*,', body):
                            raise ValueError('Rare unbreakable invariant failed: ' + field)
    for filename in ('WORKSHOP_DESCRIPTION.txt', 'WORKSHOP_CHANGE_NOTE.txt'):
        text = (ROOT / filename).read_text(encoding='utf-8').strip()
        if filename=='WORKSHOP_DESCRIPTION.txt' and len(text.encode('utf-8'))>8000:
            raise ValueError('Description exceeds the established project 8000-byte preflight limit')
        if not text or '\\n' in text or '\\r' in text or re.search(r'\bTODO\b', text):
            raise ValueError('Invalid canonical Workshop text: ' + filename)
        if 'MP testing build - dedicated multiplayer NOT TESTED' not in text:
            raise ValueError('Missing MP-testing distribution notice: ' + filename)
    assets = ROOT / 'assets/retainers'
    asset_manifest = json.loads((assets / 'asset-manifest.json').read_text())
    for name, expected in asset_manifest['files'].items():
        if digest((assets / name).read_bytes()) != expected:
            raise ValueError('Editable asset provenance mismatch: ' + name)
    icon = 'media/textures/Item_B47ANCEDEyewearRetainer.png'
    if digest(files[icon]) != asset_manifest['files']['Item_B47ANCEDEyewearRetainer.png']:
        raise ValueError('Runtime retainer icon differs from original authoring asset')
    crafted = json.loads((assets / 'crafted-icons.json').read_text(encoding='utf-8'))
    for entry in crafted['entries']:
        for key, checksum in [('source', 'source_sha256'), ('icon', 'sha256')]:
            if Path(entry[key]).name != entry[key]:
                raise ValueError('Unsafe crafted asset path')
            if digest((assets / entry[key]).read_bytes()) != entry[checksum]:
                raise ValueError('Crafted asset provenance mismatch: ' + entry[key])
        if digest(files[entry['runtime_path']]) != entry['sha256']:
            raise ValueError('Runtime crafted icon differs from authoring export')
        data = files[entry['runtime_path']]
        if data[:8] != b'\x89PNG\r\n\x1a\n' or int.from_bytes(data[16:20], 'big') != 64 or int.from_bytes(data[20:24], 'big') != 64 or data[25] != 6:
            raise ValueError('Crafted runtime icon must be a 64x64 RGBA PNG')
    description = (ROOT / 'WORKSHOP_DESCRIPTION.txt').read_text(encoding='utf-8')
    origin = subprocess.check_output(['git', '-C', str(ROOT), 'remote', 'get-url', 'origin'], text=True).strip()
    match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:)([^/]+)/([^/]+?)(?:\.git)?', origin)
    if not match or match.group(1).lower()!='b47ance' or match.group(2).lower()!='b47ancedeyewear':
        raise ValueError('Configured GitHub source identity is unsupported or unexpected')
    if 'https://github.com/B47ANCE/B47ANCEDEyewear' not in description:
        raise ValueError('Canonical Workshop description lacks verified source URL')

def validate_archive(path, files, stage):
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC validation failed')
        normalized = {}
        folded = set()
        for member in archive.infolist():
            if stat.S_ISLNK(member.external_attr >> 16):
                raise ValueError('ZIP symlink is prohibited')
            name = member.filename.replace('\\', '/')
            if name.startswith('/') or '..' in PurePosixPath(name).parts or ':' in name:
                raise ValueError('Unsafe ZIP path')
            if name.lower() in folded:
                raise ValueError('ZIP duplicate/case collision')
            folded.add(name.lower())
            if not member.is_dir():
                normalized[name] = archive.read(member)
        expected = {'Contents/mods/B47ANCEDEyewear/42/' + name: data for name, data in files.items()}
        if set(normalized) != set(expected) | {'preview.png', 'workshop.txt', 'release-manifest.json'}:
            raise ValueError('ZIP file inventory mismatch')
        for name, data in expected.items():
            if normalized[name] != data:
                raise ValueError('ZIP/source mismatch: ' + name)
        manifest = json.loads(normalized['release-manifest.json'])
        version = (ROOT / 'VERSION').read_text().strip()
        commit = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
        status = json.loads((ROOT / 'docs/RELEASE_STATUS.json').read_text())
        required = {'version': version, 'workshop_id': (ROOT / 'WORKSHOP_ID.txt').read_text().strip(),
                    'app_id': 108600, 'mod_id': 'B47ANCEDEyewear', 'commit': commit,
                    'target_game': '42.21', 'source_root': 'src/B47ANCEDEyewear/42',
                    'source_validation': 'STATIC PASS', 'sp': status['sp'], 'g7': status['g7'], 'g8': status['g8']}
        if any(manifest.get(key) != value for key, value in required.items()):
            raise ValueError('ZIP provenance identity/commit/status mismatch')
        entries = manifest.get('files', [])
        declared = {entry['path']: entry['sha256'] for entry in entries}
        if len(entries) != len(declared) or declared != {name: digest(data) for name, data in files.items()}:
            raise ValueError('Embedded source manifest hash/inventory mismatch')
        if manifest.get('preview_sha256') != digest(normalized['preview.png']) or manifest.get('workshop_metadata_sha256') != digest(normalized['workshop.txt']):
            raise ValueError('Embedded preview/metadata provenance mismatch')
        for key, filename in [('description_sha256', 'WORKSHOP_DESCRIPTION.txt'), ('changenote_sha256', 'WORKSHOP_CHANGE_NOTE.txt')]:
            if manifest.get(key) != digest((ROOT / filename).read_bytes()):
                raise ValueError('Embedded canonical-text provenance mismatch')
        if stage:
            if any(p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()) for p in stage.rglob('*')):
                raise ValueError('Staging reparse point is prohibited')
            staged = {p.relative_to(stage).as_posix(): p.read_bytes() for p in stage.rglob('*') if p.is_file()}
            if staged != normalized:
                raise ValueError('Source/staging/ZIP inventory or data mismatch')
    print('Package CRC, inventory, path/case and source/staging parity PASS:', path.name)

def validate_vdf(path, stage):
    if stage is None:
        raise ValueError('VDF validation requires the explicit verified --stage path')
    text = path.read_text(encoding='utf-8-sig')
    pattern = re.compile(r'\s*(?:"((?:[^"\\]|\\["\\])*)"|([{}]))', re.S)
    tokens = []
    position = 0
    while text[position:].strip():
        match = pattern.match(text, position)
        if not match:
            raise ValueError('Invalid or unmatched VDF text')
        tokens.append(('brace', match.group(2)) if match.group(2) else ('string', re.sub(r'\\(["\\])', r'\1', match.group(1))))
        position = match.end()
    if len(tokens) < 3 or tokens[:2] != [('string', 'workshopitem'), ('brace', '{')] or tokens[-1] != ('brace', '}'):
        raise ValueError('Invalid Workshop VDF root')
    fields = {}
    body = tokens[2:-1]
    if len(body) % 2 or any(kind != 'string' for kind, value in body):
        raise ValueError('Invalid VDF field structure')
    for (_, key), (_, value) in zip(body[::2], body[1::2]):
        if key in fields:
            raise ValueError('Duplicate VDF field')
        fields[key] = value
    expected_keys = {'appid', 'publishedfileid', 'contentfolder', 'previewfile', 'visibility', 'title', 'description', 'changenote'}
    if fields.keys() != expected_keys:
        raise ValueError('Unexpected VDF fields')
    if fields['appid'] != '108600' or fields['publishedfileid'] != (ROOT / 'WORKSHOP_ID.txt').read_text().strip():
        raise ValueError('VDF targets wrong Workshop item')
    if Path(fields['contentfolder']).resolve() != (stage / 'Contents').resolve() or Path(fields['previewfile']).resolve() != (stage / 'preview.png').resolve():
        raise ValueError('VDF does not target verified staging')
    metadata = {}
    for line in (stage / 'workshop.txt').read_text(encoding='utf-8').splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            metadata[key] = value
    if fields['title'] != metadata.get('title') or fields['visibility'] != {'public': '0', 'friends': '1', 'private': '2'}.get(metadata.get('visibility')):
        raise ValueError('VDF title/visibility differs from verified staging')
    for key, filename in (('description', 'WORKSHOP_DESCRIPTION.txt'), ('changenote', 'WORKSHOP_CHANGE_NOTE.txt')):
        canonical = (ROOT / filename).read_text(encoding='utf-8').strip()
        if fields[key] != canonical:
            raise ValueError('Submitted VDF text differs from canonical: ' + key)
    print('VDF identity, paths, visibility and canonical paragraph preservation PASS')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--stage', type=Path)
    parser.add_argument('--vdf', type=Path)
    args = parser.parse_args()
    files = inventory()
    validate_source(files)
    print('Lua-only source, syntax, require casing and localization preflight PASS:', len(files), 'files')
    if args.archive:
        validate_archive(args.archive, files, args.stage)
    if args.vdf:
        validate_vdf(args.vdf, args.stage)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('Preflight FAILED:', error, file=sys.stderr)
        sys.exit(1)

"""Read-only vanilla source audit. Does not load the game or modify runtime files."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET


MATERIALS = [
    ('RubberBand', 'Elastic', 2, 1, True),
    ('Thread', 'Thin fiber', 2, 3, True),
    ('DentalFloss', 'Thin fiber', 2, 3, True),
    ('RippedSheets', 'Fabric', 4, 1, True),
    ('DenimStrips', 'Fabric', 6, 1, True),
    ('Twine', 'Cord', 6, 1, True),
    ('Thread_Sinew', 'Thin fiber', 3, 3, True),
    ('LeatherStrips', 'Strap', 10, 1, True),
    ('FishingLine', 'Thin fiber', 4, 3, True),
    ('ElectricWire', 'Rigid', 12, 1, True),
    ('Wire', 'Rigid', 14, 1, True),
    ('PremiumFishingLine', 'Thin fiber', 5, 3, True),
    ('Zipties', 'Rigid', 16, 1, False),
    ('Thread_Aramid', 'Thin fiber', 6, 3, True),
    ('Scotchtape', 'Tape only', 1, 0, False),
    ('DuctTape', 'Tape only', 2, 0, False),
]


def items(path):
    source = path.read_text(encoding='utf-8-sig')
    source = re.sub(r'/\*.*?\*/', lambda m: ''.join('\n' if c == '\n' else ' ' for c in m.group()), source, flags=re.S)
    source = re.sub(r'//[^\n]*', '', source)
    modules = list(re.finditer(r'\bmodule\s+(\w+)\s*\{', source))
    result = []
    for match in re.finditer(r'^\s*item\s+(\w+)\s*\{', source, re.M):
        preceding = [m for m in modules if m.start() < match.start()]
        if not preceding:
            raise ValueError(f'Missing module: {path}:{match.group(1)}')
        start = source.index('{', match.start())
        depth, end = 1, start + 1
        while depth and end < len(source):
            depth += (source[end] == '{') - (source[end] == '}')
            end += 1
        if depth:
            raise ValueError(f'Unclosed item: {path}:{match.group(1)}')
        fields = dict(re.findall(r'^\s*(\w+)\s*=\s*([^\n,]+),', source[start:end], re.M))
        fields = {k: v.strip() for k, v in fields.items()}
        module = preceding[-1].group(1)
        result.append({'module': module, 'id': match.group(1),
                       'full_type': module + '.' + match.group(1),
                       'line': source.count('\n', 0, match.start(1)) + 1,
                       'fields': fields})
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(game_root, output):
    game_root = game_root.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows, files, duplicates = {}, {}, []
    for path in sorted((game_root / 'media/scripts/generated/items').glob('*.txt')):
        for row in items(path):
            row['source'] = str(path.relative_to(game_root)).replace('\\', '/')
            if row['full_type'] in rows:
                if row['id'] in {material[0] for material in MATERIALS} or row['id'].startswith('Glasses') or row['fields'].get('BodyLocation') == 'base:eyes':
                    raise ValueError(f'Duplicate audited FullType: {row["full_type"]}')
                duplicates.append(row['full_type'])
                continue
            rows[row['full_type']] = row
        files[str(path.relative_to(game_root)).replace('\\', '/')] = digest(path)
    translations_path = game_root / 'media/lua/shared/Translate/EN/ItemName.json'
    translations = json.loads(translations_path.read_text(encoding='utf-8-sig'))
    files[str(translations_path.relative_to(game_root)).replace('\\', '/')] = digest(translations_path)
    materials = []
    for item_id, family, contribution, layers, tape in MATERIALS:
        full_type = 'Base.' + item_id
        if full_type not in rows:
            raise ValueError(f'Proposed material absent: {full_type}')
        row = dict(rows[full_type])
        drainable = row['fields'].get('ItemType') == 'base:drainable'
        row.update(display_name=translations.get(full_type, '[MISSING EN TRANSLATION]'),
                   family=family, contribution=contribution, layers=layers,
                   maximum_base=contribution * layers, tape_compatible=tape,
                   drainable=drainable,
                   consumption=('1 script use via UseAndSync; see fishing exception' if drainable else
                                '1 whole inventory item via vanilla removal/sync'))
        materials.append(row)
    eyewear = []
    review = {'Glasses_SkiGoggles', 'Glasses_SwimmingGoggles', 'Glasses_SafetyGoggles',
              'Glasses_OldWeldingGoggles', 'Glasses_Groucho', 'Glasses_Novelty_Xray',
              'Glasses_3dGlasses', 'Glasses_Venetian'}
    for row in rows.values():
        fields = row['fields']
        item_id = row['id']
        if not (item_id.startswith('Glasses') or item_id == 'ReadingGlasses' or
                ('Goggles' in item_id) or fields.get('BodyLocation') == 'base:eyes'):
            continue
        decision = 'REQUIRES REVIEW'
        reason = 'Slot/name alone cannot establish a physical temple connection.'
        if 'Monocle' in item_id:
            decision, reason = 'RETAINER INCOMPATIBLE', 'Hard rule: monocles have no paired temples.'
        elif fields.get('ItemType') != 'base:clothing':
            decision, reason = 'RETAINER INCOMPATIBLE', 'Inventory prop, not wearable clothing.'
        elif item_id.startswith('Glasses_Eyepatch') or any(t in item_id.lower() for t in ['mask','eyepatch','clown','blindfold']):
            decision, reason = 'RETAINER INCOMPATIBLE', 'Not paired-temple eyewear.'
        elif (item_id.startswith('Glasses') or item_id == 'ReadingGlasses') and item_id not in review:
            decision = 'RETAINER COMPATIBLE'
            reason = 'Provisional conventional-frame policy; physical male/female fit remains a runtime gate.'
        xml_name = fields.get('ClothingItem')
        model = {}
        if xml_name:
            xml = game_root / 'media/clothing/clothingItems' / (xml_name + '.xml')
            if xml.exists():
                tree = ET.parse(xml).getroot()
                model = {key: tree.findtext(key) for key in ['m_Static','m_AttachBone','m_MaleModel','m_FemaleModel']}
                files[str(xml.relative_to(game_root)).replace('\\', '/')] = digest(xml)
            else:
                decision, reason = 'REQUIRES REVIEW', 'Clothing XML could not be resolved with exact filename case.'
        eyewear.append(dict(row, display_name=translations.get(row['full_type'], '[MISSING EN TRANSLATION]'),
                           decision=decision, reason=reason, model=model))
    for relative in [
        'projectzomboid.jar',
        'media/lua/server/Items/ProceduralDistributions.lua',
        'media/lua/shared/TimedActions/ISRepairClothing.lua',
        'media/lua/shared/TimedActions/Fishing/TimedActions/ISChangeFishingRodEquip.lua',
        'media/lua/shared/NPCs/BodyLocations.lua',
        'media/scripts/generated/recipes/recipes_fixing.txt',
        'media/scripts/generated/recipes/recipes.txt',
    ]:
        files[relative] = digest(game_root / relative)
    data = {'environment':'Installed vanilla source; not runtime evidence',
            'materials': materials, 'eyewear': sorted(eyewear, key=lambda r:r['full_type']),
            'unrelated_duplicate_fulltypes_not_resolved': duplicates, 'source_sha256': files}
    (output / 'vanilla-audit.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    text = ['# Vanilla retainer material audit', '', '[VERIFIED installed source] FullTypes, fields and tags below are read from vanilla.',
            'DUR/layer/tape values are proposed mod balance from the user handoff, not vanilla statistics.',
            'No material or new retainer feature is enabled in runtime source.', '',
            '| Display name | Module / ID / FullType | Consumption | Tags | DUR | Layers | Max base | Tape |',
            '| --- | --- | --- | --- | ---: | ---: | ---: | --- |']
    for row in materials:
        fields = row['fields']
        consumption = '1 whole item' if not row['drainable'] else '1 use, UseDelta=' + fields.get('UseDelta', '?')
        text.append(f'| {row["display_name"]} | `{row["module"]}` / `{row["id"]}` / `{row["full_type"]}` | {consumption} | `{fields.get("Tags", "none")}` | {row["contribution"]} | {row["layers"]} | {row["maximum_base"]} | {"YES" if row["tape_compatible"] else "NO"} |')
    text += ['', 'Tape has layers=0 because it is reinforcement only; its contribution is added once, never standalone.',
             'Clean RippedSheets/DenimStrips/LeatherStrips are the initial candidates. Dirty, sterile, bundled',
             'and boxed variants are not silently mapped; vanilla unpacking/cleaning can produce the audited item.', '',
             '## Consumption evidence', '',
             'ISRepairClothing.complete uses thread UseAndSync; fabric uses sendRemoveItemFromContainer.',
             'Fishing/TimedActions/ISChangeFishingRodEquip.complete consumes 0.125 of normalized line fill',
             'with explicit sync/remove, not necessarily one script UseDelta. A future retainer uses one',
             'script-defined use consistently unless an approved recipe-specific amount replaces that policy.',
             'That is a declared mod consumption choice, not a claim that every vanilla action uses one use.',
             'Scotchtape is base:normal here; FixWithAdhesiveTape consumes three whole items for its own repair,',
             'while the proposed retainer reinforcement consumes one. DuctTape is drainable; its use count differs.',
             'No vanilla recipe supplies this second-layer retainer state; generic fixing callbacks are inappropriate.', '',
             'Source files, exact fields, line numbers, model metadata and hashes: research/retainers/vanilla-audit.json.']
    (output / 'MATERIAL_AUDIT.md').write_text('\n'.join(text)+'\n', encoding='utf-8')
    text = ['# Vanilla eyewear compatibility audit', '',
            '[VERIFIED installed source] FullTypes/slots/XML and attachment bone metadata.',
            '[INFERRED] Compatibility is a proposed policy, not tested fit. Conventional frames are candidates;',
            'goggles and novelty frames need geometry review. Nothing is activated by this audit.', '',
            '| FullType | Slot | Decision | Clothing XML | Static / bone | Reason |',
            '| --- | --- | --- | --- | --- | --- |']
    for row in data['eyewear']:
        f, m = row['fields'], row['model']
        text.append(f'| `{row["full_type"]}` | `{f.get("BodyLocation", "none")}` | {row["decision"]} | `{f.get("ClothingItem", "none")}` | {m.get("m_Static", "unknown")} / `{m.get("m_AttachBone", "unknown")}` | {row["reason"]} |')
    text += ['', 'All four monocles remain incompatible regardless of material/permanent/tape flags.',
             'Third-party eyewear is not implicitly admitted by its display name or FACE/EYES slot.',
             'Current broad Core.isGlasses detection is not sufficient for the expanded physical-fit allowlist.']
    (output / 'EYEWEAR_AUDIT.md').write_text('\n'.join(text)+'\n', encoding='utf-8')
    print(f'Verified {len(materials)} materials/tapes; classified {len(eyewear)} eyewear/eye-slot candidates; recorded {len(files)} source hashes.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game-root', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'research/retainers')
    args = parser.parse_args()
    audit(args.game_root, args.output)

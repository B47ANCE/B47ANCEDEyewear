# Unbreakable eyewear retainer — original source assets

These editable sources remain outside src/. The exact 64x64 inventory icon is
now reserved for the loot-only UnbreakableRetainer and copied into its runtime
texture slot unchanged. The mesh/model texture are reserved for the same item,
remain authoring-only and are not distributed. Crafted cloth and leather items
have separate generated masters and 64x64 exports in crafted-icons.json.
Source geometry/texture validation is distinct from PZ import, head fit and networking.

- Item_B47ANCEDEyewearRetainer.png: 64×64 RGBA inventory icon, real transparency.
- EyewearRetainer_Inventory_Source.png: selected built-in imagegen source, preserved
  at its original dimensions. No vanilla/third-party artwork was copied.
- B47ANCEDEyewearRetainer.obj / .mtl: original wearable mesh source, 354 vertices,
  488 triangles. Two hollow rubber temple sleeves, a thin rear cord and one slider.
- B47ANCEDEyewearRetainer.glb: portable glTF 2.0 source/preview with embedded original texture.
- B47ANCEDEyewearRetainer_Texture.png: original 128×32 power-of-two dark material atlas.
- asset-manifest.json: dimensions, part counts, status and SHA-256 hashes.

Item scripts and an invisible empty-texture clothing XML now support vanilla
Wear/Take Off. No final PZ FBX or fitted live model attachment is claimed.
The source mesh is metre-scaled, Y-up, with provisional head-local origin/axes and
human-scale proportions. Its dimensions are author-created, not extracted from
vanilla geometry. Vanilla XML independently verifies static Bip01_Head attachment;
the actual origin, axis conversion, male/female fit and compatible frame geometry
remain native/art-pipeline gates. OBJ/GLB are source deliverables, not assumed PZ formats.

## Rebuild and export

From the workspace root, rebuild deterministic model/texture outputs and retain
the existing icon without regenerating artwork:

```powershell
$pzPython = & ./tools/Resolve-HostTestPython.ps1
& $pzPython -B ./B47ANCEDEyewear/scripts/build_retainer_assets.py
```

The checked paths/PATH did not provide a Blender executable. The supplied export
script has not been run. With Blender 4.x or a compatible version, execute:

```powershell
blender --background --python ./B47ANCEDEyewear/scripts/export_retainer_fbx.py -- --output ./B47ANCEDEyewear/assets/retainers/export/B47ANCEDEyewearRetainer.fbx
```

That script imports the OBJ/MTL, uses metres, exports only the static mesh with
Y-up/-Z-forward FBX axes, no bones and no animation. These are initial export
settings, not validated PZ placement. If Blender changes those operator arguments,
resolve against that installed version before exporting. Do not claim the script
produced an FBX merely because it parses as Python.

In Blender, inspect front/side/back against independently inspected vanilla
head/eyewear dimensions. Confirm sleeve openings face along the temples, rear cord
has slight sag and slider sits behind the head. Calibrate scale/origin/rotation
against the actual PZ importer; provide male/female variants if required. No skeleton
is needed if the verified static Bip01_Head clothing path remains suitable.

After the native authority/ownership blockers are resolved, intended runtime paths:

```text
media/textures/Item_B47ANCEDEyewearRetainer.png
media/models_X/static/B47ANCEDEyewearRetainer.fbx
media/textures/B47ANCEDEyewearRetainer_Texture.png
media/clothing/clothingItems/B47ANCEDEyewearRetainer.xml
```

The icon path and clothing XML now exist under src/; the XML currently uses an
empty texture and has no model. Mesh and model-texture paths remain RESERVED.
Verify exact filename case, FBX import and lookup conventions before enabling them.
An XML using m_Static=true and m_AttachBone=Bip01_Head follows the audited vanilla
convention, but must accompany a verified way to render alongside the existing
eyewear without owning shared gameplay state or leaving orphaned visuals.
Then test equip/unequip, drop, inventory/container transfer, both body models,
animations, hats/hair clipping, two-client remote visuals, reconnect and restart.

The 64×64 icon was inspected after downscaling and is structurally alpha-checked.
Its native inventory appearance and any lighting/color differences remain NOT TESTED.

## Crafted inventory artwork

- ClothRetainer_Inventory_Source.png → Item_B47ANCEDEyewearClothRetainer.png.
- LeatherRetainer_Inventory_Source.png → Item_B47ANCEDEyewearLeatherRetainer.png.

Built-in image_gen created both transparent originals from text prompts. Normal
Pillow export resizes the artwork to 60x60 and pads it with 2 transparent pixels
inside a 64x64 RGBA icon, preserving alpha. The originals remain unchanged.
crafted-icons.json records dimensions, export/source SHA-256 and runtime paths;
ART_PROVENANCE.md records the full prompts. No new worn mesh is claimed.

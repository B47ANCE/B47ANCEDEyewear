# Retainer ground models

Project Version: 0.11.0-dev.1

All three existing retainer items now have original static ground assets:

| Item | Model | Appearance | Triangles |
| --- | --- | --- | --- |
| MakeshiftRetainer | ClothRetainerGround | Beige cloth strap, knotted loops | 1412 |
| EyewearRetainer | LeatherRetainerGround | Brown stitched strap, rubber loops | 1220 |
| UnbreakableRetainer | UnbreakableRetainerGround | Original black cord, hollow rubber sleeves, slider | 488 |

Module B47ANCEDEyewear qualifies every item/model name. The model script is
media/scripts/B47ANCEDEyewear_Models.txt. Each mesh lives in media/models_X/
WorldItems and its texture in media/textures/WorldItems, with exact matching
case. Ground models bind through WorldStaticModel; the invisible worn clothing
XML is unchanged. No Lua, recipes, loot, durability, sandbox settings, item/save
IDs or gameplay networking changed. Scale 0.6 follows the nearby vanilla rubber
band reference and is a presentation calibration value, not shared gameplay
configuration. Final PZ size and placement remain a runtime gate.

## Native source evidence

[VERIFIED: source] Installed Project Zomboid Build 42.21 (Steam 25485521):

- media/scripts/generated/models_items.txt: RubberBand, LeatherStrips, Thread,
  Twine and RippedSheets use mesh/texture paths under WorldItems and scale values.
  RubberBand uses scale 0.6; RippedSheets also demonstrates attachment world.
- media/scripts/generated/items/drainable.txt: RippedSheets, Thread and Twine bind
  WorldStaticModel. ModelScript.Load accepts mesh, texture, scale and static.
- Installed projectzomboid.jar, ItemModelRenderer.hasModel/init: checks
  InventoryItem.getWorldStaticItem and resolves ScriptManager.getModelScript
  before the worn-clothing fallback. WorldItemModelDrawer delegates rendering to
  ItemModelRenderer. Native source inspection is evidence for binding support,
  not evidence that these particular exports have rendered in PZ.
- Read-only Blender import of installed RubberBand.fbx and LeatherStrips.fbx
  confirmed flat ground geometry and metre-scale dimensions. No vanilla geometry,
  textures or materials were copied into this project.

## Authoring and ownership

assets/retainers/ground/RetainerGroundModels.blend contains editable meshes with
packed textures and a labelled preview scene. GroundRetainers_Preview.png is
an offline Blender render. ground-models.json records exporter version/settings,
mesh statistics, source/export hashes and FBX roundtrip dimensions. The new
script creates cloth/leather geometry and procedural atlases independently;
the rare asset derives from the project's existing original OBJ and exact atlas.
Original OBJ/MTL/GLB, inventory artwork and their provenance remain unchanged.

[TESTED: offline] Blender 4.5.7 LTS exports three binary FBX 7400 files and
re-imports each as one mesh with unchanged metre dimensions (tolerance 0.00001m).
Source meshes have UV coordinates, finite dimensions, nondegenerate triangles,
recalculated normals and no armatures/animation. Production preflight verifies
all hashes, PNG integrity, exact-case paths, item/model/texture bindings, static
flag and scale. No testing/debug runtime code was added.

[RUNTIME GATE] User requested no in-game testing. FBX importer compatibility,
orientation/ground contact, scale, lighting and dropped-item display on SP and
dedicated clients remain NOT TESTED. No PZ/server launch occurred. Ground
presentation introduces no new authority or persistence state; existing vanilla
item synchronization owns item identity. The underlying gameplay still lacks
required dedicated evidence: G7 BLOCKED / NOT TESTED, stable G8 BLOCKED.

0.11.0-dev.1 is source only. No package, local deployment or Workshop upload was
requested or performed in this iteration; Workshop still serves 0.10.0-dev.1.

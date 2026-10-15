# Visible worn improvised ties

Project Version: 0.13.1-dev.1

All six existing improvised materials now share a thin neutral knotted-cord
appearance. The three existing physical item types select different fittings:

| Existing item | Native slot | Clothing definition | Fit |
| --- | --- | --- | --- |
| ImprovisedTieEyes | b47ancedeyewear:tieeyes | B47ANCEDEyewearImprovisedTieEyesWorn | Rear eyewear cord |
| ImprovisedTieFace | b47ancedeyewear:tieface | B47ANCEDEyewearImprovisedTieFaceWorn | Slightly lower/outward rear cord |
| ImprovisedTieHat | b47ancedeyewear:tiehat | B47ANCEDEyewearImprovisedTieHatWorn | Under-chin hat cord |

Each XML selects separate male/female static DirectX meshes, a stable unique
GUID, Bip01_Head, no masks and fixed original cloth-atlas color. Exactly six new
meshes live under media/models_X/static/clothes with lowercase names. The Eyes
and Face positions differ to avoid identical overlapping surfaces when both
native slots are worn. Hat support remains limited to the existing straw/summer
hats; no compatibility scope is expanded. Twine, rubber bands, dental floss,
ordinary thread, sinew thread and aramid thread use the same cord visual;
material-specific appearances and linked-item geometry fitting are not claimed.

## Ownership, persistence and configuration

This is presentation on actual existing worn clothing items. All 14 gameplay Lua
files, payments, reciprocal native item links, condition, breaking, schemas, IDs,
body slots, recipes, loot and protection settings remain unchanged. The native
server-owned worn mapping and SyncClothing already replicate these tie items.
No item grants, new types, client command, ModData, migration, dynamic texture
mutation or new synchronization is introduced. Actual ties render whenever worn,
including without their linked target; protection still requires both items.
Vanilla break/unwear, taking off and Untie govern the actual item appearance.
The old invisible XML remains as a compatibility asset. Existing retainers and
all ground assets/icons are preserved byte-for-byte.

Art dimensions are internal fitting values; no new shared gameplay behavior
needs sandbox configuration. Existing authoritative gameplay settings continue
unchanged. There are no per-tick scans or new runtime events.

## Evidence and authoring

[VERIFIED: source] Installed Build 42.21 / Steam 25485521 uses m_Static=true and
Bip01_Head on glasses, earrings and the supported Hat_StrawHat/Hat_SummerHat XMLs.
Read-only numeric bounds from M/F_StrawHat.x and M/F_SummerHat.x establish the
supported hat reference scale, not a promise of final fit. No game geometry or
textures were copied. Existing ItemVisual.getClothingItem resolves the current
script definition; PopTemplateManager renders its body-specific head attachment.
Core and TieDurability already define exactly the six material choices and three
server-owned worn slots. Source hashes are recorded in the local API audit draft;
WORN_MODELS.md documents the shared native clothing rendering route.

scripts/build_improvised_tie_models.py creates the six original cords using
Blender 4.5.7 LTS bpy and existing project geometry/export helpers. It preserves
assets/retainers/improvised/ImprovisedTieWornModels.blend with packed original
cloth atlas, a male-example schematic preview and improvised-models.json with
mesh/helper/source hashes, counts and bounds. Female meshes remain editable in
the master with preview render visibility disabled. Hat examples are front views;
Eyes/Face are rear views. Schematic heads and hats are original helpers, never
runtime payload or game geometry. The six static exports have UVs/normals and
no bones or animation; native XML attaches them to the existing head bone.

[TESTED: offline] Production preflight independently imports all six meshes
through assimp-py 1.1.0 and checks finite geometry, UVs, normals, counts and scale.
It checks every item/XML/texture/head-attachment/path-case/hash contract, plus
existing retainer and ground contracts. Total runtime source: 194 files, with
the same 14 Lua files syntax-compiled without gameplay execution. The Blender
preview was inspected. No testing/debug runtime code or test suite was added.

[RUNTIME GATE] Actual PZ orientation, eyewear/hat contact, all body types,
concurrent ties, hair/frame/hat clipping, old-save refresh, break/take-off visuals,
join/rejoin and remote rendering remain NOT TESTED. These are rigid attachments,
without physics or automatic hair/hat hiding. No separate improvised ground
model is authored; vanilla may use the worn-clothing mesh as its dropped-item
fallback, whose placement is also untested. Offline import is not game proof.
G7 BLOCKED / NOT TESTED and stable G8 BLOCKED remain in force for the gameplay.
No PZ/server launch, package, local deployment or Workshop upload was requested
or performed in this source iteration. Workshop still serves 0.12.0-dev.1.

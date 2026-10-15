# Worn retainer presentation

Project Version: 0.13.0-dev.1

All three retainer items now bind visible, original head-attached static clothing
meshes. Cloth has a beige strap and tied loops; leather has stitching and dark
loops; the rare black cord has rubber sleeves and an adjustment slider. Six
meshes provide separate male/female sizes. This is source implementation with
offline import evidence; actual PZ display and fit remain NOT TESTED.

## Binding and authority

The three item definitions now point at B47ANCEDEyewearClothRetainerWorn,
B47ANCEDEyewearLeatherRetainerWorn and B47ANCEDEyewearUnbreakableRetainerWorn
XMLs. Each has a unique stable GUID, m_Static=true, m_AttachBone=Bip01_Head,
m_MasksFolder=none, fixed color and two body-model paths. textureChoices reuses
the corresponding original WorldItems atlas. Model files use lowercase paths
under media/models_X/static/clothes, matching XML lookups exactly for Linux.
The existing B47ANCEDEyewearRetainer invisible XML remains as a compatibility
asset. Improvised ties now use separate native worn definitions; see
IMPROVISED_TIE_MODELS.md. The six retainer meshes and XMLs remain unchanged.

The independent retainer body slot already coexists with glasses; no exclusion
or hide-model rules were added. Clothing appearance follows the actual native
worn item and existing vanilla synchronization. No new client commands, copies,
item spawns, ModData, persistence schema or gameplay authority were introduced.
All Lua, recipes, loot, damage/condition, sandbox settings and ground asset bytes
are preserved. Mesh fitting dimensions are internal artwork calibration; no
new meaningfully configurable shared gameplay behavior needs a sandbox option.
The vanilla worn model appears while the retainer is equipped, including when
protection is disabled or glasses are absent; this mirrors ordinary clothing.

## Installed Build 42.21 source evidence

Steam build 25485521 is the installed baseline. This inspection launches no game.

- Glasses_Normal.xml and Glasses_Cosmetic_Normal.xml under
  media/clothing/clothingItems use body-specific static models, Bip01_Head,
  no masks and textureChoices. Earring_LoopSmall_Gold_Both.xml uses the same
  attachment independently of glasses. The custom slot has no hiding/exclusion.
- media/models_X/Static/Clothes/M_Glasses_Normal.x and F_Glasses_Normal.x
  are DirectX text meshes (xof 0303txt 0032). Read-only numeric bounds and identity
  frame transforms establish the native head-local scale: X up, Y lateral,
  Z forward. Only metadata was inspected; no vanilla geometry/art is shipped.
- Native PopTemplateManager.addClothingItem selects getModel(isFemale),
  ItemVisual.getTextureChoice and attachBone, then calls newStaticInstance.
  Model uses media/textures/<texture choice>.png. ItemVisual.getClothingItem
  resolves the current script item, supporting current bindings for existing
  item types. Actual save/load refresh behavior remains a runtime gate.

## Authoring and validation

scripts/build_retainer_worn_models.py creates six original meshes using Blender
4.5.7 LTS bpy, preserves editable assets/retainers/worn/RetainerWornModels.blend,
and renders WornRetainers_Preview.png. The heads are original schematic helpers,
not PZ character meshes and never runtime payload. Clothes export in the native
DirectX static format used by installed eyewear, with explicit UVs and normals,
no skeleton or animations. Editable Blender uses Z up/X lateral/-Y forward;
export converts to native head coordinates and reverses winding for handedness.
Worn meshes are independent fitted shapes; ground meshes remain unchanged.

worn-models.json records source/export hashes, counts, bounds, units and tool
provenance. Production validate_release.py independently imports all six files
through Assimp (assimp-py 1.1.0), checks one mesh each, finite coordinates/normals/
UVs, triangle counts and head-local scale, and verifies item/XML/texture/path-case
and stable attachment contracts. No tests/debug runtime code was introduced.

[TESTED: offline, 0.12.0-dev.1] Assimp import and source preflight passed for all
six retainer meshes and 185 runtime files, including the same 14 Lua files.
The current preflight rechecks those unchanged assets alongside the new ties,
for 194 runtime files. Lua is compiled without gameplay execution.
The Blender preview was inspected; original artwork, all ground FBX/textures and
Lua behavior remain unchanged. A subsequent explicit publish request authorizes
Workshop development / MP test distribution; exact outcome is recorded in
generated publication provenance, not inferred from these offline checks.

[RUNTIME GATE] No in-game testing was requested. Final head fit, male/female
alignment, attachment orientation, motion, hair/hat/frame clipping, take-off,
old-save refresh, remote-player rendering, join/rejoin and restart behavior are
NOT TESTED. A rigid head attachment does not simulate cord physics. Other
headwear/hair can intersect; this iteration does not hide them. G7 BLOCKED /
NOT TESTED and stable G8 BLOCKED remain in force for the underlying gameplay.
The prior published 0.11.1 package is preserved. The requested 0.12.0 development
upload uses the existing item and preflight gates; it does not prove runtime fit.

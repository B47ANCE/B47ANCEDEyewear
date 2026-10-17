# Original improvised-tie worn assets

Six original male/female Eyes/Face/Hat meshes share the existing original cloth
atlas as a neutral knotted cord for every improvised material. No material-
specific or linked-target geometry fitting is claimed.

ImprovisedTieWornModels.blend preserves editable meshes and packed atlas. The
schematic preview shows male examples: rear eyewear cords and front hat chin
cord. Female meshes/helpers remain editable with preview render visibility off.
Schematic heads/hats are original helpers, never vanilla geometry or runtime data.

Run scripts/build_improvised_tie_models.py using Blender 4.5 LTS bpy; it writes
six static native DirectX text exports and authoring/preview/provenance files.
Existing retainer scripts supply unchanged geometry/export helpers. The manifest
binds helper and asset hashes. validate_release.py independently imports every
mesh with Assimp and validates item/XML/texture/slot/case/hash contracts.

Actual PZ fit, clipping, concurrent layers and remote visuals are NOT TESTED.
See ../../../docs/IMPROVISED_TIE_MODELS.md. No Java or new gameplay code is used.

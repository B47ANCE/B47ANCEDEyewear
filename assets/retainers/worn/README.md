# Original worn retainer assets

RetainerWornModels.blend contains original male/female cloth, leather and black-
cord meshes and packed copies of the project's existing atlases. Schematic heads
are original preview helpers, never game geometry or shipped runtime models.

Run scripts/build_retainer_worn_models.py with Blender 4.5 LTS bpy to regenerate
six native DirectX text meshes, editable source, preview and worn-models.json.
The exporter uses the native static-glasses head-local format; no skinning or
animation is needed for rigid Bip01_Head attachment. UV/normals are explicit.
validate_release.py independently imports every file through Assimp and verifies
XML/texture/hash/case contracts. Dependencies are pinned in requirements-tools.txt.

PZ fit, orientation, hair/hat/frame clipping, animations and remote visuals are
NOT TESTED. See ../../../docs/WORN_MODELS.md. No vanilla/third-party art was copied.

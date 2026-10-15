# Retainer source assets

Original OBJ/MTL/GLB, original texture atlas and all inventory icon masters remain
unchanged. asset-manifest.json and crafted-icons.json retain their original file
hashes; ART_PROVENANCE.md records inventory-art creation.

The three runtime ground models are authored by
scripts/build_retainer_ground_models.py with Blender 4.5.7 LTS bpy. The editable
master, offline preview and export/hash manifest are under ground/. Textures are
packed into the .blend. The original rare-item OBJ is imported as a derived ground
asset; its 128x32 atlas is copied exactly. Cloth/leather geometry and 128x128
woven/grain atlases are original procedural work, with different silhouettes.

Run with a Blender 4.5 LTS Python environment containing bpy:

```powershell
python scripts/build_retainer_ground_models.py
python -B scripts/check_versions.py
python -B scripts/validate_release.py
```

The generator writes runtime FBX/PNG assets and the authoring master/preview/
manifest; it never writes original OBJ/GLB, inventory art or gameplay scripts.
The master lays out the three meshes for the preview; exports are individually
centred at the origin before that layout is applied. Each mesh has UVs and one
material, triangulated faces, outward normals, no bones and no animation. FBX
re-import dimensions are checked against the source. Rebuilds are not promised
byte-identical because Blender serializes timestamps/IDs; refresh the manifest
and review exports together after deliberate authoring changes.

See ../../docs/GROUND_MODELS.md for verified game bindings and remaining runtime
gates. This is a Blender preview, not PZ evidence. The worn clothing definition
still has empty models/textures. The older export_retainer_fbx.py describes a
provisional worn export only; it is not the current ground asset pipeline.

For a cord-only adjustment, run the generator with --only-unbreakable to preserve
the existing cloth/leather FBX bytes while checking all three roundtrip sizes.
The derived cord is resized to the crafted meshes' mean X/Y footprint; original
OBJ/GLB and atlas bytes are preserved. Rebuild the preview/master and manifest
with the same command so the authoring source and shipped export agree.

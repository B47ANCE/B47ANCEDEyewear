"""Run in Blender (4.x+), not host Python. FBX import/fit in PZ remains a gate."""
import argparse
from pathlib import Path
import sys
import bpy

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
assets = Path(__file__).resolve().parents[1] / 'assets/retainers'
bpy.ops.wm.read_factory_settings(use_empty=True)
# Standard OBJ source is metres, Y up. No bones or game attachment are invented.
bpy.ops.wm.obj_import(filepath=str(assets/'B47ANCEDEyewearRetainer.obj'),
                      forward_axis='NEGATIVE_Z', up_axis='Y')
mesh_objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not mesh_objects:
    raise RuntimeError('No source mesh imported')
for obj in mesh_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = mesh_objects[0]
bpy.context.scene.unit_settings.system='METRIC'
bpy.context.scene.unit_settings.scale_length=1.0
args.output.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.export_scene.fbx(filepath=str(args.output), use_selection=True,
                         object_types={'MESH'}, axis_forward='-Z', axis_up='Y',
                         apply_unit_scale=True, bake_anim=False, add_leaf_bones=False,
                         path_mode='RELATIVE', use_mesh_modifiers=True)
print('Exported source FBX; native scale/origin/axis and head fitting still require validation.')

"""Author original worn improvised cords with Blender 4.5 LTS bpy.

Shared neutral cord for all six existing materials; body-slot-specific fits.
This authoring tool never changes gameplay or existing retainer assets.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
import bpy
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_retainer_worn_models import tube, join, export_x, use_image, aim

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/B47ANCEDEyewear/42'
AUTHOR=ROOT/'assets/retainers/improvised'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def knot(center):
    points=[]
    for i in range(25):
        a=i*math.tau/12
        points.append((center[0]+0.0024*math.cos(a),center[1]+0.001*i/24,
                       center[2]+0.0024*math.sin(a)))
    return tube('OverhandKnot',points,0.00085)


def main():
    AUTHOR.mkdir(parents=True,exist_ok=True)
    destination=SOURCE/'media/models_X/static/clothes'
    destination.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC'
    texture=SOURCE/'media/textures/WorldItems/B47ANCEDEyewearClothRetainerGround.png'
    material=use_image(bpy.data.images.load(str(texture)), 'NeutralImprovisedCord')
    objects=[]
    entries=[]
    for sex,width,height in [('M',0.062,0.075),('F',0.057,0.070)]:
        for slot in ('Eyes','Face','Hat'):
            points=[]
            for i in range(41):
                a=i*math.pi/40
                if slot=='Hat':
                    points.append((-(width+0.009)*math.cos(a),-0.005-0.05*math.sin(a),
                                   height+0.021-0.126*math.sin(a)))
                else:
                    # Separate native body slots may be worn together. Keep the
                    # Face cord slightly lower/further out than the Eyes cord.
                    face=slot=='Face'
                    points.append((-(width+(0.003 if face else 0))*math.cos(a),
                                   0.018+(0.071 if face else 0.067)*math.sin(a),
                                   height-(0.008 if face else 0)-0.020*math.sin(a)))
            parts=[tube(slot+'Cord',points,0.0011)]
            if slot=='Hat':
                center=points[20]
                parts.append(knot(center))
                for side in (-1,1):
                    parts.append(tube('LooseChinTail',[center,(side*0.005,center[1]-0.002,center[2]-0.012),
                                                      (side*0.009,center[1]+0.001,center[2]-0.024)],0.0009))
            else:
                # Visible knotted ends at the eyewear temples, without sleeves.
                for index,side in ((0,-1),(-1,1)):
                    point=points[index]
                    parts.append(knot(point))
                    parts.append(tube('TempleTail',[point,(point[0]+side*0.003,point[1]+0.006,point[2]-0.008),
                                                   (point[0]+side*0.004,point[1]+0.009,point[2]-0.015)],0.00085))
                center=points[20]
                parts.append(knot(center))
            name='b47ancedeyewear_improvised_'+slot.lower()+'_'+sex.lower()
            obj=join(parts,name,material)
            path=destination/(name+'.x')
            stats=export_x(obj,path)
            entries.append({'slot':slot,'body':sex,'mesh':path.relative_to(SOURCE).as_posix(),
                            'mesh_sha256':sha(path),'texture':texture.relative_to(SOURCE).as_posix(),
                            'texture_sha256':sha(texture),**stats})
            objects.append((obj,slot,sex))
    # Original schematic heads/hats only; no game geometry in authoring/runtime.
    labels=[]
    for i,(obj,slot,sex) in enumerate(objects):
        x=(i%3-1)*0.24
        y=0.31 if sex=='M' else -0.01
        obj.location=(x,y,0)
        obj.hide_render=sex=='F'  # Single-row overview; female authoring meshes remain in the master.
        if slot=='Hat':
            obj.rotation_euler.z=math.pi  # Front view in preview only; export is unchanged.
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=(x,y-0.005,0.095))
        head=bpy.context.object
        head.name='SchematicHead_'+slot+sex
        head.scale=(0.055 if sex=='M' else 0.050,0.074,0.097)
        mat=bpy.data.materials.get('Mannequin') or bpy.data.materials.new('Mannequin')
        mat.diffuse_color=(0.25,0.28,0.32,1)
        head.data.materials.append(mat)
        head.hide_render=sex=='F'
        if slot=='Hat':
            hatmat=bpy.data.materials.get('SchematicHat') or bpy.data.materials.new('SchematicHat')
            hatmat.diffuse_color=(0.40,0.31,0.19,1)
            brim_height=0.100 if sex=='M' else 0.095
            bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=0.108,depth=0.004,location=(x,y,brim_height))
            brim=bpy.context.object
            brim.name='SchematicHatBrim_'+sex
            brim.scale.y=1.15
            brim.data.materials.append(hatmat)
            brim.hide_render=sex=='F'
            bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=0.064,depth=0.110,location=(x,y,brim_height+0.055))
            bpy.context.object.name='SchematicHatCrown_'+sex
            bpy.context.object.scale.y=1.22
            bpy.context.object.hide_render=sex=='F'
            bpy.context.object.data.materials.append(hatmat)
        bpy.ops.object.text_add()
        label=bpy.context.object
        label.data.body=slot.upper()+' / '+sex+(' (FRONT)' if slot=='Hat' else ' (REAR)')
        label.data.align_x='CENTER'
        label.data.size=0.010
        label.hide_render=sex=='F'
        labels.append((label,x,sex))
    bpy.ops.object.camera_add(location=(0,0.95,0.62))
    scene.camera=bpy.context.object
    aim(scene.camera,(0,0.31,0.07))
    scene.camera.data.type='ORTHO'
    scene.camera.data.ortho_scale=0.85
    bpy.context.view_layer.update()
    for label,x,sex in labels:
        label.location=scene.camera.matrix_world@Vector((-x,-0.185,-0.12))
        label.rotation_euler=scene.camera.rotation_euler
        labelmat=bpy.data.materials.get('Labels') or bpy.data.materials.new('Labels')
        labelmat.use_nodes=True
        shader=labelmat.node_tree.nodes.get('Principled BSDF')
        shader.inputs['Emission Color'].default_value=(1,1,1,1)
        shader.inputs['Emission Strength'].default_value=1
        label.data.materials.append(labelmat)
    for location,energy in [((0,0.6,0.8),30),((-0.5,0.2,0.4),15)]:
        bpy.ops.object.light_add(type='AREA',location=location)
        light=bpy.context.object
        light.data.energy=energy
        light.data.size=0.6
        aim(light,(0,0.15,0.06))
    scene.world=bpy.data.worlds.new('Preview world')
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0.25,0.25,0.25,1)
    scene.render.engine='CYCLES'
    scene.cycles.samples=24
    scene.render.resolution_x,scene.render.resolution_y=1400,700
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    preview=AUTHOR/'ImprovisedTies_Preview.png'
    scene.render.filepath=str(preview)
    for image in bpy.data.images:
        if image.source=='FILE':image.pack()
    blend=AUTHOR/'ImprovisedTieWornModels.blend'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.render.render(write_still=True)
    manifest={'schema':1,'version':(ROOT/'VERSION').read_text(encoding='utf-8').strip(),
              'tool':'Blender '+bpy.app.version_string,'format':'DirectX text xof 0303txt 0032; static, no skin/animation',
              'attachment':'Bip01_Head','axes':'Native X up/Y lateral/Z forward; Blender Z up/X lateral/-Y forward',
              'appearance':'Shared neutral knotted cord for all six existing materials; Eyes/Face rear cords and Hat chin cord.',
              'provenance':'Original procedural meshes; existing original cloth atlas. Preview shows male examples; female meshes are retained in the master with render visibility off. Original schematic heads/hats are preview helpers only.',
              'runtime':'NOT TESTED in PZ; actual fit, clipping, old-save refresh and remote visuals remain runtime gates.',
              'entries':entries,'authoring_files':{blend.name:sha(blend),preview.name:sha(preview)},
              'generator_sha256':sha(Path(__file__)),
              'helper_sha256':{name:sha(ROOT/'scripts'/name) for name in ('build_retainer_worn_models.py','build_retainer_ground_models.py')}}
    (AUTHOR/'improvised-models.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Exported six original improvised tie models, editable master, preview and provenance')


if __name__=='__main__':
    main()

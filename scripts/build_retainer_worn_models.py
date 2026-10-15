"""Original head-local static clothing assets; run with Blender 4.5 LTS bpy.

DirectX text meshes follow the installed vanilla static-glasses convention.
Preview mannequins are original schematic geometry, never copied game meshes.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
import bpy
import bmesh
from mathutils import Vector, Matrix
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_retainer_ground_models import mesh, loop, use_image, aim

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/B47ANCEDEyewear/42'
AUTHOR = ROOT / 'assets/retainers/worn'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tube(name, points, radius, band=0, inner=None, rare=False):
    verts, faces = [], []
    sides = 8
    radii = [radius, inner] if inner else [radius]
    for r in radii:
        for i, point in enumerate(points):
            direction = (Vector(points[min(i+1, len(points)-1)]) - Vector(points[max(i-1, 0)])).normalized()
            a = direction.cross(Vector((0, 0, 1))).normalized()
            if a.length < 0.1:
                a = direction.cross(Vector((0, 1, 0))).normalized()
            b = direction.cross(a).normalized()
            for j in range(sides):
                angle = j * math.tau / sides
                verts.append(tuple(Vector(point) + r * (a * math.cos(angle) + b * math.sin(angle))))
    layer = len(points) * sides
    for k in range(len(radii)):
        for i in range(len(points)-1):
            for j in range(sides):
                face = (k*layer+i*sides+j, k*layer+i*sides+(j+1)%sides,
                        k*layer+(i+1)*sides+(j+1)%sides, k*layer+(i+1)*sides+j)
                faces.append(face if k == 0 else face[::-1])
    for cap in (0, len(points)-1):
        for j in range(sides):
            if inner:
                face = (cap*sides+j, cap*sides+(j+1)%sides,
                        layer+cap*sides+(j+1)%sides, layer+cap*sides+j)
                faces.append(face if cap == 0 else face[::-1])
        if not inner:
            faces.append(tuple(cap*sides+j for j in (range(sides) if cap == 0 else reversed(range(sides)))))
    obj = mesh(name, verts, faces, band)
    if rare:
        for uv in obj.data.uv_layers.active.data:
            uv.uv = ((band + 0.5) / 3, 0.5)
    return obj


def strap(points, width, thickness):
    verts, faces = [], [(3, 2, 1, 0)]
    for i, p in enumerate(points):
        tangent = Vector(points[min(i+1, len(points)-1)]) - Vector(points[max(i-1, 0)])
        outward = Vector((-tangent.y, tangent.x, 0)).normalized() * thickness / 2
        vertical = Vector((0, 0, width / 2))
        for offset in (-outward-vertical, outward-vertical, outward+vertical, -outward+vertical):
            verts.append(tuple(Vector(p)+offset))
    for i in range(len(points)-1):
        for j in range(4):
            faces.append((i*4+j, i*4+(j+1)%4, (i+1)*4+(j+1)%4, (i+1)*4+j))
    k=(len(points)-1)*4
    faces.append((k,k+1,k+2,k+3))
    return mesh('Strap', verts, faces)


def join(parts, name, material):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.object.join()
    obj=parts[0]
    obj.name=name
    obj.data.materials.clear()
    obj.data.materials.append(material)
    bm=bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    if any(p.area <= 1e-12 for p in obj.data.polygons):
        raise ValueError('Degenerate worn triangle')
    return obj


def export_x(obj, path):
    # Match native head-local XYZ: X up, Y lateral, Z forward.
    # Split triangle corners to preserve per-corner UVs/normals without skin data.
    positions,normals,uvs,faces=[],[],[],[]
    for polygon in obj.data.polygons:
        ids=[]
        for loop_index in reversed(polygon.loop_indices):
            co=obj.data.vertices[obj.data.loops[loop_index].vertex_index].co
            n=polygon.normal
            ids.append(len(positions))
            positions.append((co.z,co.x,-co.y))
            normals.append((n.z,n.x,-n.y))
            u,v=obj.data.uv_layers.active.data[loop_index].uv
            uvs.append((u,1-v))
        faces.append(tuple(ids))
    def rows(values):
        return '\n'.join(';'.join(f'{v:.9f}' for v in row)+';'+(';' if i==len(values)-1 else ',') for i,row in enumerate(values))
    def face_rows():
        return '\n'.join('3;'+','.join(map(str,f))+';'+(';' if i==len(faces)-1 else ',') for i,f in enumerate(faces))
    text=('xof 0303txt 0032\nMesh '+obj.name+' {\n'+str(len(positions))+';\n'+rows(positions)+'\n'+str(len(faces))+';\n'+face_rows()+
          '\nMeshNormals {\n'+str(len(normals))+';\n'+rows(normals)+'\n'+str(len(faces))+';\n'+face_rows()+'\n}\n'+
          'MeshTextureCoords {\n'+str(len(uvs))+';\n'+rows(uvs)+'\n}\n}\n')
    path.write_text(text,encoding='ascii',newline='\n')
    return {'vertices':len(positions),'triangles':len(faces),
            'native_min':[min(p[i] for p in positions) for i in range(3)],
            'native_max':[max(p[i] for p in positions) for i in range(3)]}


def main():
    AUTHOR.mkdir(parents=True,exist_ok=True)
    destination=SOURCE/'media/models_X/static/clothes'
    destination.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC'
    entries=[]
    objects=[]
    for sex,width,height in [('M',0.062,0.075),('F',0.057,0.070)]:
        for kind in ('Cloth','Leather','Unbreakable'):
            image_path=SOURCE/('media/textures/WorldItems/B47ANCEDEyewear'+kind+'RetainerGround.png')
            material=use_image(bpy.data.images.load(str(image_path),check_existing=True),kind+sex)
            points=[]
            for i in range(33):
                a=i*math.pi/32
                points.append((-width*math.cos(a),0.018+0.064*math.sin(a),height-0.018*math.sin(a)))
            if kind=='Unbreakable':
                parts=[tube('Cord',points,0.0017,rare=True)]
                for x in (-width,width):
                    parts.append(tube('RubberSleeve',[(x,0.006,height),(x,0.028,height)],0.004,1,inner=0.0024,rare=True))
                parts.append(tube('Slider',[(-0.005,0.082,height-0.018),(0.005,0.082,height-0.018)],0.0036,2,rare=True))
            else:
                parts=[strap(points,0.009 if kind=='Cloth' else 0.006,0.0015)]
                for x in (-width,width):
                    end=loop('TempleLoop',(0,0,0),0.004,0.006,0.0015,0 if kind=='Cloth' else 2)
                    rotation=Matrix.Rotation(math.pi/2,4,'X')
                    for vertex in end.data.vertices:
                        vertex.co=rotation@vertex.co+Vector((x,0.018,height))
                    parts.append(end)
                    if kind=='Cloth':
                        parts.append(tube('Knot',[(x-0.004,0.023,height),(x+0.004,0.023,height)],0.002,1))
                if kind=='Leather':
                    for i in range(1,32,2):
                        x,y,z=points[i]
                        for dz in (-0.0019,0.0019):
                            parts.append(tube('Stitch',[(x-0.0005,y+0.001,z+dz),(x+0.0005,y+0.001,z+dz)],0.0002,1))
            name='b47ancedeyewear_'+kind.lower()+'_'+sex.lower()
            obj=join(parts,name,material)
            path=destination/(name+'.x')
            stats=export_x(obj,path)
            entries.append({'kind':kind,'body':sex,'mesh':path.relative_to(SOURCE).as_posix(),'mesh_sha256':sha(path),
                            'texture':image_path.relative_to(SOURCE).as_posix(),'texture_sha256':sha(image_path),**stats})
            objects.append((obj,kind,sex))
    # Original schematic heads, only for an offline fitting overview.
    labels=[]
    for i,(obj,kind,sex) in enumerate(objects):
        x=(i%3-1)*0.24
        y=0.31 if sex=='M' else -0.01
        obj.location=(x,y,0)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=(x,y-0.005,0.095))
        head=bpy.context.object
        head.name='SchematicHead_'+kind+sex
        head.scale=(0.055 if sex=='M' else 0.050,0.074,0.097)
        mat=bpy.data.materials.get('Mannequin') or bpy.data.materials.new('Mannequin')
        mat.diffuse_color=(0.25,0.28,0.32,1)
        head.data.materials.append(mat)
        bpy.ops.object.text_add(location=(x,y+0.115,0))
        label=bpy.context.object
        label.data.body=kind.upper()+' / '+sex
        label.data.align_x='CENTER'
        label.data.size=0.012
        labels.append((label,x,sex))
    bpy.ops.object.camera_add(location=(0,0.90,0.72))
    scene.camera=bpy.context.object
    aim(scene.camera,(0,0.15,0.06))
    scene.camera.data.type='ORTHO'
    scene.camera.data.ortho_scale=0.85
    bpy.context.view_layer.update()
    for label,x,sex in labels:
        label.location=scene.camera.matrix_world@Vector((-x,-0.225 if sex=='M' else 0.025,-0.12))
        label.rotation_euler=scene.camera.rotation_euler
        label_mat=bpy.data.materials.get('Labels') or bpy.data.materials.new('Labels')
        label_mat.use_nodes=True
        bsdf=label_mat.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Emission Color'].default_value=(1,1,1,1)
        bsdf.inputs['Emission Strength'].default_value=1
        label.data.materials.append(label_mat)
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
    scene.render.resolution_x,scene.render.resolution_y=1400,1000
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    preview=AUTHOR/'WornRetainers_Preview.png'
    scene.render.filepath=str(preview)
    for image in bpy.data.images:
        if image.source=='FILE':image.pack()
    blend=AUTHOR/'RetainerWornModels.blend'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.render.render(write_still=True)
    manifest={'schema':1,'version':(ROOT/'VERSION').read_text(encoding='utf-8').strip(),
              'tool':'Blender '+bpy.app.version_string,'format':'DirectX text xof 0303txt 0032; static, no skin or animation',
              'attachment':'Bip01_Head','axes':'Native X up, Y lateral, Z forward; editable Blender Z up, X lateral, -Y forward',
              'provenance':'Original procedural meshes using original project atlases. Schematic heads are original preview helpers and never shipped.',
              'runtime':'NOT TESTED in PZ; head coordinates estimated from read-only vanilla accessory bounds; clipping/fit are runtime gates.',
              'entries':entries,'authoring_files':{blend.name:sha(blend),preview.name:sha(preview)},
              'generator_sha256':sha(Path(__file__)), 'helper_sha256':sha(ROOT/'scripts/build_retainer_ground_models.py')}
    (AUTHOR/'worn-models.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Exported six original static worn meshes, editable master, preview and provenance')


if __name__=='__main__':
    main()

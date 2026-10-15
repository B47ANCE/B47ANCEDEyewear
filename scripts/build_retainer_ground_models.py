"""Author original static ground assets with Blender 4.5 LTS bpy (authoring only).

Run with a Python installation containing bpy; no game or addon is required.
Exports selected meshes only, preserves the earlier OBJ/icon sources, and saves
an editable .blend plus an offline preview outside the runtime source tree.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import shutil

import bpy
import bmesh
import addon_utils
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'assets/retainers/ground'
RUNTIME = ROOT / 'src/B47ANCEDEyewear/42'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def material(name, palette):
    """Original woven/grain atlas; four horizontal material bands."""
    image = bpy.data.images.new(name, width=128, height=128, alpha=True)
    pixels = []
    for y in range(128):
        color = palette[min(y // 32, 3)]
        for x in range(128):
            grain = 0.94 + 0.06 * ((x * 7 + y * 13) % 11) / 10
            weave = 0.94 if (x % 4 == 0 or y % 4 == 0) else 1.0
            pixels.extend([c * grain * weave for c in color] + [1.0])
    image.pixels = pixels
    image.filepath_raw = str(RUNTIME / 'media/textures/WorldItems' / (name + '.png'))
    image.file_format = 'PNG'
    image.save()
    return image


def use_image(image, name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Roughness'].default_value = 0.85
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image = image
    mat.node_tree.links.new(tex.outputs['Color'], shader.inputs['Base Color'])
    return mat


def mesh(name, verts, faces, band=0):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    uv = data.uv_layers.new(name='UVMap')
    for poly in data.polygons:
        for j, loop in enumerate(poly.loop_indices):
            uv.data[loop].uv = ((j % 2) * 0.9 + 0.05, (band + (0.15 if j < 2 else 0.85)) / 4)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    return obj


def ribbon(name, points, width, thickness, band=0):
    verts = []
    for i, point in enumerate(points):
        tangent = Vector(points[min(i + 1, len(points) - 1)]) - Vector(points[max(0, i - 1)])
        side = Vector((-tangent.y, tangent.x, 0)).normalized() * width / 2
        p = Vector(point)
        for offset, z in ((-side, -thickness / 2), (side, -thickness / 2),
                          (side, thickness / 2), (-side, thickness / 2)):
            verts.append(tuple(p + offset + Vector((0, 0, z))))
    faces = [(3, 2, 1, 0)]
    for i in range(len(points) - 1):
        for j in range(4):
            a = i * 4 + j
            b = i * 4 + (j + 1) % 4
            faces.append((a, b, b + 4, a + 4))
    k = (len(points) - 1) * 4
    faces.append((k, k + 1, k + 2, k + 3))
    return mesh(name, verts, faces, band)


def loop(name, center, rx, ry, radius, band):
    verts, faces = [], []
    for i in range(24):
        a = i * math.tau / 24
        outward = Vector((math.cos(a), math.sin(a), 0))
        p = Vector(center) + Vector((rx * math.cos(a), ry * math.sin(a), 0))
        for j in range(6):
            b = j * math.tau / 6
            verts.append(tuple(p + outward * radius * math.cos(b) + Vector((0, 0, radius * math.sin(b)))))
    for i in range(24):
        for j in range(6):
            faces.append((i * 6 + j, ((i + 1) % 24) * 6 + j,
                          ((i + 1) % 24) * 6 + (j + 1) % 6, i * 6 + (j + 1) % 6))
    return mesh(name, verts, faces, band)


def finish(parts, name, mat):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = parts[0]
    obj.name = name
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    bm.free()
    coords = [v.co for v in obj.data.vertices]
    offset = Vector(((min(v.x for v in coords) + max(v.x for v in coords)) / 2,
                     (min(v.y for v in coords) + max(v.y for v in coords)) / 2,
                     min(v.z for v in coords) - 0.001))
    for vert in obj.data.vertices:
        vert.co -= offset
    obj.location = (0, 0, 0)
    obj.data.update()
    if any(p.area <= 1e-12 for p in obj.data.polygons):
        raise ValueError('Degenerate triangle: ' + name)
    if len(obj.data.uv_layers.active.data) != len(obj.data.loops):
        raise ValueError('Missing UV coordinates: ' + name)
    return obj


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only-unbreakable', action='store_true',
                        help='Preserve existing cloth/leather FBX exports while rebuilding the cord and preview')
    args = parser.parse_args()
    AUTHOR.mkdir(parents=True, exist_ok=True)
    for directory in ('media/models_X/WorldItems', 'media/textures/WorldItems'):
        (RUNTIME / directory).mkdir(parents=True, exist_ok=True)
    addon_utils.enable('io_scene_fbx', default_set=False)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    cloth_image = material('B47ANCEDEyewearClothRetainerGround',
                           [(0.72, 0.64, 0.49), (0.87, 0.80, 0.65), (0.54, 0.45, 0.32), (0.70, 0.62, 0.47)])
    leather_image = material('B47ANCEDEyewearLeatherRetainerGround',
                             [(0.24, 0.09, 0.035), (0.66, 0.44, 0.22), (0.035, 0.04, 0.045), (0.40, 0.19, 0.07)])
    models = []
    for kind, width, thick, image in [('Cloth', 0.010, 0.0015, cloth_image), ('Leather', 0.0065, 0.002, leather_image)]:
        points = []
        for i in range(33):
            a = i * math.pi / 32
            points.append((-0.065 * math.cos(a), -0.082 * math.sin(a), 0.0035 + (0.0012 * math.sin(a * 5) if kind == 'Cloth' else 0)))
        parts = [ribbon(kind + 'Strap', points, width, thick)]
        for x in (-0.065, 0.065):
            parts.append(loop(kind + 'EndLoop', (x, 0.002, 0.004), 0.005, 0.010, 0.0017, 0 if kind == 'Cloth' else 2))
            if kind == 'Cloth':
                parts.append(loop('ClothKnot', (x, -0.008, 0.005), 0.0045, 0.002, 0.0018, 1))
        if kind == 'Leather':
            for i in range(1, 32, 2):
                a = i * math.pi / 32
                for side in (-1, 1):
                    radius = 0.065 + side * 0.0022
                    x, y = -radius * math.cos(a), -(0.082 + side * 0.0022) * math.sin(a)
                    parts.append(ribbon('Stitch', [(x - 0.0006, y, 0.0047), (x + 0.0006, y, 0.0047)], 0.00035, 0.00025, 1))
        obj = finish(parts, 'B47ANCEDEyewear' + kind + 'RetainerGround', use_image(image, kind))
        models.append((obj, 'MakeshiftRetainer' if kind == 'Cloth' else 'EyewearRetainer', kind + 'RetainerGround'))
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.wm.obj_import(filepath=str(ROOT / 'assets/retainers/B47ANCEDEyewearRetainer.obj'), forward_axis='NEGATIVE_Z', up_axis='Y')
    parts = list(bpy.context.selected_objects)
    rare_path = RUNTIME / 'media/textures/WorldItems/B47ANCEDEyewearUnbreakableRetainerGround.png'
    shutil.copyfile(ROOT / 'assets/retainers/B47ANCEDEyewearRetainer_Texture.png', rare_path)
    rare = finish(parts, 'B47ANCEDEyewearUnbreakableRetainerGround', use_image(bpy.data.images.load(str(rare_path)), 'Unbreakable'))
    bpy.context.view_layer.update()
    # Match the crafted retainers' footprint, rather than the old worn-source size.
    # Bake the resize into the derived mesh; preserve the original OBJ and atlas.
    target_width = sum(obj.dimensions.x for obj, _, _ in models) / len(models)
    target_depth = sum(obj.dimensions.y for obj, _, _ in models) / len(models)
    scale_x, scale_y = target_width / rare.dimensions.x, target_depth / rare.dimensions.y
    for vertex in rare.data.vertices:
        vertex.co.x *= scale_x
        vertex.co.y *= scale_y
        vertex.co.z = (vertex.co.z - 0.001) * min(scale_x, scale_y) + 0.001
    rare.data.update()
    models.append((rare, 'UnbreakableRetainer', 'UnbreakableRetainerGround'))
    entries = []
    for obj, item, model in models:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        destination = RUNTIME / ('media/models_X/WorldItems/' + obj.name + '.fbx')
        if not args.only_unbreakable or item == 'UnbreakableRetainer':
            bpy.ops.export_scene.fbx(filepath=str(destination), use_selection=True, object_types={'MESH'},
                                    axis_forward='-Z', axis_up='Y', global_scale=1.0, apply_unit_scale=True,
                                    apply_scale_options='FBX_SCALE_ALL', bake_space_transform=False,
                                    bake_anim=False, add_leaf_bones=False, path_mode='STRIP', embed_textures=False)
        elif not destination.is_file():
            raise ValueError('Missing preserved crafted FBX: ' + str(destination))
        bpy.context.view_layer.update()
        original = tuple(obj.dimensions)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.fbx(filepath=str(destination))
        imported = list(bpy.context.selected_objects)
        if len(imported) != 1 or imported[0].type != 'MESH':
            raise ValueError('Unexpected FBX contents')
        bpy.context.view_layer.update()
        measured = tuple(imported[0].dimensions)
        if any(abs(a - b) > 0.00001 for a, b in zip(original, measured)):
            raise ValueError('FBX roundtrip dimension drift: ' + repr((original, measured)))
        for temp in imported:
            bpy.data.objects.remove(temp, do_unlink=True)
        texture = RUNTIME / ('media/textures/WorldItems/' + obj.name + '.png')
        entries.append({'item': 'B47ANCEDEyewear.' + item, 'model': 'B47ANCEDEyewear.' + model,
                        'mesh': destination.relative_to(RUNTIME).as_posix(), 'mesh_sha256': sha(destination),
                        'texture': texture.relative_to(RUNTIME).as_posix(), 'texture_sha256': sha(texture),
                        'vertices': len(obj.data.vertices), 'triangles': len(obj.data.polygons),
                        'dimensions_metres': list(original), 'roundtrip_dimensions_metres': list(measured),
                        'uv_layers': len(obj.data.uv_layers), 'fbx_roundtrip': 'PASS'})
    # Offline presentation only: scene layout is separate from the origin-centred exports.
    for i, (obj, item, model) in enumerate(models):
        obj.location.x = (i - 1) * 0.215
        bpy.ops.object.text_add(location=((i - 1) * 0.215, -0.11, 0.001))
        label = bpy.context.object
        label.data.body = ['CLOTH', 'LEATHER', 'UNBREAKABLE'][i]
        label.data.align_x = 'CENTER'
        label.data.size = 0.012
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.001))
    plane = bpy.context.object
    mat = bpy.data.materials.new('Preview background')
    mat.diffuse_color = (0.19, 0.22, 0.25, 1)
    plane.data.materials.append(mat)
    bpy.ops.object.camera_add(location=(0, -0.50, 0.67))
    camera = bpy.context.object
    aim(camera, (0, -0.035, 0))
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 0.69
    scene.camera = camera
    for location, energy, size in [((0, -0.3, 0.6), 18, 0.6), ((0.25, 0.2, 0.4), 9, 0.4)]:
        bpy.ops.object.light_add(type='AREA', location=location)
        light = bpy.context.object
        light.data.energy, light.data.shape, light.data.size = energy, 'DISK', size
        aim(light, (0, 0, 0))
    scene.world = bpy.data.worlds.new('Preview world')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (0.3, 0.3, 0.3, 1)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.render.resolution_x, scene.render.resolution_y = 1400, 600
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    preview = AUTHOR / 'GroundRetainers_Preview.png'
    scene.render.filepath = str(preview)
    bpy.data.orphans_purge(do_recursive=True)
    for image in bpy.data.images:
        if image.source == 'FILE':
            image.pack()
    blend = AUTHOR / 'RetainerGroundModels.blend'
    scene.render.film_transparent = False
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.render.render(write_still=True)
    manifest = {'schema': 1, 'version': (ROOT / 'VERSION').read_text(encoding='utf-8').strip(),
                'tool': 'Blender ' + bpy.app.version_string, 'units': 'metres; XY ground plane; Z up in editable source',
                'fbx': 'Binary, -Z forward / Y up, FBX_SCALE_ALL, standard axis transform, no bones/animation',
                'provenance': 'Original cloth/leather procedural geometry and atlases; rare mesh/atlas derived from existing original authoring assets. No vanilla/third-party geometry copied.',
                'runtime': 'NOT TESTED in Project Zomboid; final importer orientation, scale and lighting remain runtime gates.',
                'cord_resize': {'target_footprint_metres': [target_width, target_depth],
                                'axes_scale': [scale_x, scale_y, min(scale_x, scale_y)],
                                'reason': 'Match mean crafted-retainer width/depth; preserve original source and runtime texture'},
                'entries': entries, 'authoring_files': {blend.name: sha(blend), preview.name: sha(preview)},
                'generator_sha256': sha(Path(__file__))}
    (AUTHOR / 'ground-models.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()

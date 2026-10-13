"""Produce original model source and an alpha-preserving inventory icon.

These assets remain outside runtime source until native attachment/fit validation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import struct
import zlib
from PIL import Image


ASSETS = Path(__file__).resolve().parents[1] / 'assets/retainers'


def write_png(path, width, height, pixels):
    def chunk(kind, payload):
        return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', zlib.crc32(kind + payload))
    data = b''.join(b'\x00' + pixels[y*width*4:(y+1)*width*4] for y in range(height))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width,height,8,6,0,0,0)) +
                     chunk(b'IDAT', zlib.compress(data)) + chunk(b'IEND', b''))


def build(sprite_source):
    ASSETS.mkdir(parents=True, exist_ok=True)
    if sprite_source:
        image = Image.open(sprite_source)
        if image.mode != 'RGBA' or image.getchannel('A').getextrema()[0] != 0:
            raise ValueError('Generated sprite must have real alpha transparency')
        image.save(ASSETS / 'EyewearRetainer_Inventory_Source.png')
        image.thumbnail((60,60), Image.Resampling.LANCZOS)
        icon = Image.new('RGBA',(64,64))
        icon.paste(image, ((64-image.width)//2, (64-image.height)//2))
        icon.save(ASSETS / 'Item_B47ANCEDEyewearRetainer.png')
    # Original technical color atlas: cord, rubber loops, adjustment slider.
    colors = [(52,55,59,255), (31,34,38,255), (74,78,83,255)]
    write_png(ASSETS / 'B47ANCEDEyewearRetainer_Texture.png', 128,32,
              bytes(component for _y in range(32) for x in range(128) for component in colors[x*3//128]))
    positions, normals, uvs, triangles = [], [], [], []
    parts = []

    def tube(name, points, radius, sides, stripe, inner=None):
        start_vertex, start_triangle = len(positions), len(triangles)
        rings = []
        tangents = []
        for index, point in enumerate(points):
            tangent = tuple(points[min(index+1,len(points)-1)][k]-points[max(index-1,0)][k] for k in range(3))
            length = math.sqrt(sum(v*v for v in tangent))
            tangent = tuple(v/length for v in tangent)
            tangents.append(tangent)
            reference = (0,1,0) if abs(tangent[1]) < .95 else (1,0,0)
            a = (tangent[1]*reference[2]-tangent[2]*reference[1],
                 tangent[2]*reference[0]-tangent[0]*reference[2],
                 tangent[0]*reference[1]-tangent[1]*reference[0])
            length = math.sqrt(sum(v*v for v in a)); a = tuple(v/length for v in a)
            b = (tangent[1]*a[2]-tangent[2]*a[1], tangent[2]*a[0]-tangent[0]*a[2], tangent[0]*a[1]-tangent[1]*a[0])
            ring = []
            for side in range(sides):
                angle = 2*math.pi*side/sides
                normal = tuple(a[k]*math.cos(angle)+b[k]*math.sin(angle) for k in range(3))
                ring.append(len(positions))
                positions.append(tuple(point[k]+radius*normal[k] for k in range(3)))
                normals.append(normal); uvs.append(((stripe+.5)/3, .5))
            rings.append(ring)
        for previous, current in zip(rings, rings[1:]):
            for side in range(sides):
                nxt = (side+1)%sides
                triangles.extend([(previous[side], previous[nxt], current[nxt]), (previous[side], current[nxt], current[side])])
        if inner:
            inner_rings=[]
            for ring, point in zip(rings, points):
                ids=[]
                for outer in ring:
                    ids.append(len(positions)); n=normals[outer]
                    positions.append(tuple(point[k]+inner*n[k] for k in range(3)))
                    normals.append(tuple(-v for v in n)); uvs.append(((stripe+.5)/3,.5))
                inner_rings.append(ids)
            for previous,current in zip(inner_rings,inner_rings[1:]):
                for side in range(sides):
                    nxt=(side+1)%sides
                    triangles.extend([(previous[side], current[nxt], previous[nxt]),(previous[side], current[side],current[nxt])])
            for cap in (0,-1):
                normal = tuple(v*(-1 if cap==0 else 1) for v in tangents[cap])
                cap_outer, cap_inner = [], []
                for outer, inside in zip(rings[cap], inner_rings[cap]):
                    cap_outer.append(len(positions)); positions.append(positions[outer]); normals.append(normal); uvs.append(uvs[outer])
                    cap_inner.append(len(positions)); positions.append(positions[inside]); normals.append(normal); uvs.append(uvs[inside])
                for side in range(sides):
                    nxt=(side+1)%sides
                    face=(cap_outer[side],cap_inner[side],cap_inner[nxt],cap_outer[nxt])
                    if cap==-1: face=face[::-1]
                    triangles.extend([(face[0],face[1],face[2]),(face[0],face[2],face[3])])
        else:
            for cap in (0,-1):
                normal = tuple(v*(-1 if cap==0 else 1) for v in tangents[cap])
                ids=[]
                for original in rings[cap]:
                    ids.append(len(positions)); positions.append(positions[original]); normals.append(normal); uvs.append(uvs[original])
                for side in range(1,sides-1):
                    face=(ids[0],ids[side],ids[side+1])
                    triangles.append(face[::-1] if cap==0 else face)
        parts.append({'name':name,'vertices':len(positions)-start_vertex,'triangles':len(triangles)-start_triangle})

    # Author-created provisional head-local geometry, metres; no vanilla mesh copied.
    curve=[]
    for index in range(25):
        t=math.pi*index/24
        curve.append((-.078*math.cos(t), -.018*math.sin(t), .040-.153*math.sin(t)))
    tube('Cord',curve,.0018,6,0)
    for x, name in [(-.078,'LeftTempleSleeve'),(.078,'RightTempleSleeve')]:
        tube(name,[(x,0,.035),(x,0,.071)],.0048,8,1,inner=.0028)
    tube('AdjustmentSlider',[(-.006,-.018,-.113),(.006,-.018,-.113)],.0042,8,2,inner=.002)
    model=ASSETS/'B47ANCEDEyewearRetainer.obj'
    lines=['# Original provisional eyewear-retainer mesh. Metres, Y up; fit NOT TESTED.',
           'mtllib B47ANCEDEyewearRetainer.mtl', 'o B47ANCEDEyewearRetainer']
    lines += ['v '+' '.join(f'{v:.8f}' for v in point) for point in positions]
    lines += ['vt '+' '.join(f'{v:.8f}' for v in point) for point in uvs]
    lines += ['vn '+' '.join(f'{v:.8f}' for v in point) for point in normals]
    lines += ['usemtl RetainerAtlas']
    lines += ['f '+' '.join(f'{index+1}/{index+1}/{index+1}' for index in face) for face in triangles]
    model.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (ASSETS/'B47ANCEDEyewearRetainer.mtl').write_text(
        'newmtl RetainerAtlas\nKa 0.1 0.1 0.1\nKd 1 1 1\nKs 0.1 0.1 0.1\nNs 16\nmap_Kd B47ANCEDEyewearRetainer_Texture.png\n',encoding='utf-8')
    # glTF 2.0 binary preview/source; not claimed to be a PZ runtime model format.
    binary=bytearray(); views=[]; accessors=[]
    def section(payload, target=None):
        while len(binary)%4: binary.append(0)
        offset=len(binary); binary.extend(payload)
        view={'buffer':0,'byteOffset':offset,'byteLength':len(payload)}
        if target: view['target']=target
        views.append(view); return len(views)-1
    for values, kind in [(positions,'VEC3'),(normals,'VEC3'),(uvs,'VEC2')]:
        flat=[x for row in values for x in row]
        view=section(struct.pack('<'+'f'*len(flat),*flat),34962)
        accessor={'bufferView':view,'componentType':5126,'count':len(values),'type':kind}
        if values is positions:
            accessor.update(min=[min(row[k] for row in values) for k in range(3)],max=[max(row[k] for row in values) for k in range(3)])
        accessors.append(accessor)
    indices=[index for face in triangles for index in face]
    accessors.append({'bufferView':section(struct.pack('<'+'H'*len(indices),*indices),34963),
                      'componentType':5123,'count':len(indices),'type':'SCALAR'})
    image_view=section((ASSETS/'B47ANCEDEyewearRetainer_Texture.png').read_bytes())
    gltf={'asset':{'version':'2.0','generator':'Original B47ANCEDEyewear asset builder'},
          'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0,'name':'B47ANCEDEyewearRetainer'}],
          'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'TEXCOORD_0':2},'indices':3,'material':0}]}],
          'materials':[{'pbrMetallicRoughness':{'baseColorTexture':{'index':0},'metallicFactor':0,'roughnessFactor':.85},'doubleSided':False}],
          'textures':[{'source':0,'sampler':0}],'samplers':[{'magFilter':9729,'minFilter':9729,'wrapS':33071,'wrapT':33071}],
          'images':[{'bufferView':image_view,'mimeType':'image/png'}],
          'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors}
    encoded=json.dumps(gltf,separators=(',',':')).encode()
    encoded += b' '*((-len(encoded))%4); binary += b'\x00'*((-len(binary))%4)
    payload=struct.pack('<II',len(encoded),0x4E4F534A)+encoded+struct.pack('<II',len(binary),0x004E4942)+binary
    (ASSETS/'B47ANCEDEyewearRetainer.glb').write_bytes(struct.pack('<III',0x46546C67,2,len(payload)+12)+payload)
    manifest={'status':'SOURCE ASSETS ONLY — PZ import/attachment/fit NOT TESTED',
              'model_vertices':len(positions),'model_triangles':len(triangles),
              'parts':parts,'units':'metres','source_axes':'Y up, Z forward (provisional; calibrate against vanilla export)',
              'attachment_bone':'Bip01_Head (verified vanilla XML; not applied in a game asset yet)',
              'sprite_dimensions':[64,64],'texture_dimensions':[128,32],
              'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ASSETS.iterdir()) if f.is_file() and f.suffix in ['.png','.obj','.mtl','.glb']}}
    (ASSETS/'asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'Created original {len(positions)}-vertex/{len(triangles)}-triangle source model and RGBA inventory icon.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--sprite-source',type=Path)
    args=parser.parse_args(); build(args.sprite_source)

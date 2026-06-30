#!/usr/bin/env python3
"""Generate GLBs: textured painting + white frame (using trimesh with separate materials)."""
import os, sys, io, re, json, struct, urllib.request, urllib.parse, base64
from PIL import Image
import trimesh
import numpy as np

BASE = r'C:\Users\Hauska\jiri-hauschka-next'
ARTS = os.path.join(BASE, 'lib', 'artworks.js')
ASSETS = os.path.join(BASE, 'public', 'assets')

def encode_url(url):
    parsed = list(urllib.parse.urlsplit(url))
    parsed[2] = urllib.parse.quote(urllib.parse.unquote(parsed[2]), safe='/:@!$&\'()*+,;=-._~%')
    return urllib.parse.urlunsplit(parsed)

def download_image(url):
    encoded = encode_url(url)
    req = urllib.request.Request(encoded, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=30).read()
    img = Image.open(io.BytesIO(data)).convert('RGB')
    if max(img.size) > 2048:
        ratio = 2048 / max(img.size)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    return img

def create_glb(img, out_path):
    w_px, h_px = img.size
    scale = 1.0 / max(w_px, h_px) * 0.9
    w, h = w_px * scale, h_px * scale
    fw, fd = 0.02, 0.04
    half_w, half_h = w / 2, h / 2
    
    # Save texture to PNG bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    tex_data = buf.getvalue()
    
    # --- Build raw GLTF ---
    # Vertices: painting (4) + frame (32 = 4 boxes * 8 verts)
    pv = [
        [-half_w, -half_h, 0], [half_w, -half_h, 0],
        [half_w, half_h, 0], [-half_w, half_h, 0]
    ]
    
    fv = []
    fi = []
    
    def box(cx, cy, bw, bh, bd):
        off = len(fv)
        hbw, hbh, hbd = bw/2, bh/2, bd/2
        for dz in [-hbd, hbd]:
            for dx in [-hbw, hbw]:
                for dy in [-hbh, hbh]:
                    # Need to order vertices for proper faces
                    pass
        # Simple box with 8 verts and 12 tris
        v = [
            [cx-hbw, cy-hbh, -hbd], [cx+hbw, cy-hbh, -hbd],
            [cx+hbw, cy+hbh, -hbd], [cx-hbw, cy+hbh, -hbd],
            [cx-hbw, cy-hbh, hbd], [cx+hbw, cy-hbh, hbd],
            [cx+hbw, cy+hbh, hbd], [cx-hbw, cy+hbh, hbd],
        ]
        f = [
            off, off+1, off+2,  off, off+2, off+3,
            off+4, off+6, off+5,  off+4, off+7, off+6,
            off, off+4, off+5,  off, off+5, off+1,
            off+1, off+5, off+6,  off+1, off+6, off+2,
            off+2, off+6, off+7,  off+2, off+7, off+3,
            off+3, off+7, off+4,  off+3, off+4, off,
        ]
        fv.extend(v)
        fi.extend(f)
    
    box(0, half_h + fw/2, w + 2*fw, fw, fd)
    box(0, -half_h - fw/2, w + 2*fw, fw, fd)
    box(-half_w - fw/2, 0, fw, h, fd)
    box(half_w + fw/2, 0, fw, h, fd)
    
    all_v = pv + fv
    p_idx = [0, 1, 2, 0, 2, 3]
    f_idx = [i + 4 for i in fi]
    
    # Interleave: positions + UVs for painting, positions for frame
    # Positions: all vertices (4 + 32 = 36)
    pos_data = bytearray()
    for v in all_v:
        pos_data.extend(struct.pack('fff', *v))
    
    # UV data: only for painting (4 verts)
    uv_data = bytearray()
    for u in [[0,0],[1,0],[1,1],[0,1]]:
        uv_data.extend(struct.pack('ff', *u))
    
    # Index data: painting (6) + frame
    idx_data = bytearray()
    for i in p_idx:
        idx_data.extend(struct.pack('H', i))
    for i in f_idx:
        idx_data.extend(struct.pack('H', i))
    
    # Pad to 4 bytes
    while len(pos_data) % 4: pos_data.append(0)
    while len(uv_data) % 4: uv_data.append(0)
    while len(idx_data) % 4: idx_data.append(0)
    
    # Buffer 0: positions + UVs + indices
    buf0 = pos_data + uv_data + idx_data
    
    # Texture size
    tex_b64 = base64.b64encode(tex_data).decode('ascii')
    
    pos_len = len(pos_data)
    uv_len = len(uv_data)
    idx_len = len(idx_data)
    p_idx_count = len(p_idx)
    f_idx_count = len(fi)
    
    gltf = {
        "asset": {"version": "2.0", "generator": "hermes-ar"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [
            {
                "attributes": {"POSITION": 0, "TEXCOORD_0": 1},
                "indices": 2, "material": 0
            },
            {
                "attributes": {"POSITION": 0},
                "indices": 3, "material": 1
            }
        ]}],
        "accessors": [
            {"bufferView": 0, "byteOffset": 0, "componentType": 5126, "count": len(all_v), "type": "VEC3"},
            {"bufferView": 1, "byteOffset": 0, "componentType": 5126, "count": 4, "type": "VEC2"},
            {"bufferView": 2, "byteOffset": 0, "componentType": 5123, "count": p_idx_count, "type": "SCALAR"},
            {"bufferView": 2, "byteOffset": p_idx_count*2, "componentType": 5123, "count": f_idx_count, "type": "SCALAR"},
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": pos_len, "target": 34962},
            {"buffer": 0, "byteOffset": pos_len, "byteLength": uv_len, "target": 34962},
            {"buffer": 0, "byteOffset": pos_len + uv_len, "byteLength": idx_len, "target": 34963},
        ],
        "textures": [{"source": 0, "sampler": 0}],
        "images": [{"mimeType": "image/png", "uri": f"data:image/png;base64,{tex_b64}"}],
        "samplers": [{"magFilter": 9729, "minFilter": 9987}],
        "materials": [
            {
                "name": "Painting",
                "pbrMetallicRoughness": {
                    "baseColorTexture": {"index": 0},
                    "baseColorFactor": [1.0, 1.0, 1.0, 1.0],
                    "metallicFactor": 0.0, "roughnessFactor": 0.85
                }
            },
            {
                "name": "Frame",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [0.95, 0.93, 0.88, 1.0],
                    "metallicFactor": 0.0, "roughnessFactor": 0.7
                }
            }
        ],
        "buffers": [{"byteLength": len(buf0)}]
    }
    
    json_bytes = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
    while len(json_bytes) % 4: json_bytes += b' '
    while len(buf0) % 4: buf0.append(0)
    
    glb = b'glTF' + struct.pack('II', 2, 12)
    glb += struct.pack('I', len(json_bytes)) + b'JSON' + json_bytes
    glb += struct.pack('I', len(buf0)) + b'BIN' + bytes(buf0)
    glb = glb[:8] + struct.pack('I', len(glb)) + glb[12:]
    
    with open(out_path, 'wb') as f:
        f.write(glb)

def main():
    with open(ARTS, 'r', encoding='utf-8') as f:
        content = f.read()
    slugs = re.findall(r"slug:\s*'([^']+)'", content)
    images = re.findall(r"image:\s*'([^']+)'", content)
    
    for i, (slug, img_url) in enumerate(zip(slugs, images)):
        if slug == 'colored-moments':
            print(f'  SKIP: {slug}'); continue
        glb_path = os.path.join(ASSETS, f'{slug}.glb')
        print(f'  [{i+1}/47] {slug}...', end=' ')
        try:
            img = download_image(img_url)
            create_glb(img, glb_path)
            print(f'OK ({img.size[0]}x{img.size[1]})')
        except Exception as e:
            print(f'FAIL: {e}')
            import traceback; traceback.print_exc()

if __name__ == '__main__':
    main()

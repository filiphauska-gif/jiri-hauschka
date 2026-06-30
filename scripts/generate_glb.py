#!/usr/bin/env python3
"""Generate improved GLB models: correct aspect ratio, with frame."""
import os, sys, io, re, urllib.request, urllib.parse
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
    try:
        encoded = encode_url(url)
        req = urllib.request.Request(encoded, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        img = Image.open(io.BytesIO(data))
        return img.convert('RGB')
    except Exception as e:
        print(f'    DL ERROR: {e}')
        return None

def create_glb_with_frame(img, out_path):
    """Create a flat rectangle with image texture + thin frame"""
    w_px, h_px = img.size
    # Normalize: max dimension = 1m, keep aspect ratio
    max_dim = max(w_px, h_px)
    w = w_px / max_dim  # width in meters
    h = h_px / max_dim  # height in meters
    
    # Scale to a reasonable size (max ~1m for the longer side)
    scale = 1.0 / max_dim
    w, h = w_px * scale, h_px * scale
    
    frame_width = 0.015  # 1.5cm frame
    frame_depth = 0.03   # 3cm frame depth
    
    half_w, half_h = w / 2, h / 2
    
    # --- Painting surface (flat plane) ---
    verts = [
        [-half_w, -half_h, 0],
        [ half_w, -half_h, 0],
        [ half_w,  half_h, 0],
        [-half_w,  half_h, 0],
    ]
    faces = [[0, 1, 2], [0, 2, 3]]
    uvs = [[0, 0], [1, 0], [1, 1], [0, 1]]
    
    mesh = trimesh.Trimesh(
        vertices=np.array(verts, dtype=np.float32),
        faces=np.array(faces, dtype=np.int64),
    )
    
    # Save texture
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=92)
    buf.seek(0)
    texture = Image.open(buf)
    mesh.visual = trimesh.visual.TextureVisuals(
        uv=np.array(uvs, dtype=np.float32),
        image=texture
    )
    
    # --- Frame (4 sides) ---
    fw = frame_width
    fd = frame_depth
    frame_verts = []
    frame_faces = []
    
    # Frame corners (outer and inner)
    # Left side
    l = -half_w - fw
    r_outer = -half_w
    r_inner = -half_w
    # Actually let's do a simpler frame: just 4 thin boxes on each edge
    
    def add_box(cx, cy, bw, bh, bd):
        """Add a box at position, return vertex offset"""
        offset = len(frame_verts)
        hbw, hbh, hbd = bw/2, bh/2, bd/2
        v = [
            [cx-hbw, cy-hbh, -hbd], [cx+hbw, cy-hbh, -hbd],
            [cx+hbw, cy+hbh, -hbd], [cx-hbw, cy+hbh, -hbd],
            [cx-hbw, cy-hbh, hbd], [cx+hbw, cy-hbh, hbd],
            [cx+hbw, cy+hbh, hbd], [cx-hbw, cy+hbh, hbd],
        ]
        f = [
            [0,1,2],[0,2,3],[4,6,5],[4,7,6],
            [0,4,5],[0,5,1],[1,5,6],[1,6,2],
            [2,6,7],[2,7,3],[3,7,4],[3,4,0],
        ]
        frame_verts.extend(v)
        frame_faces.extend([[i+offset for i in tri] for tri in f])
        return offset
    
    # Top frame
    add_box(0, half_h + fw/2, w + 2*fw, fw, fd)
    # Bottom frame
    add_box(0, -half_h - fw/2, w + 2*fw, fw, fd)
    # Left frame
    add_box(-half_w - fw/2, 0, fw, h, fd)
    # Right frame
    add_box(half_w + fw/2, 0, fw, h, fd)
    
    if frame_verts:
        frame_mesh = trimesh.Trimesh(
            vertices=np.array(frame_verts, dtype=np.float32),
            faces=np.array(frame_faces, dtype=np.int64),
        )
        # Dark brown frame color
        frame_color = np.array([40, 30, 20, 255], dtype=np.uint8)
        frame_mesh.visual = trimesh.visual.ColorVisuals(frame_mesh, vertex_colors=frame_color)
        mesh = trimesh.util.concatenate([mesh, frame_mesh])
    
    mesh.export(out_path, file_type='glb')

def main():
    with open(ARTS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slugs = re.findall(r"slug:\s*'([^']+)'", content)
    images = re.findall(r"image:\s*'([^']+)'", content)
    
    total = len(slugs)
    ok = 0
    
    for i, (slug, img_url) in enumerate(zip(slugs, images)):
        glb_path = os.path.join(ASSETS, f'{slug}.glb')
        
        # Skip colored-moments (already has custom model)
        if slug == 'colored-moments':
            print(f'  SKIP (custom): {slug}')
            continue
        
        print(f'  [{i+1}/{total}] {slug}...', end=' ')
        img = download_image(img_url)
        if img is None:
            print('FAIL (download)')
            continue
        
        create_glb_with_frame(img, glb_path)
        print(f'OK ({img.size[0]}x{img.size[1]})')
        ok += 1
    
    print(f'\nDone: {ok} regenerated')

if __name__ == '__main__':
    main()

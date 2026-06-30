#!/usr/bin/env python3
"""Generate GLB 3D models for all artworks from their images."""
import os, sys, json, re, math, io, urllib.request
from PIL import Image
import trimesh
import numpy as np

BASE = r'C:\Users\Hauska\jiri-hauschka-next'
ARTS = os.path.join(BASE, 'lib', 'artworks.js')
ASSETS = os.path.join(BASE, 'public', 'assets')

def parse_size(size_str):
    """Parse '150 × 200 cm' -> (150, 200) in cm, or default 1:1"""
    if not size_str:
        return (1.0, 1.0)
    m = re.search(r'(\d+)\s*[×x]\s*(\d+)', size_str)
    if m:
        w, h = float(m.group(1)), float(m.group(2))
        # Normalize: keep ratio but max dimension = 1 meter (100cm)
        scale = max(w, h) / 100
        return (w / 100 / scale, h / 100 / scale)
    return (1.0, 1.0)

def download_image(url, max_size=1024):
    """Download image, resize if needed"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        img = Image.open(io.BytesIO(data))
        # Resize if too large (keep aspect ratio)
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
        return img
    except Exception as e:
        print(f'  Download failed: {e}')
        return None

def create_glb(image_url, out_path, real_w, real_h):
    """Create a GLB file: flat rectangle with image texture"""
    img = download_image(image_url)
    if img is None:
        return False
    
    # Use real-world proportions but cap at 1m
    max_dim = max(real_w, real_h)
    if max_dim == 0:
        max_dim = 1
    w = real_w / max_dim
    h = real_h / max_dim
    
    # Create a flat rectangular mesh (XY plane, facing +Z)
    half_w, half_h = w / 2, h / 2
    vertices = np.array([
        [-half_w, -half_h, 0],
        [ half_w, -half_h, 0],
        [ half_w,  half_h, 0],
        [-half_w,  half_h, 0],
    ], dtype=np.float32)
    
    faces = np.array([
        [0, 1, 2],
        [0, 2, 3],
    ], dtype=np.int64)
    
    # UV coordinates (texture mapping)
    uvs = np.array([
        [0, 0], [1, 0], [1, 1], [0, 1]
    ], dtype=np.float32)
    
    # Save texture as PNG in memory
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    texture = Image.open(buf)
    
    # Create mesh with material
    mesh = trimesh.Trimesh(
        vertices=vertices,
        faces=faces,
    )
    
    # Add UV coordinates
    mesh.visual = trimesh.visual.TextureVisuals(uv=uvs, image=texture)
    
    # Export as GLB
    mesh.export(out_path, file_type='glb')
    return True

def main():
    # Read artworks
    with open(ARTS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slugs = re.findall(r"slug:\s*'([^']+)'", content)
    titles = re.findall(r"title:\s*'([^']+)'", content)
    images = re.findall(r"image:\s*'([^']+)'", content)
    sizes = re.findall(r"size:\s*'([^']*)'", content)
    ar_flags = re.findall(r"ar:\s*(true|false)", content)
    
    total = len(slugs)
    ok = 0
    skip = 0
    
    for i, (slug, title, img_url, size_str, ar) in enumerate(zip(slugs, titles, images, sizes, ar_flags)):
        if ar == 'true':
            print(f'  SKIP (already has AR): {slug}')
            skip += 1
            continue
        
        glb_path = os.path.join(ASSETS, f'{slug}.glb')
        
        # Skip if already exists
        if os.path.exists(glb_path):
            print(f'  SKIP (exists): {slug}')
            skip += 1
            continue
        
        real_w, real_h = parse_size(size_str)
        if real_w == 0 or real_h == 0:
            real_w, real_h = 1.0, 1.0
        
        print(f'  [{i+1}/{total}] {slug} ({real_w:.2f}x{real_h:.2f}m)')
        
        if create_glb(img_url, glb_path, real_w, real_h):
            ok += 1
        else:
            print(f'    FAILED')
    
    print(f'\nDone: {ok} created, {skip} skipped, {total} total')

if __name__ == '__main__':
    main()

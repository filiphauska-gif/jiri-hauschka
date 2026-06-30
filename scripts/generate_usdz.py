#!/usr/bin/env python3
"""Generate USDZ files for all artworks (mirroring the GLB structure)."""
import os, sys, io, re, json, struct, zipfile, urllib.request, urllib.parse
from PIL import Image

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
    return img

def create_usdz(img, out_path):
    """Create a simple USDZ file with a textured plane + white frame"""
    w_px, h_px = img.size
    scale = 1.0 / max(w_px, h_px) * 0.9
    w, h = w_px * scale, h_px * scale
    fw, fd = 0.02, 0.04
    half_w, half_h = w/2, h/2
    
    # Save texture as JPEG
    tex_buf = io.BytesIO()
    img.save(tex_buf, format='JPEG', quality=92)
    tex_data = tex_buf.getvalue()
    tex_name = 'texture.jpg'
    
    # Build USDA content (human-readable USD format)
    # For simplicity, I'll generate the same geometry as the GLB
    # Painting: 4 vertices, 2 triangles
    pv = [
        (-half_w, -half_h, 0), (half_w, -half_h, 0),
        (half_w, half_h, 0), (-half_w, half_h, 0)
    ]
    puv = [(0,0), (1,0), (1,1), (0,1)]
    pvi = [0, 1, 2, 0, 2, 3]  # triangle indices
    
    # Frame: 4 boxes
    fv = []
    fvi = []
    
    def add_box(vlist, ilist, cx, cy, bw, bh, bd):
        off = len(vlist)
        hw, hh, hd = bw/2, bh/2, bd/2
        v = [
            (cx-hw, cy-hh, -hd), (cx+hw, cy-hh, -hd),
            (cx+hw, cy+hh, -hd), (cx-hw, cy+hh, -hd),
            (cx-hw, cy-hh, hd), (cx+hw, cy-hh, hd),
            (cx+hw, cy+hh, hd), (cx-hw, cy+hh, hd),
        ]
        f = [
            off, off+1, off+2,  off, off+2, off+3,
            off+4, off+6, off+5,  off+4, off+7, off+6,
            off, off+4, off+5,  off, off+5, off+1,
            off+1, off+5, off+6,  off+1, off+6, off+2,
            off+2, off+6, off+7,  off+2, off+7, off+3,
            off+3, off+7, off+4,  off+3, off+4, off,
        ]
        vlist.extend(v)
        ilist.extend(f)
    
    add_box(fv, fvi, 0, half_h+fw/2, w+2*fw, fw, fd)
    add_box(fv, fvi, 0, -half_h-fw/2, w+2*fw, fw, fd)
    add_box(fv, fvi, -half_w-fw/2, 0, fw, h, fd)
    add_box(fv, fvi, half_w+fw/2, 0, fw, h, fd)
    
    all_v = pv + fv
    p_faces = [(pvi[i], pvi[i+1], pvi[i+2]) for i in range(0, len(pvi), 3)]
    f_faces = [(fvi[i] + 4, fvi[i+1] + 4, fvi[i+2] + 4) for i in range(0, len(fvi), 3)]
    
    # Generate USDA text
    usda_lines = [
        '#usda 1.0',
        '()',
        'def Xform "Root" {',
        '  def Mesh "Painting" {',
        '    uniform bool doubleSided = 0',
        f'    int[] faceVertexCounts = [{", ".join("3" for _ in p_faces)}]',
        f'    int[] faceVertexIndices = [{", ".join(str(i) for tri in p_faces for i in tri)}]',
        f'    point3f[] points = [{", ".join(f"({v[0]:.6f}, {v[1]:.6f}, {v[2]:.6f})" for v in pv)}]',
        f'    texCoord2f[] primvars:st = [{", ".join(f"({u[0]:.6f}, {u[1]:.6f})" for u in puv)}]',
        '    int[] primvars:st:indices = [0, 1, 2, 0, 2, 3]',
        '    uniform token subdivisionScheme = "none"',
        '    rel material:binding = </Root/PaintingMat>',
        '  }',
        '  def Mesh "Frame" {',
        '    uniform bool doubleSided = 0',
        f'    int[] faceVertexCounts = [{", ".join("3" for _ in f_faces)}]',
        f'    int[] faceVertexIndices = [{", ".join(str(i) for tri in f_faces for i in tri)}]',
        f'    point3f[] points = [{", ".join(f"({v[0]:.6f}, {v[1]:.6f}, {v[2]:.6f})" for v in fv)}]',
        '    uniform token subdivisionScheme = "none"',
        '    rel material:binding = </Root/FrameMat>',
        '  }',
        '  def Material "PaintingMat" {',
        '    token inputs:frame:st.connect = </Root/Painting/primvars:st>',
        '    token outputs:surface.connect = </Root/PaintingMat/PBRShader.outputs:surface>',
        '    def Shader "PBRShader" {',
        '      uniform token info:id = "UsdPreviewSurface"',
        '      color3f inputs:diffuseColor.connect = </Root/PaintingMat/TextureReader.outputs:rgb>',
        '      float inputs:roughness = 0.85',
        '      float inputs:metallic = 0',
        '    }',
        '    def Shader "TextureReader" {',
        '      uniform token info:id = "UsdUVTexture"',
        '      asset inputs:file = @./texture.jpg@',
        '      float2 inputs:st.connect = </Root/Painting/primvars:st>',
        '      token inputs:wrapS = "repeat"',
        '      token inputs:wrapT = "repeat"',
        '      float3 outputs:rgb',
        '    }',
        '  }',
        '  def Material "FrameMat" {',
        '    token outputs:surface.connect = </Root/FrameMat/FrameShader.outputs:surface>',
        '    def Shader "FrameShader" {',
        '      uniform token info:id = "UsdPreviewSurface"',
        '      color3f inputs:diffuseColor = (0.95, 0.93, 0.88)',
        '      float inputs:roughness = 0.7',
        '      float inputs:metallic = 0',
        '    }',
        '  }',
        '}',
        '',
    ]
    
    usda_content = '\n'.join(usda_lines)
    
    # Create USDZ (zip archive)
    import zipfile
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('model.usda', usda_content)
        zf.writestr('texture.jpg', tex_data)

def main():
    with open(ARTS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slugs = re.findall(r"slug:\s*'([^']+)'", content)
    images = re.findall(r"image:\s*'([^']+)'", content)
    
    for i, (slug, img_url) in enumerate(zip(slugs, images)):
        if slug == 'colored-moments':
            print(f'  SKIP: {slug} (already has USDZ)')
            continue
        
        usdz_path = os.path.join(ASSETS, f'{slug}.usdz')
        print(f'  [{i+1}/47] {slug}...', end=' ')
        
        try:
            img = download_image(img_url)
            create_usdz(img, usdz_path)
            size = os.path.getsize(usdz_path)
            print(f'OK ({size/1024:.0f}KB)')
        except Exception as e:
            print(f'FAIL: {e}')

if __name__ == '__main__':
    main()

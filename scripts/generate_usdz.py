#!/usr/bin/env python3
"""Generate USDZ files matching colored-moments structure EXACTLY."""
import os, io, zipfile, re, urllib.request, urllib.parse
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
    return data

def create_usdz(texture_bytes, out_path, w_px, h_px):
    """Create USDZ matching colored-moments EXACT structure"""
    max_dim = max(w_px, h_px)
    w = w_px / max_dim * 0.9
    h = h_px / max_dim * 0.9
    hw, hh = w/2, h/2
    d = 0.025
    
    # 6 quad faces, 4 separate vertices per face (24 total)
    # Same vertex ordering as colored-moments
    pts = [
        # front face (textured)
        (-hw,-hh,d), (hw,-hh,d), (hw,hh,d), (-hw,hh,d),
        # back face
        (hw,-hh,-d), (-hw,-hh,-d), (-hw,hh,-d), (hw,hh,-d),
        # right face
        (hw,-hh,d), (hw,-hh,-d), (hw,hh,-d), (hw,hh,d),
        # left face
        (-hw,-hh,-d), (-hw,-hh,d), (-hw,hh,d), (-hw,hh,-d),
        # top face
        (-hw,hh,d), (hw,hh,d), (hw,hh,-d), (-hw,hh,-d),
        # bottom face
        (-hw,-hh,-d), (hw,-hh,-d), (hw,-hh,d), (-hw,-hh,d),
    ]
    
    # UV coords: each face has full 0-1 UVs (same as colored-moments)
    uv = [(0,0),(1,0),(1,1),(0,1)] * 6
    
    def fmt(v): return f"({v[0]:.6f},{v[1]:.6f},{v[2]:.6f})"
    def fmt2(v): return f"({v[0]:.6f},{v[1]:.6f})"
    
    pts_str = ','.join(fmt(p) for p in pts)
    uv_str = ','.join(fmt2(u) for u in uv)
    
    usda = f'''#usda 1.0
(
    defaultPrim = "Artwork"
    metersPerUnit = 1
    upAxis = "Y"
)

def Xform "Artwork"
{{
    def Mesh "Canvas"
    {{
        uniform token subdivisionScheme = "none"
        float3[] extent = [({-hw:.6f},{-hh:.6f},{-d:.6f}), ({hw:.6f},{hh:.6f},{d:.6f})]
        int[] faceVertexCounts = [4,4,4,4,4,4]
        int[] faceVertexIndices = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        point3f[] points = [{pts_str}]
        texCoord2f[] primvars:st = [{uv_str}] (
            interpolation = "varying"
        )
        rel material:binding = </ArtworkMaterial>
    }}
}}

def Material "ArtworkMaterial"
{{
    token outputs:surface.connect = </ArtworkMaterial/PreviewSurface.outputs:surface>
    def Shader "PreviewSurface"
    {{
        uniform token info:id = "UsdPreviewSurface"
        color3f inputs:diffuseColor.connect = </ArtworkMaterial/DiffuseTexture.outputs:rgb>
        float inputs:roughness = 0.82
        float inputs:metallic = 0
        token outputs:surface
    }}
    def Shader "DiffuseTexture"
    {{
        uniform token info:id = "UsdUVTexture"
        asset inputs:file = @texture.png@
        token inputs:wrapS = "clamp"
        token inputs:wrapT = "clamp"
        float2 inputs:st.connect = </ArtworkMaterial/PrimvarReader.outputs:result>
        token outputs:rgb
    }}
    def Shader "PrimvarReader"
    {{
        uniform token info:id = "UsdPrimvarReader_float2"
        token inputs:varname = "st"
        float2 outputs:result
    }}
}}
'''
    
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('model.usda', usda)
        zf.writestr('texture.jpg', texture_bytes)

def main():
    with open(ARTS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slugs = re.findall(r"slug:\s*'([^']+)'", content)
    images = re.findall(r"image:\s*'([^']+)'", content)
    
    for i, (slug, img_url) in enumerate(zip(slugs, images)):
        if slug == 'colored-moments':
            print(f'  SKIP: {slug}')
            continue
        
        usdz_path = os.path.join(ASSETS, f'{slug}.usdz')
        print(f'  [{i+1}] {slug}...', end=' ')
        
        try:
            data = download_image(img_url)
            img = Image.open(io.BytesIO(data))
            if max(img.size) > 2048:
                r = 2048 / max(img.size)
                img = img.resize((int(img.width*r), int(img.height*r)), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            create_usdz(buf.getvalue(), usdz_path, img.width, img.height)
            print(f'OK ({img.width}x{img.height})')
        except Exception as e:
            print(f'FAIL: {e}')

if __name__ == '__main__':
    main()

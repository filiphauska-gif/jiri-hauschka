#!/usr/bin/env python3
"""Generate USDZ files matching the colored-moments structure."""
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
    return data  # Keep raw bytes

def create_usdz(texture_bytes, out_path, w_px, h_px):
    """Create USDZ matching colored-moments structure"""
    max_dim = max(w_px, h_px)
    w = w_px / max_dim * 0.9  # Scale to 0.9m max
    h = h_px / max_dim * 0.9
    hw, hh = w/2, h/2
    d = 0.025  # depth like colored-moments
    
    # Box: 8 vertices, 12 triangles (6 quads split)
    # Front: 0,1,2,3 (textured), Back: 4,5,6,7, etc.
    pts = [
        (-hw,-hh,d), (hw,-hh,d), (hw,hh,d), (-hw,hh,d),  # front (textured)
        (hw,-hh,-d), (-hw,-hh,-d), (-hw,hh,-d), (hw,hh,-d),  # back
    ]
    uv = [
        (0,0),(1,0),(1,1),(0,1),
        (1,0),(0,0),(0,1),(1,1),  # back UVs (mirrored)
    ]
    # Triangles for each quad face
    faces = [
        0,1,2, 0,2,3,  # front
        4,7,6, 4,6,5,  # back
        1,5,6, 1,6,2,  # right
        0,4,7, 0,7,3,  # left
        2,6,7, 2,7,3,  # top
        0,1,5, 0,5,4,  # bottom
    ]
    
    def fmt(v): return f"({v[0]:.6f},{v[1]:.6f},{v[2]:.6f})"
    def fmt2(v): return f"({v[0]:.6f},{v[1]:.6f})"
    
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
        float3[] extent = [{fmt((-hw,-hh,-d))}, {fmt((hw,hh,d))}]
        int[] faceVertexCounts = [{','.join(['3']*12)}]
        int[] faceVertexIndices = [{','.join(str(i) for i in faces)}]
        point3f[] points = [{','.join(fmt(p) for p in pts)}]
        texCoord2f[] primvars:st = [{','.join(fmt2(u) for u in uv)}] (
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
        asset inputs:file = @texture.jpg@
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
        print(f'  [{i+1}/47] {slug}...', end=' ')
        
        try:
            data = download_image(img_url)
            img = Image.open(io.BytesIO(data))
            if max(img.size) > 2048:
                ratio = 2048 / max(img.size)
                img = img.resize((int(img.width*ratio), int(img.height*ratio)), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format='JPEG', quality=92)
            tex_data = buf.getvalue()
            
            create_usdz(tex_data, usdz_path, img.width, img.height)
            print(f'OK ({img.width}x{img.height})')
        except Exception as e:
            print(f'FAIL: {e}')
            import traceback; traceback.print_exc()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Master script: add missing artworks from old WP, generate GLB+USDZ models, write merged artworks.js."""
import os, sys, io, re, json, struct, zipfile, urllib.request, urllib.parse, base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

BASE = r'C:\Users\Hauska\jiri-hauschka-next'
ARTS = os.path.join(BASE, 'lib', 'artworks.js')
ASSETS = os.path.join(BASE, 'public', 'assets')
SCRIPTS = os.path.join(BASE, 'scripts')

# ---------- Load data ----------
with open(os.path.join(SCRIPTS, 'wp-missing3.json'), encoding='utf-8') as f:
    missing = json.load(f)
with open(os.path.join(SCRIPTS, 'wp-all-posts.json'), encoding='utf-8') as f:
    posts = json.load(f)
post_by_id = {str(p['id']): p for p in posts}

# Posts to SKIP (duplicates / mismatched images - verified visually or by phash)
SKIP_IDS = {'1274', '1250', '570', '1141', '1224', '1194', '1215', '1212', '1169', '1182', '1185'}

# 5 posts recovered from content images (no attached media)
RECOVERED = [
    {'id': '1254', 'url': 'https://jirihauschka.com/wp-content/uploads/2021/11/Jiri-Hauschka_Small-Town-Boy_2021_100x120cm.jpg',
     'url_fallback': 'https://jirihauschka.com/wp-content/uploads/2021/11/Jiri-Hauschka_Small-Town-Boy_2021_100x120cm-848x1024.jpg',
     'title': 'Small Town Boy', 'date': '2021-11-16', 'slug': 'small-town-boy'},
    {'id': '582', 'url': 'https://jirihauschka.com/wp-content/uploads/2017/01/White-river.jpg',
     'url_fallback': 'https://jirihauschka.com/wp-content/uploads/2017/01/White-river-683x1024.jpg',
     'title': 'White River', 'date': '2017-01-30', 'slug': 'white-river'},
    {'id': '579', 'url': 'https://jirihauschka.com/wp-content/uploads/2017/01/Tree-of-life.jpg',
     'url_fallback': 'https://jirihauschka.com/wp-content/uploads/2017/01/Tree-of-life-1024x721.jpg',
     'title': 'Tree of Life', 'date': '2017-01-30', 'slug': 'tree-of-life-2'},
    {'id': '576', 'url': 'https://jirihauschka.com/wp-content/uploads/2017/01/Silent-night.jpg',
     'url_fallback': 'https://jirihauschka.com/wp-content/uploads/2017/01/Silent-night-1024x725.jpg',
     'title': 'Silent Night', 'date': '2017-01-30', 'slug': 'silent-night'},
    {'id': '63', 'url': 'https://jirihauschka.com/wp-content/uploads/2015/04/2009-Battersea.jpg',
     'url_fallback': 'https://jirihauschka.com/wp-content/uploads/2015/04/2009-Battersea-1024x852.jpg',
     'title': 'Battersea', 'date': '2015-04-16', 'slug': 'battersea'},
]

def decode_entities(s):
    for a, b in [('&#8217;', '\u2019'), ('&#8216;', '\u2018'), ('&#8211;', '\u2013'), ('&#8212;', '\u2014'),
                 ('&#038;', '&'), ('&amp;', '&'), ('&nbsp;', ' '), ('&#215;', '\u00d7')]:
        s = s.replace(a, b)
    s = re.sub(r'&#?\w+;', '', s)
    return s.strip()

def slugify(t):
    import unicodedata
    t = unicodedata.normalize('NFKD', t)
    t = t.encode('ascii', 'ignore').decode()
    t = t.lower().replace('&', 'and')
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t

def extract_year(stem):
    for m in re.findall(r'(?<!\d)((?:19|20)\d{2})(?!\d)', stem):
        y = int(m)
        if 1990 <= y <= 2026:
            return str(y)
    return ''

def extract_size(stem):
    m = re.search(r'(\d{2,3})\s*[xX\u00d7]\s*(\d{2,3})', stem)
    if m:
        return f"{m.group(1)} \u00d7 {m.group(2)} cm"
    return ''

def stem_of(url):
    b = urllib.parse.unquote(url.split('/')[-1])
    b = re.sub(r'\.(jpg|jpeg|png)$', '', b, flags=re.I)
    b = re.sub(r'-\d+x\d+$', '', b)
    return b

# ---------- Build candidate list ----------
candidates = []
for item in missing:
    if str(item['id']) in SKIP_IDS:
        continue
    p = post_by_id[str(item['id'])]
    title = decode_entities(p['title'])
    url = item['url']
    stem = stem_of(url)
    date = p['date']
    year = extract_year(stem) or date[:4]
    size = extract_size(stem)
    candidates.append({'id': item['id'], 'title': title, 'slug': p.get('slug') or slugify(title),
                       'url': url, 'url_fallback': None, 'date': date, 'year': year, 'size': size})

for r in RECOVERED:
    stem = stem_of(r['url'])
    year = extract_year(stem) or r['date'][:4]
    size = extract_size(stem)
    candidates.append({'id': r['id'], 'title': r['title'], 'slug': r['slug'],
                       'url': r['url'], 'url_fallback': r['url_fallback'], 'date': r['date'],
                       'year': year, 'size': size})

print(f'Candidates to add: {len(candidates)}')

# ---------- Parse existing artworks.js ----------
with open(ARTS, encoding='utf-8') as f:
    arts_src = f.read()

existing = []
for block in re.finditer(r'\{\s*slug:\s*\'([^\']+)\',.*?poster:\s*\'([^\']*)\',\s*\}', arts_src, re.DOTALL):
    b = block.group(0)
    def g(field):
        m = re.search(field + r":\s*'([^']*)'", b)
        return m.group(1) if m else ''
    existing.append({
        'slug': block.group(1),
        'title': g('title'), 'year': g('year'), 'medium': g('medium'), 'size': g('size'),
        'image': g('image'), 'ar': True, 'usdz_path': g('usdz'),
    })
print(f'Existing entries parsed: {len(existing)}')

used_slugs = {e['slug'] for e in existing}

# resolve slug conflicts for new candidates
for c in candidates:
    slug = c['slug']
    if slug in used_slugs:
        slug2 = f"{slug}-{c['year']}" if c['year'] else slug + '-2'
        if slug2 in used_slugs:
            i = 2
            while f"{slug2}-{i}" in used_slugs:
                i += 1
            slug2 = f"{slug2}-{i}"
        c['slug'] = slug2
    used_slugs.add(c['slug'])

# ---------- Download helper ----------
def encode_url(url):
    parsed = list(urllib.parse.urlsplit(url))
    parsed[2] = urllib.parse.quote(urllib.parse.unquote(parsed[2]), safe='/:@!$&\'()*+,;=-._~%')
    return urllib.parse.urlunsplit(parsed)

def download_image(url, fallback=None, max_dim=1600):
    urls = [url] + ([fallback] if fallback else [])
    last_err = None
    for u in urls:
        try:
            encoded = encode_url(u)
            req = urllib.request.Request(encoded, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=60).read()
            img = Image.open(io.BytesIO(data)).convert('RGB')
            if max(img.size) > max_dim:
                ratio = max_dim / max(img.size)
                img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
            return img
        except Exception as e:
            last_err = e
    raise last_err

# ---------- GLB generator (compact: JPEG in buffer) ----------
def create_glb(img, out_path):
    w_px, h_px = img.size
    scale = 1.0 / max(w_px, h_px) * 0.9
    w, h = w_px * scale, h_px * scale
    fw, fd = 0.02, 0.04
    half_w, half_h = w / 2, h / 2

    jbuf = io.BytesIO()
    img.save(jbuf, format='JPEG', quality=88, optimize=True)
    jpg = jbuf.getvalue()

    pv = [[-half_w, -half_h, 0], [half_w, -half_h, 0], [half_w, half_h, 0], [-half_w, half_h, 0]]
    fv, fi = [], []

    def box(cx, cy, bw, bh, bd):
        off = len(fv)
        hbw, hbh, hbd = bw/2, bh/2, bd/2
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
        fv.extend(v); fi.extend(f)

    box(0, half_h + fw/2, w + 2*fw, fw, fd)
    box(0, -half_h - fw/2, w + 2*fw, fw, fd)
    box(-half_w - fw/2, 0, fw, h, fd)
    box(half_w + fw/2, 0, fw, h, fd)

    all_v = pv + fv
    p_idx = [0, 1, 2, 0, 2, 3]
    f_idx = [i + 4 for i in fi]

    pos_data = bytearray()
    for v in all_v:
        pos_data.extend(struct.pack('fff', *v))
    uv_data = bytearray()
    for u in [[0,0],[1,0],[1,1],[0,1]]:
        uv_data.extend(struct.pack('ff', *u))
    idx_data = bytearray()
    for i in p_idx:
        idx_data.extend(struct.pack('H', i))
    for i in f_idx:
        idx_data.extend(struct.pack('H', i))

    while len(pos_data) % 4: pos_data.append(0)
    while len(uv_data) % 4: uv_data.append(0)
    while len(idx_data) % 4: idx_data.append(0)

    buf0 = bytes(pos_data) + bytes(uv_data) + bytes(idx_data) + jpg
    img_offset = len(pos_data) + len(uv_data) + len(idx_data)
    total = len(buf0)
    if total % 4:
        buf0 += b'\x00' * (4 - total % 4)

    minv = [min(v[i] for v in all_v) for i in range(3)]
    maxv = [max(v[i] for v in all_v) for i in range(3)]

    gltf = {
        "asset": {"version": "2.0", "generator": "hermes-ar"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [
            {"attributes": {"POSITION": 0, "TEXCOORD_0": 1}, "indices": 2, "material": 0},
            {"attributes": {"POSITION": 0}, "indices": 3, "material": 1},
        ]}],
        "accessors": [
            {"bufferView": 0, "byteOffset": 0, "componentType": 5126, "count": len(all_v), "type": "VEC3",
             "min": [round(x, 6) for x in minv], "max": [round(x, 6) for x in maxv]},
            {"bufferView": 1, "byteOffset": 0, "componentType": 5126, "count": 4, "type": "VEC2"},
            {"bufferView": 2, "byteOffset": 0, "componentType": 5123, "count": len(p_idx), "type": "SCALAR"},
            {"bufferView": 2, "byteOffset": len(p_idx)*2, "componentType": 5123, "count": len(f_idx), "type": "SCALAR"},
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos_data), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos_data), "byteLength": len(uv_data), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos_data)+len(uv_data), "byteLength": len(idx_data), "target": 34963},
            {"buffer": 0, "byteOffset": img_offset, "byteLength": len(jpg)},
        ],
        "textures": [{"source": 0, "sampler": 0}],
        "images": [{"mimeType": "image/jpeg", "bufferView": 3}],
        "samplers": [{"magFilter": 9729, "minFilter": 9987}],
        "materials": [
            {"name": "Painting", "pbrMetallicRoughness": {
                "baseColorTexture": {"index": 0}, "baseColorFactor": [1.0, 1.0, 1.0, 1.0],
                "metallicFactor": 0.0, "roughnessFactor": 0.85}},
            {"name": "Frame", "pbrMetallicRoughness": {
                "baseColorFactor": [0.95, 0.93, 0.88, 1.0], "metallicFactor": 0.0, "roughnessFactor": 0.7}},
        ],
        "buffers": [{"byteLength": len(buf0)}],
    }

    json_bytes = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
    while len(json_bytes) % 4: json_bytes += b' '
    glb = b'glTF' + struct.pack('II', 2, 12)
    glb += struct.pack('I', len(json_bytes)) + b'JSON' + json_bytes
    glb += struct.pack('I', len(buf0)) + b'BIN\x00' + buf0
    glb = glb[:8] + struct.pack('I', len(glb)) + glb[12:]
    with open(out_path, 'wb') as f:
        f.write(glb)

# ---------- USDZ generator (PNG, STORED, CRLF, quads, PrimvarReader) ----------
USDA_TEMPLATE = '''#usda 1.0
(
    defaultPrim = "Artwork"
    metersPerUnit = 1
    upAxis = "Y"
)

def Xform "Artwork"
{
    def Mesh "Canvas"
    {
        uniform token subdivisionScheme = "none"
        float3[] extent = [{{EXTENT_MIN}}, {{EXTENT_MAX}}]
        int[] faceVertexCounts = [4,4,4,4,4,4]
        int[] faceVertexIndices = [
            0,1,2,3,
            4,5,6,7,
            8,9,10,11,
            12,13,14,15,
            16,17,18,19,
            20,21,22,23
        ]
        point3f[] points = [
            {{POINTS}}
        ]
        texCoord2f[] primvars:st = [
            (0,0),(1,0),(1,1),(0,1),
            (0,0),(1,0),(1,1),(0,1),
            (0,0),(1,0),(1,1),(0,1),
            (0,0),(1,0),(1,1),(0,1),
            (0,0),(1,0),(1,1),(0,1),
            (0,0),(1,0),(1,1),(0,1)
        ] (
            interpolation = "varying"
        )
        rel material:binding = </ArtworkMaterial>
    }
}

def Material "ArtworkMaterial"
{
    token outputs:surface.connect = </ArtworkMaterial/PreviewSurface.outputs:surface>
    def Shader "PreviewSurface"
    {
        uniform token info:id = "UsdPreviewSurface"
        color3f inputs:diffuseColor.connect = </ArtworkMaterial/DiffuseTexture.outputs:rgb>
        float inputs:roughness = 0.82
        float inputs:metallic = 0
        token outputs:surface
    }
    def Shader "DiffuseTexture"
    {
        uniform token info:id = "UsdUVTexture"
        asset inputs:file = @texture.png@
        token inputs:wrapS = "clamp"
        token inputs:wrapT = "clamp"
        float2 inputs:st.connect = </ArtworkMaterial/PrimvarReader.outputs:result>
        token outputs:rgb
    }
    def Shader "PrimvarReader"
    {
        uniform token info:id = "UsdPrimvarReader_float2"
        token inputs:varname = "st"
        float2 outputs:result
    }
}
'''

def create_usdz(img, out_path):
    w_px, h_px = img.size
    max_dim = max(w_px, h_px)
    w = w_px / max_dim * 0.9
    h = h_px / max_dim * 0.9
    hw, hh = w/2, h/2
    d = 0.025
    pts = [
        (-hw,-hh,d), (hw,-hh,d), (hw,hh,d), (-hw,hh,d),
        (hw,-hh,-d), (-hw,-hh,-d), (-hw,hh,-d), (hw,hh,-d),
        (hw,-hh,d), (hw,-hh,-d), (hw,hh,-d), (hw,hh,d),
        (-hw,-hh,-d), (-hw,-hh,d), (-hw,hh,d), (-hw,hh,-d),
        (-hw,hh,d), (hw,hh,d), (hw,hh,-d), (-hw,hh,-d),
        (-hw,-hh,-d), (hw,-hh,-d), (hw,-hh,d), (-hw,-hh,d),
    ]
    def fmt(v): return f"({v[0]:.6f},{v[1]:.6f},{v[2]:.6f})"
    usda = USDA_TEMPLATE.replace('{{EXTENT_MIN}}', fmt((-hw, -hh, -d)))
    usda = usda.replace('{{EXTENT_MAX}}', fmt((hw, hh, d)))
    usda = usda.replace('{{POINTS}}', ',\n            '.join(fmt(p) for p in pts))
    usda = usda.replace('\n', '\r\n')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_STORED) as zf:
        zf.writestr('model.usda', usda)
        zf.writestr('texture.png', buf.getvalue())

# ---------- Process one artwork (download, GLB, optional USDZ) ----------
def process_one(item, make_usdz, override_local=None):
    slug = item['slug']
    try:
        if override_local and os.path.exists(override_local):
            img = Image.open(override_local).convert('RGB')
        else:
            img = download_image(item['url'], item.get('url_fallback'))
        create_glb(img, os.path.join(ASSETS, f'{slug}.glb'))
        if make_usdz:
            create_usdz(img, os.path.join(ASSETS, f'{slug}.usdz'))
        return (slug, True, f'{img.size[0]}x{img.size[1]}', None)
    except Exception as e:
        return (slug, False, '', str(e))

# ---------- Run ----------
results = {}
errors = []

# 1) Regenerate compact GLBs for existing (keep their USDZ untouched)
print('--- Existing GLB regen ---')
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(process_one, {'slug': e['slug'], 'url': e['image']}, False,
                      os.path.join(ASSETS, 'colored-moments.jpg') if e['slug'] == 'colored-moments' else None): e
            for e in existing}
    for f in as_completed(futs):
        slug, ok, info, err = f.result()
        results[slug] = (ok, info, err)
        if not ok:
            errors.append(('existing', slug, err))
        print(f"  {'OK ' if ok else 'FAIL'} {slug} {info} {err or ''}")

# 2) New artworks: GLB + USDZ
print('--- New artworks (GLB + USDZ) ---')
successful = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(process_one, {'slug': c['slug'], 'url': c['url'], 'url_fallback': c.get('url_fallback')}, True): c
            for c in candidates}
    for f in as_completed(futs):
        c = futs[f]
        slug, ok, info, err = f.result()
        if ok:
            successful.append(c)
        else:
            errors.append(('new', slug, err))
        print(f"  {'OK ' if ok else 'FAIL'} {slug} {info} {err or ''}")

print(f'\nNew artworks OK: {len(successful)} / {len(candidates)}')
print(f'Errors: {len(errors)}')
for kind, slug, err in errors:
    print(f'  {kind}: {slug}: {err[:120]}')

# ---------- Write merged artworks.js ----------
def esc(s):
    return s.replace('\\', '\\\\').replace("'", "\\'")

def entry_js(e):
    lines = [
        '  {',
        f"    slug: '{esc(e['slug'])}',",
        f"    title: '{esc(e['title'])}',",
        f"    year: '{esc(e.get('year', ''))}',",
        f"    medium: '{esc(e.get('medium', 'Acrylic on canvas'))}',",
        f"    size: '{esc(e.get('size', ''))}',",
        f"    image: '{esc(e['image'])}',",
        '    ar: true,',
        f"    glb: '/assets/{esc(e['slug'])}.glb',",
        f"    usdz: '/assets/{esc(e['slug'])}.usdz',",
        f"    poster: '{esc(e['image'])}',",
        '  },',
    ]
    return '\n'.join(lines)

merged = []
for e in existing:
    e2 = dict(e)
    e2['glb'] = f"/assets/{e['slug']}.glb"
    merged.append(e2)
for c in successful:
    merged.append({'slug': c['slug'], 'title': c['title'], 'year': c['year'],
                   'medium': 'Acrylic on canvas', 'size': c['size'], 'image': c['url']})

# sort: year desc, stable
merged.sort(key=lambda e: -(int(e['year']) if str(e.get('year', '')).isdigit() else 0))

out = 'export const artworks = [\n' + '\n'.join(entry_js(e) for e in merged) + '\n];\n\n'
out += "export const featuredArtwork = artworks[0];\n"
out += "export const arArtwork = artworks.find((a) => a.slug === 'colored-moments');\n"
out += "export const arArtworks = artworks.filter((a) => a.ar);\n"
out += "export const artworkBySlug = (slug) => artworks.find((a) => a.slug === slug);\n"

with open(ARTS, 'w', encoding='utf-8') as f:
    f.write(out)

with open(os.path.join(SCRIPTS, 'new-slugs.json'), 'w', encoding='utf-8') as f:
    json.dump([c['slug'] for c in successful], f, indent=1)

print(f'\nartworks.js written: {len(merged)} total artworks ({len(successful)} new)')

#!/usr/bin/env python3
"""Regenerate NEW artworks' USDZ at max 1200px (PNG, STORED) to reduce size."""
import os, io, re, json, zipfile, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

BASE = r'C:\Users\Hauska\jiri-hauschka-next'
ARTS = os.path.join(BASE, 'lib', 'artworks.js')
ASSETS = os.path.join(BASE, 'public', 'assets')

with open(ARTS, encoding='utf-8') as f:
    src = f.read()

# Get all artworks: slug + image url
entries = []
for m in re.finditer(r"slug:\s*'([^']+)',\s*title:\s*'((?:[^'\\]|\\.)*)'[^}]*?image:\s*'([^']+)'", src):
    entries.append({'slug': m.group(1), 'title': m.group(2), 'image': m.group(3)})

RENAMES = {'721':'elastic-world','534':'in-the-garden','514':'wind','528':'mercy-boat','436':'god-in-the-house',
           '427':'around-us','421':'angels','503':'wave','stejny':'museum','telefon':'and-dark-became',
           'slide':'cage','deka':'the-place-farm-house','inthe-middle-of-somewhere':'in-the-middle-of-somewhere'}
OLD_47_SKIP = None

# Determine which slugs are "new" (regenerate) = all except original 47
# Original 47 = the ones whose usdz existed before... simplest: sizes > threshold? No.
# Use: regenerate ALL except the original list. Original list = first 47 slugs from git (we know names).
ORIGINAL_47 = {'bohemian-forest-5','bride','saint-sebastian-with-plastic-arrows','upside-down','red-coast','fragility','heartbeats','i-need-the-night','their-love','colored-moments','all-my-boats','fisher-island-sound','mermaid','red-house','dream-about-renoir','conversation','evening-walk-along-the-sea-that-never-freezes','albatross','fallen-suns','pocket-museum-yellow-version','two-dogs-inside','one-of-these-mornings','into-the-blue','i-am-on-fire','shell-picker','death-becomes-them','untitled-005','night-flight','speak-my-language','bohemian-forest-3','beautiful-boys','birth','tunnel','finding-martin','mistral','broken-starfish','pink','travelling-mood','fish-is-fish','such-a-beautiful-boy','blue-freedom','in-front-of-the-tent','cleanup','untitled','cinema-2','angel-ii','feral-2022'}

USDA_TEMPLATE = open(os.path.join(BASE, 'scripts', '_usda_tmpl.txt'), encoding='utf-8').read()

def encode_url(url):
    parsed = list(urllib.parse.urlsplit(url))
    parsed[2] = urllib.parse.quote(urllib.parse.unquote(parsed[2]), safe='/:@!$&\'()*+,;=-._~%')
    return urllib.parse.urlunsplit(parsed)

def dl(url, max_dim=1200, fallback=None):
    urls = [url] + ([fallback] if fallback else [])
    last = None
    for u in urls:
        try:
            req = urllib.request.Request(encode_url(u), headers={'User-Agent': 'Mozilla/5.0'})
            img = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert('RGB')
            if max(img.size) > max_dim:
                r = max_dim / max(img.size)
                img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
            return img
        except Exception as e:
            last = e
    raise last

FALLBACKS = {
    'small-town-boy': 'https://jirihauschka.com/wp-content/uploads/2021/11/Jiri-Hauschka_Small-Town-Boy_2021_100x120cm-848x1024.jpg',
    'white-river': 'https://jirihauschka.com/wp-content/uploads/2017/01/White-river-683x1024.jpg',
    'tree-of-life-2': 'https://jirihauschka.com/wp-content/uploads/2017/01/Tree-of-life-1024x721.jpg',
    'silent-night': 'https://jirihauschka.com/wp-content/uploads/2017/01/Silent-night-1024x725.jpg',
    'battersea': 'https://jirihauschka.com/wp-content/uploads/2015/04/2009-Battersea-1024x852.jpg',
}

def create_usdz(img, out_path):
    w_px, h_px = img.size
    m = max(w_px, h_px)
    w, h = w_px / m * 0.9, h_px / m * 0.9
    hw, hh = w/2, h/2
    d = 0.025
    pts = [(-hw,-hh,d),(hw,-hh,d),(hw,hh,d),(-hw,hh,d),
           (hw,-hh,-d),(-hw,-hh,-d),(-hw,hh,-d),(hw,hh,-d),
           (hw,-hh,d),(hw,-hh,-d),(hw,hh,-d),(hw,hh,d),
           (-hw,-hh,-d),(-hw,-hh,d),(-hw,hh,d),(-hw,hh,-d),
           (-hw,hh,d),(hw,hh,d),(hw,hh,-d),(-hw,hh,-d),
           (-hw,-hh,-d),(hw,-hh,-d),(hw,-hh,d),(-hw,-hh,d)]
    def fmt(v): return f"({v[0]:.6f},{v[1]:.6f},{v[2]:.6f})"
    usda = USDA_TEMPLATE.replace('{{EXTENT_MIN}}', fmt((-hw,-hh,-d)))
    usda = usda.replace('{{EXTENT_MAX}}', fmt((hw,hh,d)))
    usda = usda.replace('{{POINTS}}', ',\n            '.join(fmt(p) for p in pts))
    usda = usda.replace('\n', '\r\n')
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_STORED) as zf:
        zf.writestr('model.usda', usda)
        zf.writestr('texture.png', buf.getvalue())

def process(e):
    try:
        img = dl(e['image'], fallback=FALLBACKS.get(e['slug']))
        create_usdz(img, os.path.join(ASSETS, f"{e['slug']}.usdz"))
        s = os.path.getsize(os.path.join(ASSETS, f"{e['slug']}.usdz"))
        return (e['slug'], True, f'{img.size[0]}x{img.size[1]} {s//1024}KB', None)
    except Exception as ex:
        return (e['slug'], False, '', str(ex))

targets = [e for e in entries if e['slug'] not in ORIGINAL_47]
print(f'Regenerating {len(targets)} USDZ at 1200px...')

errors = []
ok = 0
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(process, e) for e in targets]
    for f in as_completed(futs):
        slug, good, info, err = f.result()
        if good: ok += 1
        else: errors.append((slug, err))
        if not good:
            print(f'  FAIL {slug}: {err[:100]}')

print(f'OK: {ok}/{len(targets)} | Errors: {len(errors)}')

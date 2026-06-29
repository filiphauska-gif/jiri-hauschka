#!/usr/bin/env python3
"""Sync artworks from WordPress into artworks.js"""
import subprocess, re, os, json

HOME_URL = 'https://jirihauschka.com'

# Use curl to fetch the pages (handles cookies/redirects better)
def fetch(url):
    r = subprocess.run(['curl', '-s', '-L', url], capture_output=True, text=True, timeout=30)
    return r.stdout

html = fetch(HOME_URL)
works_html = fetch(HOME_URL + '/?page_id=1279')

# Parse all images from homepage - find src attributes
home_srcs = re.findall(r'src=\"([^\"]*wp-content/uploads/[^\"]+\.(?:jpg|png))\"', html)
# Deduplicate
home_urls = list(dict.fromkeys(home_srcs))

print(f'Found {len(home_urls)} artwork images on homepage')

# Parse captions from works-available
captions = re.findall(r'<figcaption[^>]*>(.*?)</figcaption>', works_html, re.DOTALL)
sold_data = {}
for cap in captions:
    clean = re.sub(r'<[^>]+>', '', cap).strip()
    clean = re.sub(r'<br\s*/?>', ', ', clean)
    parts = [p.strip() for p in clean.split(',') if p.strip()]
    if len(parts) >= 2:
        title = parts[0].strip()
        year = ''
        medium = ''
        size = ''
        for p in parts[1:]:
            p = p.strip()
            if re.match(r'^\d{4}$', p):
                year = p
            elif 'acrylic' in p.lower():
                medium = p
            elif 'cm' in p.lower():
                size = p
        if not medium:
            medium = 'Acrylic on canvas'
        slug = title.lower().replace(' ', '-').replace('–', '-').replace('×', 'x')
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        sold_data[slug] = {'title': title, 'year': year, 'medium': medium, 'size': size}

print(f'Found {len(sold_data)} artworks with metadata from works-available')

def parse_artwork(url):
    fn = url.split('/')[-1]
    name = re.sub(r'-\d+x\d+(?=\.)', '', fn)
    name = re.sub(r'\.(jpg|png)$', '', name)
    name = re.sub(r'-(large|thumb|scaled)$', '', name)
    
    clean = re.sub(r'^Jiri-Hauschka[_ -]', '', name)
    clean = re.sub(r'^Jiri-Hauschka-', '', clean)
    
    year_match = re.search(r'(19\d{2}|20\d{2})', clean)
    year = year_match.group(1) if year_match else ''
    
    size_match = re.search(r'(\d+)\s*[×x]\s*(\d+)\s*cm', clean, re.IGNORECASE)
    if not size_match:
        size_match = re.search(r'(\d+)x(\d+)cm', clean, re.IGNORECASE)
    size = f'{size_match.group(1)}x{size_match.group(2)} cm' if size_match else ''
    
    medium = ''
    if 'acrylic' in clean.lower():
        medium = 'Acrylic on canvas'
    
    # Extract title by removing metadata
    title = clean
    # Remove year
    title = re.sub(r'_?' + year + r'_?', ' ', title) if year else title
    # Remove size patterns
    title = re.sub(r'_\d+[×x]\d+\s*cm-?', '', title, flags=re.IGNORECASE)
    title = re.sub(r'-\d+[×x]\d+-?cm?', '', title, flags=re.IGNORECASE)
    title = re.sub(r'_\d+[×x]\d+cm_?', '', title, flags=re.IGNORECASE)
    # Remove medium
    title = re.sub(r'[-_]?acrylic[-_ ]on[-_ ]canvas[-_]?', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[-_]?acrylic_on_canvas[-_]?', '', title, flags=re.IGNORECASE)
    # Normalize
    title = re.sub(r'[-_]+', ' ', title).strip()
    title = re.sub(r'\b\d{4}\b', '', title).strip()
    title = re.sub(r'\bcm\b', '', title, flags=re.IGNORECASE).strip()
    title = re.sub(r'\s+', ' ', title).strip()
    
    slug = title.lower().replace(' ', '-')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    if not slug or len(slug) < 3:
        # Fallback: use filename as slug
        slug = re.sub(r'[^a-z0-9-]', '', os.path.splitext(fn)[0].lower())[:40]
        slug = re.sub(r'-+', '-', slug).strip('-')
    
    # Check sold data
    if slug in sold_data:
        sd = sold_data[slug]
        artwork = {
            'slug': slug,
            'title': sd['title'],
            'year': sd['year'] or year,
            'medium': sd['medium'] or (medium or 'Acrylic on canvas'),
            'size': sd['size'] or size,
            'image': url,
            'ar': False
        }
    else:
        # Clean up title words
        filtered = [w for w in title.split() if w.lower() not in 
                    ['acrylic','on','canvas','cm','jpg','png','large','thumb']]
        title_clean = ' '.join(filtered).strip()
        if not title_clean:
            title_clean = os.path.splitext(fn)[0].replace('-', ' ').replace('_', ' ')
            title_clean = re.sub(r'\s*\d+x\d+\s*cm\s*', ' ', title_clean, flags=re.IGNORECASE).strip()
        
        artwork = {
            'slug': slug or 'untitled',
            'title': title_clean.title() if title_clean else 'Untitled',
            'year': year,
            'medium': medium or 'Acrylic on canvas',
            'size': size,
            'image': url,
            'ar': False
        }
    return artwork

# Process all images
seen = set()
all_artworks = []
for url in home_urls:
    art = parse_artwork(url)
    if art['slug'] and art['slug'] not in seen:
        seen.add(art['slug'])
        all_artworks.append(art)

# Read existing artworks.js to preserve AR config
arts_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'artworks.js')
with open(arts_js_path, 'r', encoding='utf-8') as f:
    existing_content = f.read()

existing_ar = re.findall(r"slug:\s*'([^']+)'[^}]+ar:\s*true", existing_content)
existing_ar_slugs = set(existing_ar)
existing_glb = dict(re.findall(r"slug:\s*'([^']+)'[^}]+glb:\s*'([^']+)'", existing_content))
existing_usdz = dict(re.findall(r"slug:\s*'([^']+)'[^}]+usdz:\s*'([^']+)'", existing_content))
existing_poster = dict(re.findall(r"slug:\s*'([^']+)'[^}]+poster:\s*'([^']+)'", existing_content))

for a in all_artworks:
    if a['slug'] in existing_ar_slugs:
        a['ar'] = True
    if a['slug'] in existing_glb:
        a['glb'] = existing_glb[a['slug']]
    if a['slug'] in existing_usdz:
        a['usdz'] = existing_usdz[a['slug']]
    if a['slug'] in existing_poster:
        a['poster'] = existing_poster[a['slug']]

# Generate output
lines = ['export const artworks = [']
for a in all_artworks:
    lines.append('  {')
    lines.append(f"    slug: '{a['slug']}',")
    lines.append(f"    title: '{a['title']}',")
    lines.append(f"    year: '{a['year']}',")
    lines.append(f"    medium: '{a['medium']}',")
    lines.append(f"    size: '{a['size']}',")
    lines.append(f"    image: '{a['image']}',")
    lines.append(f"    ar: {str(a['ar']).lower()},")
    if a.get('glb'): lines.append(f"    glb: '{a['glb']}',")
    if a.get('usdz'): lines.append(f"    usdz: '{a['usdz']}',")
    if a.get('poster'): lines.append(f"    poster: '{a['poster']}',")
    lines.append('  },')
lines.append('];')
lines.append('')
lines.append('export const featuredArtwork = artworks[0];')
lines.append("export const arArtwork = artworks.find((artwork) => artwork.slug === 'colored-moments');")

with open(arts_js_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f'\nDone! Synced {len(all_artworks)} artworks to lib/artworks.js')
print(f'  AR enabled: {sum(1 for a in all_artworks if a.get("ar"))}')
print(f'  Sold data matched: {sum(1 for a in all_artworks if a["slug"] in sold_data)}')

# Show first 10 slugs for verification
print('\nFirst 20 artworks:')
for a in all_artworks[:20]:
    print(f'  {a["slug"]:40s} | {a["year"]:4s} | {a["size"]:15s} | {"AR" if a.get("ar") else "  "}')

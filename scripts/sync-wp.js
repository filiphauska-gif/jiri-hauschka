import sys, json, re, os
sys.path.insert(0, os.path.dirname(__file__))
from lib.artworks import artworks as existing_artworks

HOME_URL = 'https://jirihauschka.com'
WORKS_AVAILABLE_ID = 1279

def fetch(url):
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': 'Hermes-Sync/1.0'})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8')

# 1. Fetch homepage and works-available page
html = fetch(HOME_URL)
works_html = fetch(f'{HOME_URL}/?page_id={WORKS_AVAILABLE_ID}')

# 2. Parse all images from homepage
home_imgs = re.findall(r'<img[^>]+src=\"([^\"]*wp-content/uploads/[^\"]+\.(?:jpg|png))\"', html)
home_urls = list(dict.fromkeys([i[0] for i in home_imgs]))

# 3. Parse captions from works-available
captions = re.findall(r'<figcaption[^>]*>(.*?)</figcaption>', works_html, re.DOTALL)
sold_data = {}
for cap in captions:
    clean = re.sub(r'<[^>]+>', '', cap).strip()
    # Parse: TITLE, YEAR, medium, size
    parts = [p.strip() for p in clean.split(',')]
    if len(parts) >= 4:
        title = parts[0]
        year = parts[1]
        medium = parts[2]
        size = parts[3]
        slug = title.lower().replace(' ', '-').replace('–', '-').replace('×', 'x')
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        sold_data[slug] = {'title': title, 'year': year, 'medium': medium, 'size': size}

# 4. Parse image filenames to extract artwork info
def parse_filename(url):
    fn = url.split('/')[-1]
    name = re.sub(r'-\d+x\d+(?=\.)', '', fn)
    name = re.sub(r'\.(jpg|png)$', '', name)
    name = re.sub(r'-(large|thumb)$', '', name)
    return name

def extract_artwork_data(url):
    fn = url.split('/')[-1]
    name = re.sub(r'-\d+x\d+(?=\.)', '', fn)
    name = re.sub(r'\.(jpg|png)$', '', name)
    
    # Remove leading artist prefix
    clean = re.sub(r'^Jiri-Hauschka_', '', name)
    clean = re.sub(r'^Jiří-Hauschka_', '', clean)
    clean = re.sub(r'^Jiri-Hauschka-', '', clean)
    
    # Try to extract year (4 digits)
    year_match = re.search(r'(19\d{2}|20\d{2})', clean)
    year = year_match.group(1) if year_match else ''
    
    # Try to extract size
    size_match = re.search(r'(\d+)[×x](\d+)\s*cm', clean, re.IGNORECASE)
    if not size_match:
        size_match = re.search(r'(\d+)x(\d+)cm', clean, re.IGNORECASE)
    size = f'{size_match.group(1)}x{size_match.group(2)} cm' if size_match else ''
    
    # Try to extract medium
    medium = ''
    for m in ['acrylic-on-canvas', 'acrylic_on_canvas', 'acrylic on canvas']:
        if m in clean.lower():
            medium = 'Acrylic on canvas'
            break
    
    # Title is everything before year or size
    title_clean = re.sub(r'_\d{4}_', ' ', clean)
    title_clean = re.sub(r'-\d{4}-', ' - ', title_clean)
    title_clean = re.sub(r'_\d+[x×]\d+cm?', '', title_clean, flags=re.IGNORECASE)
    title_clean = re.sub(r'-\d+[x×]\d+-?cm?', '', title_clean, flags=re.IGNORECASE)
    title_clean = re.sub(r'[-_]+', ' ', title_clean)
    title_clean = re.sub(r'\s+', ' ', title_clean).strip()
    title_clean = re.sub(r'(\d{4})$', '', title_clean).strip()
    if title_clean.endswith('-'):
        title_clean = title_clean[:-1].strip()
    
    # Cleanup common noise
    title_clean = re.sub(r'\bcm\b', '', title_clean, flags=re.IGNORECASE).strip()
    title_clean = re.sub(r'\bacrylic\s+on\s+canvas\b', '', title_clean, flags=re.IGNORECASE).strip()
    
    # Generate slug
    slug = title_clean.lower().replace(' ', '-')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    
    if not slug:
        slug = os.path.splitext(fn)[0][:40]
        slug = re.sub(r'[^a-z0-9-]', '', slug.lower())
    
    # Check if we have sold data for this slug
    if slug in sold_data:
        sd = sold_data[slug]
        return {
            'slug': slug,
            'title': sd['title'],
            'year': sd['year'],
            'medium': sd['medium'] or (medium or 'Acrylic on canvas'),
            'size': sd['size'],
            'image': url if url.startswith('http') else f'https://jirihauschka.com{url}',
            'ar': False
        }
    
    return {
        'slug': slug,
        'title': title_clean.title() if title_clean else 'Untitled',
        'year': year,
        'medium': medium or 'Acrylic on canvas',
        'size': size,
        'image': url if url.startswith('http') else f'https://jirihauschka.com{url}',
        'ar': False
    }

# 5. Process all images, deduplicate by slug
seen_slugs = set()
all_artworks = []
for url in home_urls:
    artwork = extract_artwork_data(url)
    if artwork['slug'] and artwork['slug'] not in seen_slugs:
        seen_slugs.add(artwork['slug'])
        all_artworks.append(artwork)

# 6. Merge with existing artworks (preserve ar config)
existing_by_slug = {a['slug']: a for a in existing_artworks}
for a in all_artworks:
    if a['slug'] in existing_by_slug:
        ea = existing_by_slug[a['slug']]
        a['ar'] = ea.get('ar', False)
        if ea.get('glb'): a['glb'] = ea['glb']
        if ea.get('usdz'): a['usdz'] = ea['usdz']
        if ea.get('poster'): a['poster'] = ea['poster']

# 7. Generate the file
output = 'export const artworks = [\n'
for a in all_artworks:
    output += '  {\n'
    output += f"    slug: '{a['slug']}',\n"
    output += f"    title: '{a['title']}',\n"
    output += f"    year: '{a['year']}',\n"
    output += f"    medium: '{a['medium']}',\n"
    output += f"    size: '{a['size']}',\n"
    output += f"    image: '{a['image']}',\n"
    output += f"    ar: {str(a['ar']).lower()},\n"
    if a.get('glb'): output += f"    glb: '{a['glb']}',\n"
    if a.get('usdz'): output += f"    usdz: '{a['usdz']}',\n"
    if a.get('poster'): output += f"    poster: '{a['poster']}',\n"
    output += '  },\n'
output += '];\n\n'
output += f"export const featuredArtwork = artworks[0];\n"
output += f"export const arArtwork = artworks.find((artwork) => artwork.slug === 'colored-moments');\n"

with open('lib/artworks.js', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'Synced {len(all_artworks)} artworks from WordPress')
print(f'  - {sum(1 for a in all_artworks if a["ar"])} with AR')
print(f'  - {len(all_artworks) - sum(1 for a in all_artworks if a["ar"])} without AR')
print('Done!')

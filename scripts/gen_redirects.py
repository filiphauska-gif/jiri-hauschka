#!/usr/bin/env python3
"""Generate vercel.json redirects for old WP URLs + public/robots.txt + sitemap.xml."""
import re, json, os

BASE = r'C:\Users\Hauska\jiri-hauschka-next'
BACKUP = r'C:\Users\Hauska\wp-archive-jirihauschka\content-posts-pages.json'

# 1) New slugs from artworks.js
src = open(os.path.join(BASE, 'lib', 'artworks.js'), encoding='utf-8').read()
new_slugs = set(re.findall(r"slug:\s*'([^']+)'", src))
print(f'New artwork slugs: {len(new_slugs)}')

# 2) Old posts from backup
data = json.load(open(BACKUP, encoding='utf-8'))
old_posts = [p['slug'] for p in data['posts']]
print(f'Old posts: {len(old_posts)}')

# 3) Old slug -> new slug renames (junk WP slugs)
RENAMES = {
    'stejny': 'museum', 'telefon': 'and-dark-became', 'slide': 'cage',
    'deka': 'the-place-farm-house', '721': 'elastic-world', '534': 'in-the-garden',
    '514': 'wind', '528': 'mercy-boat', '436': 'god-in-the-house',
    '427': 'around-us', '421': 'angels', '503': 'wave',
    'inthe-middle-of-somewhere': 'in-the-middle-of-somewhere',
}

redirects = []

# Pages
page_map = {
    'work': '/#works', 'works': '/#works', 'works-available': '/#works',
    'contact': '/#contact', 'intro': '/', 'home-template': '/',
    'instagram-feed': '/#instagram',
}
for old, dest in page_map.items():
    redirects.append({'source': f'/{old}/?', 'destination': dest, 'permanent': True})

# Posts
mapped = renamed = fallback = 0
for slug in old_posts:
    if slug in new_slugs:
        redirects.append({'source': f'/{slug}/?', 'destination': f'/ar/{slug}/', 'permanent': True})
        mapped += 1
    elif slug in RENAMES and RENAMES[slug] in new_slugs:
        redirects.append({'source': f'/{slug}/?', 'destination': f'/ar/{RENAMES[slug]}/', 'permanent': True})
        renamed += 1
    else:
        redirects.append({'source': f'/{slug}/?', 'destination': '/#works', 'permanent': True})
        fallback += 1

print(f'Posts: {mapped} direct, {renamed} renamed, {fallback} fallback -> /#works')
print(f'Total redirects: {len(redirects)}')

# 4) Write vercel.json (keep existing headers, add redirects)
vercel = json.load(open(os.path.join(BASE, 'vercel.json'), encoding='utf-8'))
vercel['redirects'] = redirects
with open(os.path.join(BASE, 'vercel.json'), 'w', encoding='utf-8') as f:
    json.dump(vercel, f, indent=2, ensure_ascii=False)
print('vercel.json updated')

# 5) robots.txt
robots = """User-agent: *
Allow: /

Sitemap: https://jirihauschka.com/sitemap.xml
"""
open(os.path.join(BASE, 'public', 'robots.txt'), 'w', encoding='utf-8').write(robots)
print('public/robots.txt written')

# 6) sitemap.xml
from datetime import date
today = date.today().isoformat()
urls = ['https://jirihauschka.com/', 'https://jirihauschka.com/bio/', 'https://jirihauschka.com/exhibitions/']
urls += [f'https://jirihauschka.com/ar/{s}/' for s in sorted(new_slugs)]
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    prio = '1.0' if u.endswith('.com/') else '0.8'
    xml += f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>\n'
xml += '</urlset>\n'
open(os.path.join(BASE, 'public', 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
print(f'public/sitemap.xml written ({len(urls)} URLs)')

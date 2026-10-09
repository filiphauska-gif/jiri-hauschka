#!/usr/bin/env python3
"""Complete WordPress backup: content JSON + all media originals."""
import urllib.request, urllib.parse, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = 'https://admin.jirihauschka.com/wp-json/wp/v2'
OUT = r'C:\Users\Hauska\wp-archive-jirihauschka'
MEDIA_DIR = os.path.join(OUT, 'media')
os.makedirs(MEDIA_DIR, exist_ok=True)

def get(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read()), dict(r.headers)

def fetch_all(post_type):
    """Fetch all items of a post type paginated."""
    items = []
    page = 1
    while True:
        data, hdrs = get(f'/{post_type}?per_page=100&page={page}')
        items.extend(data)
        total_pages = int(hdrs.get('X-WP-TotalPages', 1))
        print(f'  {post_type} page {page}/{total_pages}: {len(data)} items')
        if page >= total_pages:
            break
        page += 1
    return items

print('=== 1. Fetching content ===')
posts_data = {'posts': fetch_all('posts')}
posts_data['pages'] = fetch_all('pages')

# media separately (status inherit)
media = []
page = 1
while True:
    data, hdrs = get(f'/media?per_page=100&page={page}')
    media.extend(data)
    total_pages = int(hdrs.get('X-WP-TotalPages', 1))
    print(f'  media page {page}/{total_pages}: {len(data)} items')
    if page >= total_pages:
        break
    page += 1

with open(os.path.join(OUT, 'content-posts-pages.json'), 'w', encoding='utf-8') as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=1)
with open(os.path.join(OUT, 'content-media.json'), 'w', encoding='utf-8') as f:
    json.dump(media, f, ensure_ascii=False, indent=1)

print(f'\nSaved: {len(posts_data["posts"])} posts, {len(posts_data["pages"])} pages, {len(media)} media items')

# === 2. Download media originals ===
print('\n=== 2. Downloading media originals ===')
tasks = []
for m in media:
    url = m.get('source_url')
    if not url:
        continue
    # keep subdirectory structure from uploads path
    path = urllib.parse.urlparse(url).path  # /wp-content/uploads/2025/03/name.jpg
    rel = path.replace('/wp-content/uploads/', '')
    tasks.append((url, rel))

def encode_url(url):
    parts = urllib.parse.urlsplit(url)
    path = urllib.parse.quote(parts.path, safe='/%')
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

def dl(task):
    url, rel = task
    dest = os.path.join(MEDIA_DIR, rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return (rel, os.path.getsize(dest), 'skip')
    try:
        req = urllib.request.Request(encode_url(url), headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
        with open(dest, 'wb') as f:
            f.write(data)
        return (rel, len(data), 'ok')
    except Exception as e:
        return (rel, 0, f'ERR {str(e)[:60]}')

ok = skip = errs = 0
total_bytes = 0
errors = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(dl, t) for t in tasks]
    for i, fut in enumerate(as_completed(futs), 1):
        rel, size, status = fut.result()
        if status == 'ok':
            ok += 1; total_bytes += size
        elif status == 'skip':
            skip += 1; total_bytes += size
        else:
            errs += 1; errors.append(f'{rel}: {status}')
        if i % 50 == 0:
            print(f'  {i}/{len(tasks)} processed ({total_bytes/1e6:.1f} MB so far)')

print(f'\n=== DONE ===')
print(f'Downloaded: {ok} | Skipped: {skip} | Errors: {errs} | Total: {total_bytes/1e6:.1f} MB')
if errors:
    print('Errors:')
    for e in errors[:20]:
        print(' ', e)

# Summary file
with open(os.path.join(OUT, 'BACKUP-INFO.txt'), 'w', encoding='utf-8') as f:
    f.write(f'WordPress backup of jirihauschka.com (via admin.jirihauschka.com)\n')
    f.write(f'Date: {time.strftime("%Y-%m-%d %H:%M")}\n')
    f.write(f'Posts: {len(posts_data["posts"])} | Pages: {len(posts_data["pages"])} | Media: {len(media)}\n')
    f.write(f'Media downloaded: {ok+skip}/{len(tasks)} ({total_bytes/1e6:.1f} MB)\n')
    f.write(f'Errors: {errs}\n')
    f.write(f'Note: database dump (phpMyAdmin) must be done via Forpsi panel - see README\n')
print('BACKUP-INFO.txt written to', OUT)

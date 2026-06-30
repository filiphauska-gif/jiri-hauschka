'use client';
import { useEffect, useState } from 'react';

export default function InstagramFeed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('https://jirihauschka.com/wp-json/wp/v2/pages/1706?_fields=content')
      .then(r => r.json())
      .then(data => {
        const html = data.content.rendered;
        const urls = [...html.matchAll(/data-full-res="([^"]+)"/g)].map(m => m[1].replace(/&#038;/g, '&').replace(/&amp;/g, '&'));
        const links = [...html.matchAll(/class="sbi_photo" href="([^"]+)"/g)].map(m => m[1]);
        const items = urls.slice(0, 5).map((url, i) => ({ url, link: links[i] || '#' }));
        setPosts(items);
      })
      .catch(() => setPosts([]));
  }, []);

  if (posts.length === 0) return null;

  return (
    <div className="insta-feed-grid">
      {posts.map((post, i) => (
        <a key={i} href={post.link} target="_blank" rel="noopener noreferrer" className="insta-post">
          <img src={post.url} alt={`Instagram post ${i + 1}`} loading="lazy" />
        </a>
      ))}
    </div>
  );
}

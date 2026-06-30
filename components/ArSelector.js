'use client';

import { artworks, arArtworks } from '../lib/artworks';

export default function ArSelector({ currentSlug }) {
  return (
    <div className="ar-select-row">
      <h1>{artworks.find(a => a.slug === currentSlug)?.title}</h1>
      <select
        className="ar-select"
        defaultValue={currentSlug}
        onChange={(e) => { window.location.href = `/ar/${e.target.value}`; }}
      >
        {arArtworks.map((a) => (
          <option key={a.slug} value={a.slug}>
            {a.title} ({a.year})
          </option>
        ))}
      </select>
    </div>
  );
}

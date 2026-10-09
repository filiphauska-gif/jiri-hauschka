'use client';

import { artworks, arArtworks } from '../lib/artworks';

export default function ArSelector({ currentSlug }) {
  const groups = {};
  arArtworks.forEach((a) => {
    const y = a.year || 'Earlier';
    (groups[y] = groups[y] || []).push(a);
  });
  const years = Object.keys(groups).sort((a, b) => {
    if (a === 'Earlier') return 1;
    if (b === 'Earlier') return -1;
    return Number(b) - Number(a);
  });

  return (
    <div className="ar-select-row">
      <h1>{artworks.find(a => a.slug === currentSlug)?.title}</h1>
      <select
        className="ar-select"
        defaultValue={currentSlug}
        onChange={(e) => { window.location.href = `/ar/${e.target.value}`; }}
      >
        {years.map((y) => (
          <optgroup key={y} label={y}>
            {groups[y].map((a) => (
              <option key={a.slug} value={a.slug}>
                {a.title}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
    </div>
  );
}

'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Nav({ active }) {
  const [open, setOpen] = useState(false);

  return (
    <nav className="nav">
      <div className="nav-inner">
        <Link href="/" className="brand" onClick={() => setOpen(false)}>Jiri Hauschka</Link>
        <button className="hamburger" onClick={() => setOpen(!open)} aria-label="Menu">
          <span className={`hamburger-line ${open ? 'open' : ''}`}></span>
        </button>
        <div className={`links${open ? ' links-open' : ''}`}>
          <Link href="/#works" onClick={() => setOpen(false)}>Works</Link>
          <Link href="/#bio" onClick={() => setOpen(false)}>Bio</Link>
          <Link href="/exhibitions" onClick={() => setOpen(false)}>Exhibitions</Link>
          {active === 'ar' ? (
            <span className="nav-active">AR</span>
          ) : (
            <Link href="/ar/colored-moments" onClick={() => setOpen(false)}>AR</Link>
          )}
          <a href="#instagram" onClick={() => setOpen(false)}>Instagram</a>
          <a href="#contact" onClick={() => setOpen(false)}>Contact</a>
        </div>
      </div>
    </nav>
  );
}

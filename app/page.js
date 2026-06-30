'use client';
import { useState, useCallback, useEffect } from 'react';
import Link from 'next/link';
import { artworks, artworkBySlug } from '../lib/artworks';
import InstagramFeed from '../components/InstagramFeed';

const PER_PAGE = 12;

function QRCode({ url, size = 140 }) {
  return (
    <div className="qr-wrap">
      <img src={`https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodeURIComponent(url)}`}
           alt="QR code" width={size} height={size} />
      <span className="qr-label">Open on your phone to try AR</span>
    </div>
  );
}

export default function HomePage() {
  const [count, setCount] = useState(PER_PAGE);
  const [lightbox, setLightbox] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const visible = artworks.slice(0, count);
  const hasMore = count < artworks.length;

  const openLightbox = useCallback((slug) => {
    const art = artworkBySlug(slug);
    if (art) setLightbox(art);
  }, []);

  const closeLightbox = useCallback(() => setLightbox(null), []);

  useEffect(() => {
    if (lightbox) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [lightbox]);

  return (
    <main>
      <nav className="nav">
        <div className="nav-inner">
          <a href="#top" className="brand">Jiri Hauschka</a>
          <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)} aria-label="Menu">
            <span className={`hamburger-line ${menuOpen ? 'open' : ''}`}></span>
          </button>
          <div className={`links ${menuOpen ? 'links-open' : ''}`}>
            <a href="#works" onClick={() => setMenuOpen(false)}>Works</a>
            <a href="#bio" onClick={() => setMenuOpen(false)}>Bio</a>
            <Link href="/exhibitions" onClick={() => setMenuOpen(false)}>Exhibitions</Link>
            <a href="#ar" onClick={() => setMenuOpen(false)}>AR</a>
            <a href="#instagram" onClick={() => setMenuOpen(false)}>Instagram</a>
            <a href="#contact" onClick={() => setMenuOpen(false)}>Contact</a>
          </div>
        </div>
      </nav>

      <header className="hero" id="top">
        <div className="hero-bg" style={{backgroundImage: `url(${artworks[0].image})`}}></div>
        <div className="hero-inner">
          <div>
            <h1>Jiri<br />Hauschka</h1>
            <p className="lead">Paintings between abstraction, figuration and magical realism.</p>
            <div className="actions">
              <a className="btn primary" href="#works">View works</a>
            </div>
          </div>
          <figure className="hero-art">
            <img src={artworks[0].image} alt={`${artworks[0].title} by Jiri Hauschka`} />
            <figcaption className="caption">{artworks[0].title}, {artworks[0].year}</figcaption>
          </figure>
        </div>
      </header>

      <section>
        <div className="wrap intro-card">
          <p>Memory, nature and inner landscapes.</p>
          <div className="quote">A quiet frame for paintings that carry the colour and atmosphere themselves.</div>
        </div>
      </section>

      <section id="works">
        <div className="wrap">
          <div className="section-head">
            <div>
              <div className="kicker">Works</div>
              <h2 className="title">Paintings.</h2>
            </div>
            <p className="small-copy">{artworks.length} works</p>
          </div>
          <div className="works-grid">
            {visible.map((artwork) => (
              <article className="work" key={artwork.slug} onClick={() => openLightbox(artwork.slug)}>
                <div className="work-img"><img src={artwork.image} alt={artwork.title} loading="lazy" /></div>
                <div className="work-meta">
                  <h3>{artwork.title}</h3>
                  <p>{artwork.year}{artwork.medium ? ` · ${artwork.medium}` : ''}{artwork.size ? ` · ${artwork.size}` : ''}</p>
                </div>
              </article>
            ))}
          </div>
          {hasMore && (
            <div className="load-more-wrap">
              <button className="btn load-more" onClick={() => setCount(c => c + PER_PAGE)}>
                Load more ({artworks.length - count} remaining)
              </button>
            </div>
          )}
        </div>
      </section>

      {lightbox && (
        <div className="lightbox" onClick={closeLightbox}>
          <span className="lightbox-close">&times;</span>
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <img src={lightbox.image} alt={lightbox.title} />
            <div className="lightbox-meta">
              <h3>{lightbox.title}</h3>
              <p>{lightbox.year}{lightbox.medium ? ` · ${lightbox.medium}` : ''}{lightbox.size ? ` · ${lightbox.size}` : ''}</p>
              {lightbox.ar && <Link className="btn primary" href={`/ar/${lightbox.slug}`}>View on your wall</Link>}
            </div>
          </div>
        </div>
      )}

      <section id="bio">
        <div className="wrap">
          <div className="card bio-card">
            <h2>Biography</h2>
            <p>Born in Šumperk, Jiri Hauschka lives and works in Prague. His paintings are held in the National Gallery Prague and private collections internationally. Working primarily in acrylic on canvas, his practice moves between abstraction, figuration and symbolic landscapes — rooted in memory, nature and inner experience.</p>
            <div className="facts">
              <div className="fact"><strong>Born</strong><span>1965, Šumperk</span></div>
              <div className="fact"><strong>Based in</strong><span>Prague, Czech Republic</span></div>
              <div className="fact"><strong>Medium</strong><span>Acrylic on canvas</span></div>
              <div className="fact"><strong>Focus</strong><span>Nature, memory, symbolic landscapes</span></div>
            </div>
          </div>
        </div>
      </section>

      <section className="ar" id="ar">
        <div className="wrap ar-panel">
          <div className="ar-left">
            <div className="kicker light">Augmented reality</div>
            <h2>View on your wall.</h2>
            <p>On mobile, visitors can place an artwork in their own space and see its real scale.</p>
            <QRCode url="https://preview.jirihauschka.com/ar/colored-moments" />
            <Link className="btn primary mobile-only" href="/ar/colored-moments">Try AR preview</Link>
          </div>
          <div className="phone">
            <img className="phone-room" src="/assets/ar-room.png" alt="Room" />
            <img className="phone-art" src={artworkBySlug('colored-moments').image} alt="Artwork on wall" />
          </div>
        </div>
      </section>

      <section id="instagram">
        <div className="wrap insta-section">
          <h2>Instagram</h2>
          <p className="insta-handle">@jirihauschka</p>
          <InstagramFeed />
          <a className="btn insta-brand-btn" href="https://instagram.com/jirihauschka" target="_blank" rel="noopener">
            Follow on Instagram
          </a>
        </div>
      </section>

      <section id="contact">
        <div className="wrap">
          <div className="card contact-card">
            <h2>For sales, exhibitions and enquiries.</h2>
            <p className="contact-email">jirihauschka@seznam.cz</p>
            <p className="contact-note">Direct contact for collectors, galleries and curators.</p>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="wrap">&copy; Jiri Hauschka</div>
      </footer>
    </main>
  );
}

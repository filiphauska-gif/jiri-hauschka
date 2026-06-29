'use client';
import { useState } from 'react';
import Link from 'next/link';
import { artworks, arArtwork } from '../lib/artworks';

const PER_PAGE = 24;

export default function HomePage() {
  const [count, setCount] = useState(PER_PAGE);
  const visible = artworks.slice(0, count);
  const hasMore = count < artworks.length;

  return (
    <main>
      <nav className="nav">
        <div className="nav-inner">
          <a href="#top" className="brand">Jiri Hauschka</a>
          <div className="links">
            <a href="#works">Works</a>
            <a href="#bio">Bio</a>
            <a href="#exhibitions">Exhibitions</a>
            <a href="#ar">AR</a>
            <a href="#contact">Contact</a>
          </div>
        </div>
      </nav>

      <header className="hero" id="top">
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
            <p className="small-copy">{artworks.length} works · {artworks.filter(a => a.ar).length} with AR preview</p>
          </div>
          <div className="works-grid">
            {visible.map((artwork) => (
              <article className="work" key={artwork.slug}>
                <div className="work-img"><img src={artwork.image} alt={artwork.title} loading="lazy" /></div>
                <div className="work-meta">
                  <h3>{artwork.title}</h3>
                  <p>{artwork.year} · {artwork.medium}{artwork.size ? ` · ${artwork.size}` : ''}</p>
                  {artwork.ar ? <Link className="ar-badge" href={`/ar/${artwork.slug}`}>View on your wall</Link> : null}
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

      <section id="bio">
        <div className="wrap bio">
          <h2>Biography</h2>
          <div className="bio-grid">
            <p className="text">Born in Šumperk, Jiri Hauschka lives and works in Prague. His paintings are held in the National Gallery Prague and private collections internationally. Working primarily in acrylic on canvas, his practice moves between abstraction, figuration and symbolic landscapes — rooted in memory, nature and inner experience.</p>
            <div className="facts">
              <div className="fact"><strong>Born</strong><span>1965, Šumperk</span></div>
              <div className="fact"><strong>Based in</strong><span>Prague, Czech Republic</span></div>
              <div className="fact"><strong>Medium</strong><span>Acrylic on canvas</span></div>
              <div className="fact"><strong>Focus</strong><span>Nature, memory, symbolic landscapes</span></div>
            </div>
          </div>
        </div>
      </section>

      <section id="exhibitions">
        <div className="wrap exhibitions">
          <h2>Exhibitions</h2>
          <div className="exh-list">
            <div className="exh-item">
              <div className="exh-year">2024</div>
              <div className="exh-detail">
                <strong>National Gallery Prague</strong>
                <span className="exh-place">Prague, Czech Republic</span>
                <span className="exh-note">Group exhibition — Contemporary Czech Landscape</span>
              </div>
            </div>
            <div className="exh-item">
              <div className="exh-year">2023</div>
              <div className="exh-detail">
                <strong>Solo Exhibition</strong>
                <span className="exh-place">Galerie Kritiků, Prague</span>
                <span className="exh-note">New works</span>
              </div>
            </div>
            <div className="exh-item">
              <div className="exh-year">2022</div>
              <div className="exh-detail">
                <strong>Art Prague Fair</strong>
                <span className="exh-place">Prague</span>
              </div>
            </div>
            <div className="exh-item">
              <div className="exh-year">2021</div>
              <div className="exh-detail">
                <strong>Galerie Mánes</strong>
                <span className="exh-place">Prague, Czech Republic</span>
              </div>
            </div>
            <div className="exh-item">
              <div className="exh-year">2019</div>
              <div className="exh-detail">
                <strong>Kunsthalle Praha</strong>
                <span className="exh-place">Prague, Czech Republic</span>
              </div>
            </div>
            <div className="exh-item">
              <div className="exh-year">2017</div>
              <div className="exh-detail">
                <strong>Galerie Václava Špály</strong>
                <span className="exh-place">Prague, Czech Republic</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="ar" id="ar">
        <div className="wrap ar-panel">
          <div className="ar-copy">
            <div className="kicker light">Augmented reality</div>
            <h2>View selected paintings on your wall.</h2>
            <p>On mobile, visitors can place an artwork in their own space and see its real scale.</p>
            <Link className="btn primary" href={`/ar/${arArtwork.slug}`}>Try AR preview</Link>
          </div>
          <div className="phone">
            <img className="wall-art" src={arArtwork.image} alt={`${arArtwork.title} on wall`} />
          </div>
        </div>
      </section>

      <section id="contact">
        <div className="wrap contact">
          <h2>For sales, exhibitions and enquiries.</h2>
          <p className="contact-email">jirihauschka@seznam.cz</p>
          <p className="contact-note">Direct contact for collectors, galleries and curators.</p>
        </div>
      </section>

      <footer className="footer">
        <div className="wrap">&copy; Jiri Hauschka</div>
      </footer>
    </main>
  );
}

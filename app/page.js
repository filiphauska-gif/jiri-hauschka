import Link from 'next/link';
import { artworks, featuredArtwork, arArtwork } from '../lib/artworks';

export default function HomePage() {
  return (
    <main>
      <nav className="nav">
        <div className="nav-inner">
          <a href="#top" className="brand">Jiri Hauschka</a>
          <div className="links">
            <a href="#works">Works</a>
            <a href="#ar">View on your wall</a>
            <a href="#bio">Biography</a>
            <a href="#contact">Contact</a>
          </div>
        </div>
      </nav>

      <header className="hero" id="top">
        <div className="hero-inner">
          <div>
            <div className="eyebrow">Czech painter · Prague</div>
            <h1>Jiri<br />Hauschka</h1>
            <p className="lead">Paintings between abstraction, figuration and magical realism.</p>
            <div className="actions">
              <a className="btn primary" href="#works">View works</a>
              <Link className="btn ghost" href="/ar/colored-moments">View on your wall</Link>
            </div>
          </div>
          <figure className="hero-art">
            <img src={featuredArtwork.image} alt={`${featuredArtwork.title} by Jiri Hauschka`} />
            <figcaption className="caption">{featuredArtwork.title}, {featuredArtwork.year}</figcaption>
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
              <div className="kicker">Selected works</div>
              <h2 className="title">Recent paintings.</h2>
            </div>
            <p className="small-copy">Large images, clear details, minimal interface.</p>
          </div>
          <div className="works-grid">
            {artworks.map((artwork) => (
              <article className="work" key={artwork.slug}>
                <div className="work-img"><img src={artwork.image} alt={artwork.title} /></div>
                <div className="work-meta">
                  <h3>{artwork.title}</h3>
                  <p>{artwork.year} · {artwork.medium} · {artwork.size}</p>
                  {artwork.ar ? <Link href={`/ar/${artwork.slug}`}>View on your wall</Link> : null}
                </div>
              </article>
            ))}
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
            <img className="wall-art" src={arArtwork.poster} alt="AR artwork mockup" />
          </div>
        </div>
      </section>

      <section id="bio">
        <div className="wrap bio">
          <p className="text">Born in Šumperk, Jiri Hauschka lives and works in Prague. His paintings are held in the National Gallery Prague and private collections internationally.</p>
          <div className="facts">
            <div className="fact"><strong>Born</strong><span>1965, Šumperk</span></div>
            <div className="fact"><strong>Based in</strong><span>Prague, Czech Republic</span></div>
            <div className="fact"><strong>Medium</strong><span>Acrylic on canvas</span></div>
            <div className="fact"><strong>Focus</strong><span>Nature, memory, symbolic landscapes</span></div>
          </div>
        </div>
      </section>

      <section id="contact">
        <div className="wrap contact">
          <h2>For exhibitions, acquisitions and enquiries.</h2>
          <p>A simple contact flow for collectors, galleries and curators.</p>
          <a className="btn primary" href="mailto:jirihauschka@seznam.cz">Contact</a>
        </div>
      </section>
    </main>
  );
}

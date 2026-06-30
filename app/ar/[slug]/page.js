import Link from 'next/link';
import { artworks } from '../../../lib/artworks';
import ModelViewer from '../../../components/ModelViewer';
import ArSelector from '../../../components/ArSelector';

export function generateStaticParams() {
  return artworks.filter((a) => a.ar).map((a) => ({ slug: a.slug }));
}

export default async function ArtworkArPage({ params }) {
  const { slug } = await params;
  const artwork = artworks.find((a) => a.slug === slug && a.ar);

  if (!artwork) {
    return <main className="ar-page"><Link className="back" href="/">← Back</Link><h1>AR not available.</h1></main>;
  }

  return (
    <main className="ar-page">
      <nav className="nav">
        <div className="nav-inner">
          <Link href="/" className="brand">Jiri Hauschka</Link>
          <div className="links">
            <Link href="/#works">Works</Link>
            <Link href="/#bio">Bio</Link>
            <Link href="/exhibitions">Exhibitions</Link>
            <span className="nav-active">AR</span>
            <Link href="/#contact">Contact</Link>
          </div>
        </div>
      </nav>

      <section className="ar-page-hero">
        <div className="wrap ar-page-top">
          <div className="ar-page-info">
            <div className="kicker light">Augmented reality</div>
            <ArSelector currentSlug={slug} />
            <div className="ar-meta">{artwork.year} · {artwork.medium}{artwork.size ? ` · ${artwork.size}` : ''}</div>
            <p className="ar-hint">Tap the AR button below to place this painting on your wall.</p>
          </div>
        </div>
      </section>

      <section className="viewer-section">
        <div className="viewer-wrap">
          <ModelViewer artwork={artwork} />
        </div>
      </section>

      <footer className="footer ar-footer">
        <Link href="/">← Back to paintings</Link>
      </footer>
    </main>
  );
}

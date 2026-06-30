import Link from 'next/link';
import ModelViewer from '../../../components/ModelViewer';
import { artworks } from '../../../lib/artworks';

export function generateStaticParams() {
  return artworks.filter((artwork) => artwork.ar).map((artwork) => ({ slug: artwork.slug }));
}

export default async function ArtworkArPage({ params }) {
  const { slug } = await params;
  const artwork = artworks.find((item) => item.slug === slug && item.ar);

  if (!artwork) {
    return <main className="ar-page"><Link className="back" href="/">← Back</Link><h1>AR preview not available.</h1></main>;
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
            <h1>{artwork.title}</h1>
            <div className="ar-meta">{artwork.year} · {artwork.medium}{artwork.size ? ` · ${artwork.size}` : ''}</div>
            <p className="ar-hint">Open this page on a mobile device and tap the AR button. Use Safari on iPhone or Chrome on Android.</p>
          </div>
          <div className="ar-page-links">
            <a className="btn primary" rel="ar" href={artwork.usdz}>Open on iPhone</a>
            <a className="btn secondary" href={`intent://arvr.google.com/scene-viewer/1.0?file=${encodeURIComponent(`https://preview.jirihauschka.com${artwork.glb}`)}&mode=ar_only&title=${encodeURIComponent(artwork.title)}#Intent;scheme=https;package=com.google.ar.core;action=android.intent.action.VIEW;end;`}>Open on Android</a>
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

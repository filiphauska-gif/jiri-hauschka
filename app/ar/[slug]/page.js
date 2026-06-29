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
      <Link className="back" href="/">← Back</Link>
      <section className="ar-copy-page">
        <div className="eyebrow">AR proof of concept</div>
        <h1>{artwork.title}</h1>
        <div className="meta">{artwork.year} · {artwork.medium} · {artwork.size}</div>
        <p className="hint">Open this page on a supported mobile device. Use Safari on iPhone or Chrome on Android for the real camera AR mode.</p>
      </section>
      <section className="viewer">
        <ModelViewer artwork={artwork} />
      </section>
    </main>
  );
}

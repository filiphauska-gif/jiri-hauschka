'use client';

import { useEffect } from 'react';

export default function ModelViewer({ artwork }) {
  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
  }, []);

  const glbUrl = `https://preview.jirihauschka.com${artwork.glb}`;
  const usdzUrl = artwork.usdz ? `https://preview.jirihauschka.com${artwork.usdz}` : glbUrl;

  return (
    <div className="model-container">
      <model-viewer
        src={artwork.glb}
        poster={artwork.poster || artwork.image}
        alt={`${artwork.title} by Jiri Hauschka`}
        camera-controls=""
        touch-action="pan-y"
        shadow-intensity="0.3"
        exposure="1.2"
        interaction-prompt="none"
        class="ar-model"
      ></model-viewer>

      <a className="ar-visual-button" rel="ar" href={usdzUrl}>
        <span className="ar-ar-icon">AR</span>
        View on your wall
      </a>
    </div>
  );
}

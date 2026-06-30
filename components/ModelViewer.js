'use client';

import { useEffect } from 'react';

export default function ModelViewer({ artwork }) {
  useEffect(() => {
    // Pre-load model-viewer for the AR button functionality
    import('@google/model-viewer').catch(() => {});
  }, []);

  return (
    <div className="model-container">
      <div className="model-poster-wrap">
        <img
          className="model-poster-img"
          src={artwork.poster || artwork.image}
          alt={artwork.title}
        />
      </div>

      <model-viewer
        src={artwork.glb}
        ios-src={artwork.usdz}
        poster={artwork.poster || artwork.image}
        alt={`${artwork.title} by Jiri Hauschka`}
        ar=""
        ar-modes="webxr scene-viewer quick-look"
        ar-placement="wall"
        ar-scale="auto"
        class="ar-model-hidden"
      >
        <button slot="ar-button" className="ar-ar-button">
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </button>
      </model-viewer>
    </div>
  );
}

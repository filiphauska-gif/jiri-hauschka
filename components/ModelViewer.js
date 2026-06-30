'use client';

import { useEffect } from 'react';

export default function ModelViewer({ artwork }) {
  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
  }, []);

  return (
    <div className="model-container">
      <model-viewer
        src={artwork.glb}
        ios-src={artwork.usdz}
        poster={artwork.poster || artwork.image}
        alt={`${artwork.title} by Jiri Hauschka`}
        ar=""
        ar-modes="webxr scene-viewer quick-look"
        ar-placement="wall"
        ar-scale="auto"
        camera-controls=""
        touch-action="pan-y"
        shadow-intensity="0.3"
        exposure="1.2"
        interaction-prompt="none"
        class="ar-model"
      >
        <button slot="ar-button" className="ar-visual-button">
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </button>
      </model-viewer>
    </div>
  );
}

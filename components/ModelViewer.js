'use client';

import { useEffect, useRef } from 'react';

export default function ModelViewer({ artwork }) {
  const containerRef = useRef(null);

  useEffect(() => {
    import('@google/model-viewer').then(() => {
      // Model-viewer is loaded, the custom element will work
    }).catch((err) => {
      console.error('Failed to load model-viewer:', err);
    });
  }, []);

  return (
    <div className="model-container" ref={containerRef}>
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
        exposure="1"
        environment-image="neutral"
        interaction-prompt="when-focused"
        orientation="0 0 180deg"
        class="ar-model"
      >
        <button slot="ar-button" className="ar-ar-button">
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </button>
      </model-viewer>
    </div>
  );
}

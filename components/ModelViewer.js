'use client';

import { useEffect, useRef } from 'react';

export default function ModelViewer({ artwork }) {
  useEffect(() => {
    import('@google/model-viewer').catch(err => console.error('MV error:', err));
  }, []);

  return (
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
      camera-orbit="0deg 0deg 1.5m"
      touch-action="pan-y"
      shadow-intensity="0.3"
      exposure="1"
      environment-image="neutral"
      interaction-prompt="when-focused"
      class="ar-model"
    >
      <button slot="ar-button" className="ar-ar-button">
        <span className="ar-ar-icon">AR</span>
        View on your wall
      </button>
    </model-viewer>
  );
}

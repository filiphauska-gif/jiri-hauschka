'use client';

import { useEffect } from 'react';

export default function ModelViewer({ artwork }) {
  useEffect(() => {
    import('@google/model-viewer');
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
      touch-action="pan-y"
      shadow-intensity="0.5"
      exposure="0.8"
      environment-image="neutral"
      auto-rotate=""
      interaction-prompt="none"
      class="ar-model"
    >
      <button slot="ar-button" class="ar-ar-button">
        <span class="ar-ar-icon">AR</span>
        View on your wall
      </button>
    </model-viewer>
  );
}

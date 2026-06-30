'use client';

import { useEffect, useRef } from 'react';

export default function ModelViewer({ artwork }) {
  const mvRef = useRef(null);

  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
  }, []);

  const handleAR = () => {
    const mv = mvRef.current;
    if (mv && mv.activateAR) {
      mv.activateAR();
    }
  };

  return (
    <div className="model-container">
      <model-viewer
        ref={mvRef}
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
      ></model-viewer>

      <button className="ar-visual-button" onClick={handleAR}>
        <span className="ar-ar-icon">AR</span>
        View on your wall
      </button>
    </div>
  );
}

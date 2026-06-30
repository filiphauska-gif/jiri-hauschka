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
      <div className="model-poster-wrap">
        <img
          className="model-poster-img"
          src={artwork.poster || artwork.image}
          alt={artwork.title}
        />
      </div>

      <button className="ar-visual-button" onClick={handleAR}>
        <span className="ar-ar-icon">AR</span>
        View on your wall
      </button>

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
        class="ar-model-hidden"
      >
        <button slot="ar-button" className="ar-ar-button-hidden"></button>
      </model-viewer>
    </div>
  );
}

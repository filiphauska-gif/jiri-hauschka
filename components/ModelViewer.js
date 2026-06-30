'use client';

import { useEffect, useRef } from 'react';

export default function ModelViewer({ artwork }) {
  const mvRef = useRef(null);

  useEffect(() => {
    import('@google/model-viewer').then(() => {
      console.log('model-viewer loaded');
    }).catch((e) => {
      console.error('model-viewer failed:', e);
    });
  }, []);

  const handleAR = () => {
    const mv = mvRef.current;
    if (mv) {
      console.log('model-viewer element:', mv);
      if (typeof mv.activateAR === 'function') {
        console.log('calling activateAR...');
        try {
          mv.activateAR();
        } catch (e) {
          console.error('activateAR error:', e);
        }
      } else {
        console.log('activateAR not available, trying rel=ar fallback');
        // Fallback: directly open the GLB
        const a = document.createElement('a');
        a.rel = 'ar';
        a.href = `https://preview.jirihauschka.com${artwork.usdz || artwork.glb}`;
        a.click();
      }
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

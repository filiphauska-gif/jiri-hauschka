'use client';

import { useEffect, useRef } from 'react';

export default function ModelViewer({ artwork }) {
  const mvRef = useRef(null);

  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
  }, []);

  const handleAR = async () => {
    const mv = mvRef.current;
    if (!mv) return;

    // Try activateAR first (works on iOS via Quick Look, Android via Scene Viewer)
    if (typeof mv.activateAR === 'function') {
      try {
        await mv.activateAR();
        return; // Success!
      } catch (e) {
        console.log('activateAR failed, trying fallback:', e);
      }
    }

    // Fallback: try rel="ar" link
    const srcUrl = `https://preview.jirihauschka.com${artwork.usdz || artwork.glb}`;
    const a = document.createElement('a');
    a.rel = 'ar';
    a.href = srcUrl;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
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

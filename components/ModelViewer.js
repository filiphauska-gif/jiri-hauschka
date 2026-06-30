'use client';

import { useEffect, useRef, useState } from 'react';

export default function ModelViewer({ artwork }) {
  const mvRef = useRef(null);
  const [isInApp, setIsInApp] = useState(false);

  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
    const ua = navigator.userAgent;
    // Detect Facebook, Messenger, Instagram in-app browsers
    if (/FBAN|FBAV|FB_IAB|FBIOS|Instagram|Messenger/i.test(ua)) {
      setIsInApp(true);
    }
  }, []);

  const handleAR = () => {
    const mv = mvRef.current;
    if (mv && mv.activateAR) {
      mv.activateAR();
    }
  };

  const openInSafari = () => {
    // Try to open current URL in Safari
    const url = window.location.href;
    // iOS scheme to open Safari
    window.location.href = url.replace(/^https:\/\//, 'x-safari-https://');
  };

  return (
    <div className="model-container">
      {isInApp && (
        <div className="inapp-banner">
          <p>AR doesn't work in this browser. Please open in Safari.</p>
          <button className="inapp-btn" onClick={openInSafari}>Open in Safari</button>
        </div>
      )}

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

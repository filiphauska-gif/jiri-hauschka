'use client';

import { useEffect, useState } from 'react';

export default function ModelViewer({ artwork }) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
    const ua = navigator.userAgent;
    setIsMobile(/iphone|ipad|ipod|android/i.test(ua));
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
      ></model-viewer>

      {isMobile && (
        <a
          className="ar-visual-button"
          rel="ar"
          href={`https://preview.jirihauschka.com${artwork.usdz || artwork.glb}`}
        >
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </a>
      )}
    </div>
  );
}

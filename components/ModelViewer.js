'use client';

import { useEffect, useState } from 'react';

export default function ModelViewer({ artwork }) {
  const [isIOS, setIsIOS] = useState(false);

  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
    setIsIOS(/iphone|ipad|ipod/i.test(navigator.userAgent));
  }, []);

  const glbUrl = `https://preview.jirihauschka.com${artwork.glb}`;
  const srcUrl = artwork.usdz
    ? `https://preview.jirihauschka.com${artwork.usdz}`
    : glbUrl;

  const sceneViewerUrl = `intent://arvr.google.com/scene-viewer/1.0?file=${encodeURIComponent(glbUrl)}&mode=ar_only&title=${encodeURIComponent(artwork.title)}#Intent;scheme=https;package=com.google.ar.core;action=android.intent.action.VIEW;end;`;

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

      {isIOS ? (
        <a className="ar-visual-button" rel="ar" href={srcUrl}>
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </a>
      ) : (
        <a className="ar-visual-button" href={sceneViewerUrl}>
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </a>
      )}
    </div>
  );
}

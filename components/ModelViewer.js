'use client';

import { useEffect, useState } from 'react';

export default function ModelViewer({ artwork }) {
  const [device, setDevice] = useState(null);

  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
    const ua = navigator.userAgent;
    if (/iphone|ipad|ipod/i.test(ua)) setDevice('ios');
    else if (/android/i.test(ua)) setDevice('android');
    else setDevice('desktop');
  }, []);

  const glbUrl = `https://preview.jirihauschka.com${artwork.glb}`;
  const usdzUrl = artwork.usdz ? `https://preview.jirihauschka.com${artwork.usdz}` : glbUrl;
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

      <div className="ar-actions">
        {device === 'ios' && (
          <a className="ar-visual-button" rel="ar" href={usdzUrl}>
            <span className="ar-ar-icon">AR</span>
            View on your wall
          </a>
        )}
        {device === 'android' && (
          <a className="ar-visual-button" href={sceneViewerUrl}>
            <span className="ar-ar-icon">AR</span>
            View on your wall
          </a>
        )}
        {device === 'desktop' && (
          <p className="ar-desktop-hint">Open this page on your phone to try AR</p>
        )}
      </div>
    </div>
  );
}

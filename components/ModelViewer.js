'use client';

import { useEffect } from 'react';

export default function ModelViewer({ artwork }) {
  useEffect(() => {
    import('@google/model-viewer');
  }, []);

  const glbUrl = typeof window !== 'undefined' ? new URL(artwork.glb, window.location.href).href : artwork.glb;
  const fallbackUrl = typeof window !== 'undefined' ? window.location.href : '';
  const sceneViewerUrl = `intent://arvr.google.com/scene-viewer/1.0?file=${encodeURIComponent(glbUrl)}&mode=ar_only&title=${encodeURIComponent(artwork.title)}#Intent;scheme=https;package=com.google.ar.core;action=android.intent.action.VIEW;S.browser_fallback_url=${encodeURIComponent(fallbackUrl)};end;`;

  return (
    <>
      <div className="ar-actions">
        <a className="camera-btn" rel="ar" href={artwork.usdz}>
          <img src={artwork.poster} alt="" />
          <span>Open camera AR on iPhone</span>
        </a>
        <a className="android-btn" href={sceneViewerUrl}>Open camera AR on Android</a>
      </div>

      <model-viewer
        src={artwork.glb}
        ios-src={artwork.usdz}
        poster={artwork.poster}
        alt={`${artwork.title} by Jiri Hauschka`}
        ar=""
        ar-modes="webxr scene-viewer quick-look"
        ar-placement="wall"
        ar-scale="fixed"
        camera-controls=""
        touch-action="pan-y"
        shadow-intensity="0.25"
        exposure="1"
      >
        <button id="ar-button" slot="ar-button">View on your wall</button>
      </model-viewer>
    </>
  );
}

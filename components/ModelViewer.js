'use client';

import { useEffect, useState } from 'react';

export default function ModelViewer({ artwork }) {
  const [device, setDevice] = useState(null);

  useEffect(() => {
    import('@google/model-viewer');
    // Detect device
    const ua = navigator.userAgent;
    if (/iphone|ipad|ipod/i.test(ua)) setDevice('ios');
    else if (/android/i.test(ua)) setDevice('android');
    else setDevice('desktop');
  }, []);

  const glbUrl = `https://preview.jirihauschka.com${artwork.glb}`;
  const sceneViewerUrl = `intent://arvr.google.com/scene-viewer/1.0?file=${encodeURIComponent(glbUrl)}&mode=ar_only&title=${encodeURIComponent(artwork.title)}#Intent;scheme=https;package=com.google.ar.core;action=android.intent.action.VIEW;end;`;

  return (
    <>
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
        interaction-prompt="none"
        class="ar-model"
      >
        <button slot="ar-button" className="ar-ar-button">
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </button>
      </model-viewer>

      {device && device !== 'desktop' && (
        <div className="ar-fallback">
          {device === 'ios' && (
            <a className="btn primary" rel="ar" href={artwork.usdz}>
              <span className="ar-ar-icon">AR</span> Open on your iPhone
            </a>
          )}
          {device === 'android' && (
            <a className="btn primary" href={sceneViewerUrl}>
              <span className="ar-ar-icon">AR</span> Open on your Android
            </a>
          )}
        </div>
      )}
    </>
  );
}

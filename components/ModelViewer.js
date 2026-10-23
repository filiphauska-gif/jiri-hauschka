'use client';

import { useEffect, useRef, useState } from 'react';

export default function ModelViewer({ artwork }) {
  const mvRef = useRef(null);
  const [isInApp, setIsInApp] = useState(false);
  const [plat, setPlat] = useState({ ios: false, android: false, mobile: true });
  const [arFailed, setArFailed] = useState(false);

  useEffect(() => {
    import('@google/model-viewer').catch(() => {});
    const ua = navigator.userAgent;
    const ios = /iPad|iPhone|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    const android = /Android/i.test(ua);
    const chromium = /Chrome\/|SamsungBrowser|EdgA|OPR\//.test(ua) && !/Firefox|FxiOS/i.test(ua);
    // Facebook, Messenger, Instagram in-app browsers
    const inapp = /FBAN|FBAV|FB_IAB|FBIOS|Instagram|Messenger/i.test(ua);
    setIsInApp(inapp);
    setPlat({ ios, android, chromium, mobile: ios || android });

    // Catch AR launch failures reported by model-viewer
    const mv = mvRef.current;
    if (mv) {
      const onArStatus = (e) => {
        if (e.detail && e.detail.status === 'failed') setArFailed(true);
      };
      mv.addEventListener('ar-status', onArStatus);
      return () => mv.removeEventListener('ar-status', onArStatus);
    }
  }, []);

  const handleAR = async () => {
    const mv = mvRef.current;
    if (!mv) return;
    try {
      // Wait until the model is loaded so canActivateAR is reliable
      if (!mv.loaded) {
        await new Promise((resolve) => {
          const done = () => resolve();
          mv.addEventListener('load', done, { once: true });
          setTimeout(done, 4000);
        });
      }
      if (mv.canActivateAR && typeof mv.activateAR === 'function') {
        await mv.activateAR();
      } else {
        setArFailed(true);
      }
    } catch {
      setArFailed(true);
    }
  };

  // iOS: undocumented scheme that hands the URL over to Safari
  const openInSafari = () => {
    window.location.href = window.location.href.replace(/^https:\/\//, 'x-safari-https://');
  };

  // Android: intent that opens the current URL in Chrome
  const openInChrome = () => {
    const rest = window.location.href.replace(/^https?:\/\//, '');
    window.location.href = `intent://${rest}#Intent;scheme=https;package=com.android.chrome;end`;
  };

  return (
    <div className="model-container">
      {isInApp && (
        <div className="inapp-banner">
          <p>AR doesn't work in this browser. Open this page in {plat.ios ? 'Safari' : 'Chrome'}.</p>
          <button className="inapp-btn" onClick={plat.ios ? openInSafari : openInChrome}>
            Open in {plat.ios ? 'Safari' : 'Chrome'}
          </button>
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

      {plat.mobile ? (
        <button className="ar-visual-button" onClick={handleAR}>
          <span className="ar-ar-icon">AR</span>
          View on your wall
        </button>
      ) : (
        <p className="ar-desktop-hint">AR is available on your phone.</p>
      )}

      {!isInApp && arFailed && (
        <div className="inapp-banner">
          <p>
            {plat.ios
              ? 'AR works only in Safari on iPhone. Open this page in Safari to try it.'
              : plat.android
                ? 'AR could not start. Your phone may be missing \u201CGoogle Play Services for AR\u201D (ARCore).'
                : "AR isn't available in this browser."}
          </p>
          <div className="inapp-actions">
            {plat.ios && <button className="inapp-btn" onClick={openInSafari}>Open in Safari</button>}
            {plat.android && (
              <>
                <a className="inapp-btn" href="https://play.google.com/store/apps/details?id=com.google.ar.core" target="_blank" rel="noopener">Get ARCore</a>
                {!plat.chromium && <button className="inapp-btn" onClick={openInChrome}>Open in Chrome</button>}
              </>
            )}
          </div>
        </div>
      )}

      <img className="ar-static-preview" src={artwork.image} alt={`${artwork.title} by Jiri Hauschka`} />
    </div>
  );
}

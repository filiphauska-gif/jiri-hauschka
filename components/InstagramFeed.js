'use client';
import { useEffect, useState, useRef } from 'react';

export default function InstagramFeed() {
  const containerRef = useRef(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (loaded) return;

    // Load the plugin CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://jirihauschka.com/wp-content/plugins/instagram-feed/css/sbi-styles.min.css';
    document.head.appendChild(link);

    // Fetch the feed HTML from WordPress REST API
    fetch('https://jirihauschka.com/wp-json/wp/v2/pages/1706?_fields=content')
      .then(r => r.json())
      .then(data => {
        if (containerRef.current) {
          containerRef.current.innerHTML = data.content.rendered;
        }
        // Load the plugin JS to populate images
        const script = document.createElement('script');
        script.src = 'https://jirihauschka.com/wp-content/plugins/instagram-feed/js/sbi-scripts.min.js';
        script.async = true;
        script.onload = () => setLoaded(true);
        document.body.appendChild(script);
      })
      .catch(() => {
        if (containerRef.current) {
          containerRef.current.innerHTML = '<p style="text-align:center;color:var(--muted);padding:40px">Instagram feed unavailable.</p>';
        }
      });
  }, [loaded]);

  return (
    <div className="insta-feed-clean">
      <div ref={containerRef}></div>
    </div>
  );
}

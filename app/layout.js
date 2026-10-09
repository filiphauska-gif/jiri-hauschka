import './globals.css';
import Script from 'next/script';

const GA_ID = 'G-77VNHD7BXJ';

export const metadata = {
  title: 'Jiri Hauschka — Czech Painter',
  description: 'Contemporary Czech painter. Paintings between abstraction, figuration and magical realism. Available for exhibitions and sales.',
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: '48x48' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/icon-192.png', sizes: '192x192', type: 'image/png' },
    ],
    apple: '/apple-touch-icon.png',
  },
  openGraph: {
    title: 'Jiri Hauschka — Czech Painter',
    description: 'Contemporary Czech painter. Paintings between abstraction, figuration and magical realism.',
    url: 'https://jirihauschka.com',
    siteName: 'Jiri Hauschka',
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Jiri Hauschka — Czech Painter',
    description: 'Contemporary Czech painter. Paintings between abstraction, figuration and magical realism.',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <meta property="og:title" content="Jiri Hauschka — Czech Painter" />
        <meta property="og:description" content="Contemporary Czech painter. Paintings between abstraction, figuration and magical realism." />
        <meta property="og:url" content="https://jirihauschka.com" />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content="Jiri Hauschka" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Jiri Hauschka — Czech Painter" />
        <meta name="twitter:description" content="Contemporary Czech painter. Paintings between abstraction, figuration and magical realism." />
        <meta name="robots" content="index, follow" />
        <meta name="theme-color" content="#0a0a0a" />
        <link rel="canonical" href="https://jirihauschka.com" />
      </head>
      <body>
        {children}
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
          strategy="afterInteractive"
        />
        <Script id="ga-init" strategy="afterInteractive">
          {`window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', '${GA_ID}');`}
        </Script>
      </body>
    </html>
  );
}


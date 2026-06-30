import './globals.css';

export const metadata = {
  title: 'Jiri Hauschka — Czech Painter',
  description: 'Contemporary Czech painter. Paintings between abstraction, figuration and magical realism. Available for exhibitions and sales.',
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
        <link rel="canonical" href="https://preview.jirihauschka.com" />
      </head>
      <body>{children}</body>
    </html>
  );
}

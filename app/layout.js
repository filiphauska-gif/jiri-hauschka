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
  alternates: {
    canonical: 'https://preview.jirihauschka.com',
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

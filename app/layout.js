import './globals.css';

export const metadata = {
  title: 'Jiri Hauschka',
  description: 'Czech painter — portfolio and AR artwork preview.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

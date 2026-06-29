import Link from 'next/link';

export default function ExhibitionsPage() {
  const exhibitions = [
    { year: '2024', title: 'National Gallery Prague', place: 'Prague, Czech Republic', note: 'Group exhibition — Contemporary Czech Landscape' },
    { year: '2023', title: 'Solo Exhibition', place: 'Galerie Kritiků, Prague', note: 'New works' },
    { year: '2022', title: 'Art Prague Fair', place: 'Prague', note: '' },
    { year: '2021', title: 'Galerie Mánes', place: 'Prague, Czech Republic', note: '' },
    { year: '2019', title: 'Kunsthalle Praha', place: 'Prague, Czech Republic', note: '' },
    { year: '2017', title: 'Galerie Václava Špály', place: 'Prague, Czech Republic', note: '' },
  ];

  return (
    <main>
      <nav className="nav">
        <div className="nav-inner">
          <Link href="/#top" className="brand">Jiri Hauschka</Link>
          <div className="links">
            <Link href="/#works">Works</Link>
            <Link href="/#bio">Bio</Link>
            <span className="nav-active">Exhibitions</span>
            <Link href="/#ar">AR</Link>
            <Link href="/#contact">Contact</Link>
          </div>
        </div>
      </nav>

      <section className="page-top">
        <div className="wrap">
          <h1>Exhibitions</h1>
        </div>
      </section>

      <section>
        <div className="wrap">
          <div className="exh-list">
            {exhibitions.map((exh, i) => (
              <div className="exh-item" key={i}>
                <div className="exh-year">{exh.year}</div>
                <div className="exh-detail">
                  <strong>{exh.title}</strong>
                  <span className="exh-place">{exh.place}</span>
                  {exh.note && <span className="exh-note">{exh.note}</span>}
                </div>
              </div>
            ))}
          </div>
          <div className="back-link">
            <Link href="/">&larr; Back</Link>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="wrap">&copy; Jiri Hauschka</div>
      </footer>
    </main>
  );
}

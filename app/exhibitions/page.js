import Link from 'next/link';

const soloExhibitions = [
  { year: '2025', title: 'ARMA Gallery, Madrid (Spain)' },
  { year: '2025', title: 'Tropicals, MAAT Gallery, Paris (France)' },
  { year: '2024', title: 'CRAG Gallery, Turin (Italy)' },
  { year: '2024', title: 'Your Endless Summer, Sabine Bayasli Gallery, Paris (France)' },
  { year: '2023', title: 'Gallery Schlassgoart, Esch (Luxembourg)' },
  { year: '2022', title: 'UFFO Gallery, Trutnov (Czechia)' },
  { year: '2020', title: 'CRAG Gallery, Turin (Italy)' },
  { year: '2019', title: 'Black Swan Gallery, Prague (Czechia)' },
  { year: '2017', title: 'Quintus Gallery, Watkins Glen (USA)' },
  { year: '2015', title: 'House Art Gallery, In the Middle of Somewhere, Prague (Czechia)' },
  { year: '2014', title: 'Oko Gallery (Town Hall Gallery), Opava (Czechia)' },
  { year: '2013', title: "Michal's Collection Gallery (with Albert Ruiz Villar), Prague (Czechia)" },
  { year: '2012', title: '21st Century Gallery, Prague (Czechia)' },
  { year: '2011', title: 'Red Gate Gallery, London (with J. Valecka) (United Kingdom)' },
  { year: '2011', title: 'Rabas Gallery, Rakovník (Czechia)' },
  { year: '2010', title: 'Kotelna Gallery, Říčany (Czechia)' },
  { year: '2010', title: 'XXL Gallery, Louny (Czechia)' },
  { year: '2006', title: 'The Residence Gallery, London (United Kingdom)' },
  { year: '2005', title: 'Town Hall Gallery Prachatice (Czechia)' },
  { year: '2004', title: 'Library Gallery Liberec (Czechia)' },
];

const groupExhibitions = [
  { year: '2023', title: 'Stuckists in Ostrov, Gallery Karlovy Vary (Czechia)' },
  { year: '2016', title: 'The Stuckists, View Two Gallery, Liverpool (United Kingdom)' },
  { year: '2013', title: 'Stuck between Prague and London, Nolias Gallery, London (United Kingdom)' },
  { year: '2013', title: 'STUCK in Pardubice, Town Hall Gallery Pardubice (Czechia)' },
  { year: '2012', title: 'Stuckists: Elizabethian Avant-Garde, Bermondsey Gallery, London (United Kingdom)' },
  { year: '2012', title: 'Original and perspective, Klatovy – Klenová Gallery (Czechia)' },
  { year: '2011', title: 'Enemies of Art, Lauderdale House Gallery, London (United Kingdom)' },
  { year: '2011', title: 'Prague stuckists, Town Hall Gallery Chrudim (Czechia)' },
  { year: '2010', title: 'Summer choice, Gallery Vltavín, Prague (Czechia)' },
  { year: '2007', title: "Stuck in the middle of November, Topičův salon Gallery, Prague (Czechia)" },
  { year: '2006', title: 'The Brighton Stuckists, Art House Gallery, Brighton (United Kingdom)' },
];

function ExhibitionGroup({ title, exhibitions }) {
  const sorted = [...exhibitions].sort((a, b) => b.year - a.year);

  return (
    <div className="exhibition-group">
      <h2>{title}</h2>
      <div className="ex-list">
        {sorted.map((ex, i) => (
          <div key={i} className="ex-item">
            <span className="ex-year">{ex.year}</span>
            <span className="ex-title">{ex.title}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function ExhibitionsPage() {
  return (
    <main className="ar-page">
      <nav className="nav">
        <div className="nav-inner">
          <Link href="/" className="brand">Jiri Hauschka</Link>
          <div className="links">
            <Link href="/#works">Works</Link>
            <Link href="/#bio">Bio</Link>
            <span className="nav-active">Exhibitions</span>
            <Link href="/ar/colored-moments">AR</Link>
            <Link href="/#contact">Contact</Link>
          </div>
        </div>
      </nav>

      <section className="exhibitions-page">
        <div className="wrap">
          <h1>Exhibitions</h1>

          <ExhibitionGroup title="Solo Exhibitions" exhibitions={soloExhibitions} />
          <ExhibitionGroup title="Group Exhibitions" exhibitions={groupExhibitions} />
        </div>
      </section>

      <footer className="footer ar-footer">
        <Link href="/">← Back</Link>
      </footer>
    </main>
  );
}

import Link from 'next/link';

const martinText = [
  'Paintings by Jiri Hauschka take us to an environment of confrontation, or rather symbiosis, of man and nature. Nature influences us more than we admit. Some painters have sensed it for a long time – especially in places where there\'s a bit more of it, like in the northern regions with plenty of forests and lakes and bubbling streams, or in the south with jungles and waterfalls and howling monkeys. In nature, events involving man may be more raw, more to the bone. The name of my text concerning Hauschka\'s paintings is a reference to David Lynch\'s legendary TV series that was set in a similar northern environment. You may remember Twin Peaks, a town at the US-Canadian border, with a rural atmosphere, forests, mountains, a sawmill, a roadhouse and an actual sheriff. And – of course – with a bizarre story and characters that were so real and believable that we got entangled in a story without a narrative sense that was not supposed to be grasped rationally. We, the viewers on the verge of obsession, were getting increasingly immersed and feverishly excited – cooled only by the cold raw mountain wind – to the point where we even expected to find a wrapped corpse behind a random tree in our local woods. After Lynch\'s quintessential Twin Peaks, everything was different. Maybe this is another guide how to look at Hauschka\'s paintings. To accompany him to his tidy painting wilderness.',
  'In recent years, or rather in the last two decades, we witness the art of painting looking back at its history, examining its options, seeking what is still attractive and alive in past layers, and finally realizing, to its surprise, that it can still invigorate today\'s audience through its colours, views, compositions and ideas, and be attractive for contemporary artists. And it realizes, that figures set in a certain spatial or scenic configuration possess a visual and semantic potency that upsets and attracts a contemporary person just as it did in the decades and centuries before us. Fragments of past visuals are pieced together with the fragments of tomorrow\'s imagination.',
  'Jiri Hauschka turns to this type of painting method that utilizes colours and symbolic connotations, prevalent at the turn of the 20th century – he positions himself in that period next to the Canadian painter Tom Thomson (1877–1917) – and used by contemporary painters. Reality is transformed by the painter\'s narration into layered storytelling, where the artist\'s memory is interspersed with new experiences, views, desires and emotional turbulences. In the case of Jiri Hauschka, we find ourselves in the wilderness of painter nostalgia, where we look for the conceptual person, and in urban civilization, which has barely any options left and where we can therefore feel and see the colours of wilderness. Ultimately, we can be justified in our impression that nothing is as it seems at the first and second glance.',
];

export default function BioPage() {
  return (
    <main className="ar-page">
      <nav className="nav">
        <div className="nav-inner">
          <Link href="/" className="brand">Jiri Hauschka</Link>
          <div className="links">
            <Link href="/#works">Works</Link>
            <span className="nav-active">Bio</span>
            <Link href="/exhibitions">Exhibitions</Link>
            <Link href="/#ar">AR</Link>
            <Link href="/#contact">Contact</Link>
          </div>
        </div>
      </nav>

      <section className="bio-page">
        <div className="wrap">
          <h1>Biography</h1>

          <div className="bio-hero">
            <img className="bio-portrait" src="/assets/jiri-portrait.png" alt="Jiri Hauschka" />
            <div className="bio-hero-text">
              <blockquote className="bio-quote-main">
                "I am like a fascinated pilgrim and painting is the best way, how to show, what the world of my pilgrimage looks like."
              </blockquote>
              <p className="bio-quote-author">— Jiri Hauschka</p>
              <div className="bio-facts-inline">
                <p><strong>1965</strong> Born, Šumperk, Northern Moravia, Czechia</p>
                <p>Currently lives and works in Prague</p>
              </div>
            </div>
          </div>

          <blockquote className="bio-quote">
            <p>"Jiri Hauschka is one of the most interesting artists to have emerged in the Czech Republic during the quarter of century that has followed the fall of the Communist regime."</p>
            <cite>— Edward Lucie-Smith</cite>
          </blockquote>

          <div className="bio-text">
            <h2>The owls are not what they seem</h2>
            {martinText.map((p, i) => (
              <p key={i}>{p}</p>
            ))}
            <p className="bio-text-author">— Martin Dostal</p>
          </div>
        </div>
      </section>

      <footer className="footer ar-footer">
        <Link href="/">← Back</Link>
      </footer>
    </main>
  );
}

import Link from "next/link";
import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";
import { allArticles, TOPICS } from "@/lib/library";

export const metadata = {
  title: "Library",
  description: "Guides on speech structure, humor, delivery and storytelling, for club speakers and anyone who speaks in public.",
};

export default function Library() {
  const articles = allArticles();
  return (
    <>
      <Header />
      <main className="wrap lib">
        <section className="help-hero">
          <span className="eyebrow">Library</span>
          <h1>Get better at <em>speaking</em></h1>
          <p className="lede">Practical guides on structure, humor, delivery and storytelling. Short enough to read before you rehearse.</p>
        </section>

        <nav className="chips" aria-label="Topics">
          {TOPICS.filter((t) => articles.some((a) => a.topic === t.id)).map((t) => <a key={t.id} href={`#${t.id}`}>{t.label}</a>)}
        </nav>

        {TOPICS.map((t) => {
          const list = articles.filter((a) => a.topic === t.id);
          if (!list.length) return null;
          return (
            <section key={t.id} id={t.id} className="lib-topic">
              <h2>{t.label}</h2>
              <p className="blurb">{t.blurb}</p>
              <div className="lib-grid">
                {list.map((a) => (
                  <Link key={a.slug} href={`/library/${a.slug}`} className="lib-card">
                    <h3>{a.title}</h3>
                    <p>{a.summary}</p>
                    <span>{a.minutes} min read</span>
                  </Link>
                ))}
              </div>
            </section>
          );
        })}
        {!articles.length && <p className="lede">Guides are on the way.</p>}
      </main>
      <Disclaimer />
    </>
  );
}

import Link from "next/link";
import { notFound } from "next/navigation";
import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";
import { allArticles, getArticle, renderMarkdown, TOPICS } from "@/lib/library";

export function generateStaticParams() {
  return allArticles().map((a) => ({ slug: a.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const a = getArticle(slug);
  if (!a) return {};
  return { title: a.title, description: a.summary, openGraph: { type: "article", title: a.title, description: a.summary } };
}

export default async function ArticlePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const a = getArticle(slug);
  if (!a) notFound();
  const topic = TOPICS.find((t) => t.id === a.topic);
  const related = a.related.map((s) => getArticle(s)).filter(Boolean) as NonNullable<ReturnType<typeof getArticle>>[];
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org", "@type": "Article", headline: a.title, description: a.summary, author: { "@type": "Organization", name: a.author },
        publisher: { "@type": "Organization", name: "Talk Gooder" },
      }) }} />
      <Header />
      <main className="wrap article">
        <Link className="crumb" href="/library">Library{topic ? ` / ${topic.label}` : ""}</Link>
        <h1>{a.title}</h1>
        <p className="byline">By {a.author} · {a.minutes} min read{a.updated ? ` · Updated ${a.updated}` : ""}</p>
        <div className="prose" dangerouslySetInnerHTML={{ __html: renderMarkdown(a.body) }} />
        <div className="band article-cta">
          <div>
            <h2>Try it in your next speech</h2>
            <p>Time it, flag the lines to punch up, and rehearse from one place.</p>
          </div>
          <div className="cta"><Link className="btn primary lg" href="/signup">Start free</Link></div>
        </div>
        {related.length > 0 && (
          <section className="lib-topic">
            <h2>Keep reading</h2>
            <div className="lib-grid">
              {related.map((r) => (
                <Link key={r.slug} href={`/library/${r.slug}`} className="lib-card">
                  <h3>{r.title}</h3>
                  <p>{r.summary}</p>
                  <span>{r.minutes} min read</span>
                </Link>
              ))}
            </div>
          </section>
        )}
      </main>
      <Disclaimer />
    </>
  );
}

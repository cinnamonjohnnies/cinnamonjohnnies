import Link from "next/link";
import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";
import { PLAN } from "@/lib/env";

export default function Home() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org", "@type": "SoftwareApplication", name: "Talk Gooder", applicationCategory: "BusinessApplication", operatingSystem: "Web",
        description: "Write, time and rehearse speeches.", offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
      }) }} />
      <Header />
      <main className="wrap home">
        <section className="hero">
          <div className="hero-copy">
            <span className="eyebrow">For club speakers and public speakers</span>
            <h1>Write the speech. <em>Own the room.</em></h1>
            <p className="lede">
              Paste in a script and Talk Gooder finds your opening, body and close, times every line as you edit, flags what
              needs punching up, and prints a clean copy to rehearse from.
            </p>
            <div className="cta">
              <Link className="btn primary lg" href="/signup">Start free</Link>
              <Link className="btn lg" href="/help">See how it works</Link>
            </div>
            <p className="fine">No card needed for the free plan. Paid plans start with a {PLAN.trialDays} day free trial.</p>
          </div>

          <div className="mock" aria-hidden="true">
            <div className="mock-bar"><span /><span /><span /></div>
            <div className="mock-head">
              <div className="mock-time">5:42</div>
              <span className="mock-pill">In range</span>
              <span className="mock-target">of 5:00 to 7:00</span>
            </div>
            <div className="mock-track"><i style={{ width: "74%" }} /></div>
            <div className="mock-tabs"><b>Open</b><span>Body</span><span>Close</span><span>Show all</span></div>
            <div className="mock-card">
              <div className="mock-sec"><em>Open</em> <strong>The goat story</strong></div>
              <p><i /> So there I was, holding a very confused goat.</p>
              <p className="flagged"><i /> I had exactly nine minutes to explain compound interest.</p>
              <p className="cue"><i /> Pause, let it land (3s)</p>
              <p><i /> That is how I learned the most expensive word in finance is later.</p>
            </div>
          </div>
        </section>

        <section className="features">
          <div className="feat"><span className="num">1</span><h3>Shape the speech</h3><p>Mark the opening, body and close, drag sections and lines into order, split, merge, and undo anything.</p></div>
          <div className="feat"><span className="num">2</span><h3>Know your time</h3><p>Pauses and stage directions count toward the clock. Set a target length, watch it live, and rehearse with a built-in stopwatch.</p></div>
          <div className="feat"><span className="num">3</span><h3>Punch it up</h3><p>Flag lines for humor, a stat, a story or a tighter cut, get ideas to try, then print a clean copy for the lectern.</p></div>
        </section>

        <section className="band">
          <div>
            <h2>Start with three speeches, free</h2>
            <p>Upgrade for unlimited speeches, PDF export and the punch-up brief. Cancel any time.</p>
          </div>
          <div className="cta">
            <Link className="btn primary lg" href="/signup">Create your free account</Link>
            <Link className="btn lg" href="/pricing">Compare plans</Link>
          </div>
        </section>
      </main>
      <Disclaimer />
    </>
  );
}

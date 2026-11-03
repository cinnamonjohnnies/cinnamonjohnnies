import Link from "next/link";
import { FEEDBACK_URL } from "@/lib/env";

// The site footer. Kept under this name so every page that already includes it gets the new design.
export default function Disclaimer() {
  return (
    <footer className="sitefoot">
      <div className="foot-top">
        <div>
          <div className="foot-brand"><img className="foot-logo" src="/brand/logo-dark.svg" alt="Talk Gooder" width="141" height="50" /></div>
          <p>Write, time and rehearse your speeches.</p>
        </div>
        <nav aria-label="Footer">
          <Link href="/library">Library</Link>
          <Link href="/help">Help</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/terms">Terms</Link>
          <Link href="/privacy">Privacy</Link>
          <a href={FEEDBACK_URL} target="_blank" rel="noopener noreferrer">Feedback</a>
        </nav>
      </div>
      <p className="foot-fine">
        Talk Gooder is an independent product. It is not affiliated with, endorsed by, or sponsored by Toastmasters International.
        Names of programs and trademarks belong to their owners and appear only to describe what the tool can be used for.
      </p>
    </footer>
  );
}

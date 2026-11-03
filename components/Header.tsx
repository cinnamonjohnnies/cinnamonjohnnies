import Link from "next/link";
import MySpeechesLink, { type Recent } from "./MySpeechesLink";
import { FEEDBACK_URL } from "@/lib/env";
import { supabaseServer } from "@/lib/supabase-server";

export default async function Header() {
  let email: string | null = null;
  let recent: Recent[] = [];
  try {
    const sb = await supabaseServer();
    const { data } = await sb.auth.getUser();
    email = data.user?.email ?? null;
    if (data.user) {
      const { data: rows } = await sb.from("speeches").select("id,updated,title:data->>title").eq("user_id", data.user.id).order("updated", { ascending: false }).limit(5);
      recent = (rows || []).map((r: any) => ({ id: String(r.id), title: String(r.title || "") }));
    }
  } catch {
    email = email ?? null;
  }
  const initial = (email || "?").trim().charAt(0).toUpperCase();
  return (
    <header className="top">
      <div className="top-in">
        <Link className="brand" href="/">
          <img src="/brand/logo-dark.svg" alt="Talk Gooder" width="169" height="60" />
        </Link>
        <nav aria-label="Main">
          <Link href="/library">Library</Link>
          <Link href="/help">Help</Link>
          {email ? (
            <>
              <MySpeechesLink recent={recent} />
              <details className="acct">
                <summary aria-label="Account menu"><span className="avatar">{initial}</span></summary>
                <div className="menu">
                  <div className="menu-who">{email}</div>
                  <Link href="/account">Account</Link>
                  <Link href="/pricing">Plans and Pricing</Link>
                  <a href={FEEDBACK_URL} target="_blank" rel="noopener noreferrer">Send Feedback</a>
                  <form action="/auth/signout" method="post"><button type="submit">Sign Out</button></form>
                </div>
              </details>
            </>
          ) : (
            <>
              <Link href="/pricing">Pricing</Link>
              <Link href="/login">Sign In</Link>
              <Link className="btn primary sm" href="/signup">Start Free</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

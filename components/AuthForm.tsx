"use client";
import { useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import PasswordInput from "@/components/PasswordInput";
import { track } from "@vercel/analytics";
import { supabaseBrowser } from "@/lib/supabase-browser";

export default function AuthForm({ mode }: { mode: "login" | "signup" }) {
  const params = useSearchParams();
  const next = params.get("next") || "/app";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<{ t: "err" | "ok"; s: string } | null>(
    params.get("error") ? { t: "err", s: "That link did not work. Open links in the same browser where you asked for them, and use each one once. Request a new one below." } : null
  );

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true); setMsg(null);
    const sb = supabaseBrowser();
    try {
      if (mode === "signup") {
        const { data, error } = await sb.auth.signUp({
          email, password,
          options: { emailRedirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}` },
        });
        if (error) throw error;
        track("signup");
        if (data.session) { window.location.href = next; return; }
        setMsg({ t: "ok", s: "Check your email for a confirmation link, then come back and sign in." });
      } else {
        const { error } = await sb.auth.signInWithPassword({ email, password });
        if (error) throw error;
        window.location.href = next;
      }
    } catch (err: any) {
      setMsg({ t: "err", s: err?.message || "Something went wrong. Try again." });
    } finally { setBusy(false); }
  }

  async function magic() {
    if (!email) { setMsg({ t: "err", s: "Type your email first." }); return; }
    setBusy(true); setMsg(null);
    const { error } = await supabaseBrowser().auth.signInWithOtp({
      email, options: { emailRedirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}` },
    });
    setBusy(false);
    setMsg(error ? { t: "err", s: error.message } : { t: "ok", s: "We sent you a sign-in link. Open it on this device." });
  }

  async function reset() {
    if (!email) { setMsg({ t: "err", s: "Type your email first." }); return; }
    setBusy(true); setMsg(null);
    const { error } = await supabaseBrowser().auth.resetPasswordForEmail(email, { redirectTo: `${window.location.origin}/auth/callback?next=/auth/update-password` });
    setBusy(false);
    setMsg(error ? { t: "err", s: error.message } : { t: "ok", s: "Check your email for a link to set a new password." });
  }

  return (
    <form className="card" onSubmit={submit}>
      <h1 style={{ fontSize: 24 }}>{mode === "signup" ? "Create your account" : "Sign in"}</h1>
      <label>Email<input type="email" required autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} /></label>
      <label>Password<PasswordInput value={password} onChange={setPassword} autoComplete={mode === "signup" ? "new-password" : "current-password"} /></label>
      <div className="row">
        <button className="btn primary" type="submit" disabled={busy}>{mode === "signup" ? "Create account" : "Sign in"}</button>
        {mode === "login" && <button className="btn" type="button" onClick={magic} disabled={busy}>Email me a link</button>}
      </div>
      {msg && <p className={`msg ${msg.t}`} role="status">{msg.s}</p>}
      <p className="msg">
        {mode === "signup" ? <>Already have an account? <Link href="/login">Sign in</Link></> : <>New here? <Link href="/signup">Create an account</Link> · <a href="#" onClick={(e) => { e.preventDefault(); reset(); }}>Forgot your password?</a></>}
      </p>
      {mode === "signup" && <p className="msg">By creating an account you agree to the <Link href="/terms">Terms</Link> and <Link href="/privacy">Privacy Policy</Link>.</p>}
    </form>
  );
}

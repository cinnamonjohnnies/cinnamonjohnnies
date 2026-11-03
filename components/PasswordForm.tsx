"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import PasswordInput from "@/components/PasswordInput";
import { supabaseBrowser } from "@/lib/supabase-browser";

// Lets a signed-in person (including one who arrived from a reset link) choose a new password.
export default function PasswordForm() {
  const [signedIn, setSignedIn] = useState<boolean | null>(null);
  const [pw, setPw] = useState("");
  const [pw2, setPw2] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<{ t: "err" | "ok"; s: string } | null>(null);

  useEffect(() => {
    supabaseBrowser().auth.getUser().then(({ data }) => setSignedIn(!!data.user));
  }, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (pw !== pw2) { setMsg({ t: "err", s: "The two passwords do not match." }); return; }
    setBusy(true); setMsg(null);
    const { error } = await supabaseBrowser().auth.updateUser({ password: pw });
    setBusy(false);
    if (error) { setMsg({ t: "err", s: error.message }); return; }
    setMsg({ t: "ok", s: "Password saved. Taking you to your speeches." });
    setTimeout(() => { window.location.href = "/app"; }, 1200);
  }

  if (signedIn === null) return <div className="card"><p className="msg">One moment.</p></div>;
  if (!signedIn) {
    return (
      <div className="card">
        <h1 style={{ fontSize: 24 }}>That link did not sign you in</h1>
        <p className="msg">Reset links only work in the same browser where you asked for them, and only once. Request a new one from the sign in page.</p>
        <p className="msg"><Link href="/login">Back to sign in</Link></p>
      </div>
    );
  }
  return (
    <form className="card" onSubmit={submit}>
      <h1 style={{ fontSize: 24 }}>Choose a new password</h1>
      <label>New password<PasswordInput value={pw} onChange={setPw} autoComplete="new-password" /></label>
      <label>Type it again<PasswordInput value={pw2} onChange={setPw2} autoComplete="new-password" /></label>
      <div className="row"><button className="btn primary" type="submit" disabled={busy}>Save password</button></div>
      {msg && <p className={`msg ${msg.t}`} role="status">{msg.s}</p>}
    </form>
  );
}

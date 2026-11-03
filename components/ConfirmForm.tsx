"use client";
import { useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { supabaseBrowser } from "@/lib/supabase-browser";

// Email links land here. The person has to press a button, so mail scanners that open links
// ahead of time cannot use up the one time token, and it works in any browser.
const TYPES = ["signup", "recovery", "magiclink", "email", "invite", "email_change"] as const;
type OtpType = (typeof TYPES)[number];

export default function ConfirmForm() {
  const params = useSearchParams();
  const tokenHash = params.get("token_hash") || "";
  const type = (params.get("type") || "") as OtpType;
  const raw = params.get("next") || "/app";
  const next = raw.startsWith("/") && !raw.startsWith("//") ? raw : "/app";
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const valid = !!tokenHash && TYPES.includes(type);

  async function go() {
    setBusy(true); setErr("");
    const { error } = await supabaseBrowser().auth.verifyOtp({ token_hash: tokenHash, type });
    if (error) {
      setBusy(false);
      setErr("This link has expired or was already used. Request a new one from the sign in page.");
      return;
    }
    window.location.href = next;
  }

  const title = type === "recovery" ? "Reset your password" : type === "signup" ? "Confirm your email" : "Sign in";
  const button = type === "recovery" ? "Continue to choose a new password" : type === "signup" ? "Confirm my email" : "Sign me in";

  if (!valid) {
    return (
      <div className="card">
        <h1 style={{ fontSize: 24 }}>This link is not complete</h1>
        <p className="msg">Request a new one from the sign in page.</p>
        <p className="msg"><Link href="/login">Back to sign in</Link></p>
      </div>
    );
  }
  return (
    <div className="card">
      <h1 style={{ fontSize: 24 }}>{title}</h1>
      <p className="msg">Press the button to continue.</p>
      <div className="row"><button className="btn primary" type="button" onClick={go} disabled={busy}>{busy ? "One moment" : button}</button></div>
      {err && <p className="msg err" role="status">{err} <Link href="/login">Back to sign in</Link></p>}
    </div>
  );
}

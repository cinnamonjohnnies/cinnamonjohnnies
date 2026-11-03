"use client";
import { useState } from "react";
import { track } from "@vercel/analytics";

export function CheckoutButton({ plan, label, primary }: { plan: "monthly" | "annual"; label: string; primary?: boolean }) {
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  async function go() {
    setBusy(true); setErr(""); track("checkout_start", { plan });
    const r = await fetch("/api/stripe/checkout", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ plan }) });
    const j = await r.json().catch(() => ({}));
    if (r.status === 401) { window.location.href = "/signup?next=/pricing"; return; }
    if (j.url) { window.location.href = j.url; return; }
    setErr(j.error || "Could not start checkout."); setBusy(false);
  }
  return (<><button className={"btn" + (primary ? " primary" : "")} type="button" onClick={go} disabled={busy}>{busy ? "One moment..." : label}</button>{err && <p className="msg err" role="status">{err}</p>}</>);
}

export function PortalButton() {
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  async function go() {
    setBusy(true); setErr("");
    const r = await fetch("/api/stripe/portal", { method: "POST" });
    const j = await r.json().catch(() => ({}));
    if (j.url) { window.location.href = j.url; return; }
    setErr(j.error || "Could not open billing."); setBusy(false);
  }
  return (<><button className="btn primary" type="button" onClick={go} disabled={busy}>{busy ? "One moment..." : "Manage billing or cancel"}</button>{err && <p className="msg err" role="status">{err}</p>}</>);
}

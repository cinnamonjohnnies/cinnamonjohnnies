"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { supabaseBrowser } from "@/lib/supabase-browser";

type Req = { t: "db"; id: number; op: "get" | "set" | "delete" | "list" | "pitch" | "punch" | "condense"; payload: any };

// Hosts the editor in an iframe and does its saving. The editor never sees your login.
export default function EditorFrame({ userId, email, paid, openId, cmd }: { userId: string; email: string; paid: boolean; openId?: string; cmd?: string }) {
  const frame = useRef<HTMLIFrameElement>(null);
  const [upgrade, setUpgrade] = useState<string | null>(null);

  useEffect(() => {
    const sb = supabaseBrowser();
    const origin = window.location.origin;
    let channel: ReturnType<typeof sb.channel> | null = null;
    const send = (m: any) => frame.current?.contentWindow?.postMessage(m, origin);
    const init = () => { send({ t: "init", paid, email }); if (openId) send({ t: "open", id: openId }); if (cmd) send({ t: "cmd", name: cmd }); };

    async function handle(r: Req) {
      const reply = (result?: any, error?: { code: string; message: string }) => send({ t: "reply", id: r.id, result, error });
      try {
        const aiRoutes: Record<string, { url: string; reason: string }> = {
          pitch: { url: "/api/pitch", reason: "pitch" },
          punch: { url: "/api/punchup", reason: "punchup" },
          condense: { url: "/api/condense", reason: "condense" },
        };
        const ai = aiRoutes[r.op as string];
        if (ai) {
          const res = await fetch(ai.url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(r.payload) });
          const j = await res.json().catch(() => ({}));
          if (res.status === 402) { setUpgrade(ai.reason); return reply(undefined, { code: "paid_required", message: "paid" }); }
          if (!res.ok) return reply(undefined, { code: j?.error || "error", message: j?.error || "error" });
          return reply(j);
        }
        if (r.op === "list") {
          if (r.payload.col !== "speeches") return reply([]);
          const { data, error } = await sb.from("speeches").select("id,data").eq("user_id", userId);
          if (error) throw error;
          return reply((data || []).map((x: any) => ({ id: x.id, data: x.data })));
        }
        const path: string = r.payload.path;
        const [col, ...rest] = path.split("/");
        const id = rest.join("/");
        if (col === "speeches") {
          if (r.op === "get") {
            const { data, error } = await sb.from("speeches").select("data").eq("user_id", userId).eq("id", id).maybeSingle();
            if (error) throw error;
            return reply({ exists: !!data, data: data?.data });
          }
          if (r.op === "set") {
            const d = r.payload.data || {};
            const { error } = await sb.from("speeches").upsert({ user_id: userId, id, data: d, updated: Number(d.updated) || Date.now() });
            if (error) throw error;
            return reply({ ok: true });
          }
          const { error } = await sb.from("speeches").delete().eq("user_id", userId).eq("id", id);
          if (error) throw error;
          return reply({ ok: true });
        }
        // everything else (small flags such as "meta/app") lives in the kv table
        if (r.op === "get") {
          const { data, error } = await sb.from("kv").select("data").eq("user_id", userId).eq("path", path).maybeSingle();
          if (error) throw error;
          return reply({ exists: !!data, data: data?.data });
        }
        if (r.op === "set") {
          const { error } = await sb.from("kv").upsert({ user_id: userId, path, data: r.payload.data || {} });
          if (error) throw error;
          return reply({ ok: true });
        }
        const { error } = await sb.from("kv").delete().eq("user_id", userId).eq("path", path);
        if (error) throw error;
        return reply({ ok: true });
      } catch (e: any) {
        const limit = String(e?.message || "").includes("free_limit_reached");
        if (limit) setUpgrade("limit");
        reply(undefined, { code: limit ? "free_limit" : "error", message: limit ? "Free plan limit reached" : String(e?.message || e) });
      }
    }

    function onMessage(e: MessageEvent) {
      if (e.origin !== origin || e.source !== frame.current?.contentWindow) return;
      const m = e.data || {};
      if (m.t === "ready") init();
      else if (m.t === "db") handle(m as Req);
      else if (m.type === "upgrade") setUpgrade(m.reason || "feature");
      else if (m.t === "subscribe" && m.col === "speeches" && !channel) {
        channel = sb
          .channel("speeches-" + userId)
          .on("postgres_changes", { event: "*", schema: "public", table: "speeches", filter: `user_id=eq.${userId}` }, (p: any) => {
            const type = p.eventType === "DELETE" ? "removed" : p.eventType === "INSERT" ? "added" : "modified";
            const row = p.eventType === "DELETE" ? p.old : p.new;
            send({ t: "change", col: "speeches", type, id: row?.id, data: p.eventType === "DELETE" ? undefined : row?.data });
          })
          .subscribe();
      }
    }
    const goHome = () => send({ t: "home" });
    const openOne = (e: Event) => send({ t: "open", id: (e as CustomEvent).detail });
    window.addEventListener("tg-open", openOne);
    const runCmd = (e: Event) => send({ t: "cmd", name: (e as CustomEvent).detail });
    window.addEventListener("tg-cmd", runCmd);
    window.addEventListener("message", onMessage);
    window.addEventListener("tg-home", goHome);
    return () => { window.removeEventListener("message", onMessage); window.removeEventListener("tg-home", goHome); window.removeEventListener("tg-open", openOne); window.removeEventListener("tg-cmd", runCmd); if (channel) sb.removeChannel(channel); };
  }, [userId, email, paid, openId, cmd]);

  const reasons: Record<string, string> = {
    limit: "You have reached the free plan limit. Upgrade to keep more speeches.",
    pdf: "PDF export is part of the paid plan.",
    brief: "The punch-up brief is part of the paid plan.",
    punchup: "AI punch-up suggestions are part of the paid plan.",
    pitch: "AI pitch writing is part of the paid plan. Your answers were saved into the outline so you can write it yourself.",
    condense: "Condensing lines with AI is part of the paid plan.",
    feature: "That feature is part of the paid plan.",
  };

  return (
    <>
      <div className="frame">
        <iframe ref={frame} src="/editor.html" allow="microphone" title="Talk Gooder editor" onLoad={() => { frame.current?.contentWindow?.postMessage({ t: "init", paid, email }, window.location.origin); if (openId) frame.current?.contentWindow?.postMessage({ t: "open", id: openId }, window.location.origin); if (cmd) frame.current?.contentWindow?.postMessage({ t: "cmd", name: cmd }, window.location.origin); }} />
      </div>
      {upgrade && (
        <div className="banner" role="dialog" aria-label="Upgrade">
          <strong>{reasons[upgrade] || reasons.feature}</strong>
          <span className="row">
            <Link className="btn primary" href="/pricing">See plans</Link>
            <button className="btn" type="button" onClick={() => setUpgrade(null)}>Not now</button>
          </span>
        </div>
      )}
    </>
  );
}

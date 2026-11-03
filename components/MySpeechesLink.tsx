"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef } from "react";

export type Recent = { id: string; title: string };

// "My speeches" menu: the list page, plus the speeches you worked on most recently.
export default function MySpeechesLink({ recent = [] }: { recent?: Recent[] }) {
  const path = usePathname();
  const box = useRef<HTMLDetailsElement>(null);

  useEffect(() => {
    const close = (e: MouseEvent) => { if (box.current?.open && !box.current.contains(e.target as Node)) box.current.open = false; };
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, []);

  const done = () => { if (box.current) box.current.open = false; };
  const onApp = path === "/app";
  const cmdItem = (name: string, label: string) => (
    <Link
      href={`/app?cmd=${name}`}
      onClick={(e) => { done(); if (onApp) { e.preventDefault(); window.dispatchEvent(new CustomEvent("tg-cmd", { detail: name })); } }}
    >
      {label}
    </Link>
  );

  return (
    <details className="acct recent" ref={box}>
      <summary className="recent-btn">My Speeches <span aria-hidden="true">▾</span></summary>
      <div className="menu">
        <Link
          href="/app"
          onClick={(e) => { done(); if (onApp) { e.preventDefault(); window.dispatchEvent(new Event("tg-home")); } }}
        >
          All Speeches
        </Link>
        {cmdItem("new", "Start New")}
        {cmdItem("import", "Upload Speech")}
        {cmdItem("sample", "Load Sample Speech")}
        {cmdItem("backup", "Back Up and Restore")}
        {recent.length > 0 && <div className="menu-who">Recently Worked On</div>}
        {recent.map((r) => (
          <Link
            key={r.id}
            href={`/app?open=${encodeURIComponent(r.id)}`}
            onClick={(e) => { done(); if (onApp) { e.preventDefault(); window.dispatchEvent(new CustomEvent("tg-open", { detail: r.id })); } }}
          >
            {r.title || "Untitled speech"}
          </Link>
        ))}
      </div>
    </details>
  );
}

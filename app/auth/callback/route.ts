import { NextResponse } from "next/server";
import { supabaseServer } from "@/lib/supabase-server";

// Email confirmation and magic links land here, trade the code for a session, then continue.
export async function GET(req: Request) {
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const raw = url.searchParams.get("next") || "/app";
  const next = raw.startsWith("/") && !raw.startsWith("//") ? raw : "/app";
  if (code) {
    const sb = await supabaseServer();
    const { error } = await sb.auth.exchangeCodeForSession(code);
    if (error) return NextResponse.redirect(new URL("/login?error=link", url.origin));
  }
  return NextResponse.redirect(new URL(next, url.origin));
}

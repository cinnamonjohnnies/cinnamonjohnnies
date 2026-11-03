import { NextResponse } from "next/server";
import { supabaseServer, supabaseAdmin } from "@/lib/supabase-server";
import { stripe } from "@/lib/stripe";
import { SITE_URL } from "@/lib/env";

// Opens Stripe's hosted page where people change card, switch plans, or cancel.
export async function POST() {
  const sb = await supabaseServer();
  const { data } = await sb.auth.getUser();
  if (!data.user) return NextResponse.json({ error: "Please sign in first." }, { status: 401 });
  const { data: row } = await supabaseAdmin().from("subscriptions").select("stripe_customer_id").eq("user_id", data.user.id).maybeSingle();
  if (!row?.stripe_customer_id) return NextResponse.json({ error: "No billing account yet." }, { status: 400 });
  const session = await stripe().billingPortal.sessions.create({ customer: row.stripe_customer_id, return_url: `${SITE_URL}/account` });
  return NextResponse.json({ url: session.url });
}

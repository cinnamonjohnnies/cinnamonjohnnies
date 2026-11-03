import { NextResponse } from "next/server";
import { supabaseServer, supabaseAdmin } from "@/lib/supabase-server";
import { stripe, priceFor } from "@/lib/stripe";
import { SITE_URL, PLAN } from "@/lib/env";

// Starts a Stripe Checkout session for the signed-in person and returns its address.
export async function POST(req: Request) {
  const sb = await supabaseServer();
  const { data } = await sb.auth.getUser();
  const user = data.user;
  if (!user) return NextResponse.json({ error: "Please sign in first." }, { status: 401 });

  const { plan } = await req.json().catch(() => ({ plan: "" }));
  const price = priceFor(plan);
  if (!price) return NextResponse.json({ error: "That plan is not set up yet." }, { status: 400 });

  const admin = supabaseAdmin();
  const { data: row } = await admin.from("subscriptions").select("stripe_customer_id,stripe_subscription_id,status").eq("user_id", user.id).maybeSingle();
  if (row && ["active", "trialing"].includes(row.status)) {
    return NextResponse.json({ error: "You already have an active plan. Use Manage billing on the Account page." }, { status: 409 });
  }

  let customer = row?.stripe_customer_id as string | undefined;
  if (!customer) {
    const c = await stripe().customers.create({ email: user.email || undefined, metadata: { supabase_user_id: user.id } });
    customer = c.id;
    await admin.from("subscriptions").upsert({ user_id: user.id, stripe_customer_id: customer, status: row?.status || "none", updated_at: new Date().toISOString() });
  }

  const session = await stripe().checkout.sessions.create({
    mode: "subscription",
    customer,
    client_reference_id: user.id,
    line_items: [{ price, quantity: 1 }],
    allow_promotion_codes: true,
    // 30-day free trial, first subscription only. Card is collected up front; cancel any time before day 30 to pay nothing.
    subscription_data: {
      metadata: { supabase_user_id: user.id },
      ...(row?.stripe_subscription_id ? {} : { trial_period_days: PLAN.trialDays }),
    },
    payment_method_collection: "always",
    success_url: `${SITE_URL}/account?checkout=success`,
    cancel_url: `${SITE_URL}/pricing?checkout=canceled`,
  });
  return NextResponse.json({ url: session.url });
}

import { NextResponse } from "next/server";
import type Stripe from "stripe";
import { stripe, planFor } from "@/lib/stripe";
import { supabaseAdmin } from "@/lib/supabase-server";
import { need } from "@/lib/env";

export const runtime = "nodejs";

// Stripe calls this whenever a subscription starts, renews, changes or ends.
// It is the only thing that writes to the subscriptions table.
async function record(sub: Stripe.Subscription, fallbackUserId?: string | null) {
  const admin = supabaseAdmin();
  const customer = typeof sub.customer === "string" ? sub.customer : sub.customer.id;
  const item = sub.items.data[0];
  const priceId = item?.price?.id ?? null;
  // The period end moved onto the item in newer Stripe API versions; read whichever is present.
  const end = (sub as any).current_period_end ?? (item as any)?.current_period_end ?? null;

  let userId = (sub.metadata && sub.metadata.supabase_user_id) || fallbackUserId || null;
  if (!userId) {
    const { data } = await admin.from("subscriptions").select("user_id").eq("stripe_customer_id", customer).maybeSingle();
    userId = data?.user_id ?? null;
  }
  if (!userId) {
    const c = await stripe().customers.retrieve(customer);
    if (!("deleted" in c) && c.metadata?.supabase_user_id) userId = c.metadata.supabase_user_id;
  }
  if (!userId) throw new Error("No user found for customer " + customer);

  const { error } = await admin.from("subscriptions").upsert({
    user_id: userId,
    stripe_customer_id: customer,
    stripe_subscription_id: sub.id,
    status: sub.status,
    price_id: priceId,
    plan: planFor(priceId),
    current_period_end: end ? new Date(end * 1000).toISOString() : null,
    cancel_at_period_end: !!sub.cancel_at_period_end,
    updated_at: new Date().toISOString(),
  });
  if (error) throw error;
}

export async function POST(req: Request) {
  const sig = req.headers.get("stripe-signature");
  const body = await req.text();
  let event: Stripe.Event;
  try {
    event = stripe().webhooks.constructEvent(body, sig || "", need("STRIPE_WEBHOOK_SECRET"));
  } catch (err: any) {
    return NextResponse.json({ error: "Bad signature" }, { status: 400 });
  }
  try {
    switch (event.type) {
      case "checkout.session.completed": {
        const s = event.data.object as Stripe.Checkout.Session;
        if (s.mode === "subscription" && s.subscription) {
          const id = typeof s.subscription === "string" ? s.subscription : s.subscription.id;
          await record(await stripe().subscriptions.retrieve(id), s.client_reference_id);
        }
        break;
      }
      case "customer.subscription.created":
      case "customer.subscription.updated":
      case "customer.subscription.deleted":
        await record(event.data.object as Stripe.Subscription);
        break;
      default:
        break;
    }
  } catch (err: any) {
    // 500 makes Stripe retry later, which is what we want for a temporary database problem.
    console.error("webhook failed", event.type, err?.message);
    return NextResponse.json({ error: "handler failed" }, { status: 500 });
  }
  return NextResponse.json({ received: true });
}

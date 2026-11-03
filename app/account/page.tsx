import Link from "next/link";
import Header from "@/components/Header";
import { PortalButton, CheckoutButton } from "@/components/PlanButtons";
import { getUserAndSub, isPaid } from "@/lib/subscription";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

export const metadata = { robots: { index: false, follow: false } };

export default async function Account({ searchParams }: { searchParams: Promise<{ checkout?: string }> }) {
  const { user, sub } = await getUserAndSub();
  if (!user) redirect("/login?next=/account");
  const q = await searchParams;
  const paid = isPaid(sub);
  const end = sub?.current_period_end ? new Date(sub.current_period_end).toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" }) : null;
  return (
    <>
      <Header />
      <main className="wrap narrow">
        <h1>Account</h1>
        <div className="card">
          <p><strong>Email</strong><br />{user.email}</p>
          <p><strong>Plan</strong><br />{paid ? `Paid (${sub?.plan === "annual" ? "annual" : sub?.plan === "monthly" ? "monthly" : "active"})` : "Free"}
            {paid && end && <><br /><span className="msg">{sub?.cancel_at_period_end ? `Ends on ${end}. You will not be charged again.` : `Renews on ${end}.`}</span></>}
          </p>
          {q.checkout === "success" && !paid && <p className="msg ok" role="status">Thanks. Your payment is confirming. Refresh this page in a moment.</p>}
          {paid ? <PortalButton /> : <div className="row"><CheckoutButton plan="monthly" label="Upgrade, monthly" primary /><CheckoutButton plan="annual" label="Upgrade, annual" /></div>}
          <p className="msg"><Link href="/auth/update-password">Change password</Link></p>
          <p className="msg"><Link href="/app">Back to my speeches</Link></p>
        </div>
      </main>
    </>
  );
}

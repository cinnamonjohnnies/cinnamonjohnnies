import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";
import { CheckoutButton } from "@/components/PlanButtons";
import { PLAN } from "@/lib/env";

export const metadata = { title: "Pricing", description: "Start free with three speeches. Upgrade for unlimited speeches, PDF export and the punch-up brief, with a 30 day free trial." };

export default function Pricing() {
  return (
    <>
      <Header />
      <main className="wrap">
        <h1>Pricing</h1>
        <p className="lede">Start free. Upgrade when you want unlimited speeches and the print and punch-up tools. Paid plans start with a {PLAN.trialDays} day free trial, and you can cancel before it ends to pay nothing.</p>
        <div className="grid">
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Free</h2>
            <div className="price">$0</div>
            <ul className="tick">
              <li>Up to {PLAN.freeSpeechLimit} speeches</li>
              <li>Paste or upload, mark sections, move lines, undo</li>
              <li>Live timing, pauses and stage directions, rehearsal stopwatch</li>
              <li>Punch-up flags</li>
            </ul>
          </div>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Monthly</h2>
            <div className="price">{PLAN.monthlyLabel.split(" ")[0]}<small> per month</small></div>
            <ul className="tick"><li>Unlimited speeches</li><li>PDF export for printing</li><li>Punch-up brief</li><li>Cancel any time</li></ul>
            <CheckoutButton plan="monthly" label={`Start ${PLAN.trialDays} day free trial`} primary />
          </div>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>Annual</h2>
            <div className="price">{PLAN.annualLabel.split(" ")[0]}<small> per year</small></div>
            <ul className="tick"><li>Everything in Monthly</li><li>{PLAN.annualNote}</li></ul>
            <CheckoutButton plan="annual" label={`Start ${PLAN.trialDays} day free trial`} primary />
          </div>
        </div>
      </main>
      <Disclaimer />
    </>
  );
}

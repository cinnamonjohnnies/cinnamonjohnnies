import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";

export const metadata = { title: "Terms of Service", description: "The terms for using Talk Gooder." };

export default function Terms() {
  return (
    <>
      <Header />
      <main className="wrap">
        <h1>Terms of Service</h1>
        <p className="lede">Draft for review. Have a lawyer read and adapt this before you take payments.</p>
        <h2>The service</h2>
        <p>Talk Gooder is a tool for writing, timing and rehearsing speeches. You own the speeches you write. We store them so you can use them on your devices.</p>
        <h2>Accounts</h2>
        <p>Keep your sign-in details private. You are responsible for activity on your account.</p>
        <h2>Paid plans</h2>
        <p>Paid plans renew automatically each month or year until canceled. You can cancel at any time from the Account page, and the plan continues until the end of the period you paid for. Refunds are at our discretion unless the law requires otherwise.</p>
        <h2>Acceptable use</h2>
        <p>Do not use the service to break the law, harass people, or attempt to access other people's data.</p>
        <h2>No affiliation</h2>
        <p>Talk Gooder is independent and is not affiliated with, endorsed by, or sponsored by Toastmasters International or any other club organization.</p>
        <h2>Changes and contact</h2>
        <p>We may update these terms and will post the new version here. Contact: add your support email here.</p>
      </main>
      <Disclaimer />
    </>
  );
}

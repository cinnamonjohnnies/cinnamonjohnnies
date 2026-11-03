import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";

export const metadata = { title: "Privacy Policy", description: "How Talk Gooder handles your information." };

export default function Privacy() {
  return (
    <>
      <Header />
      <main className="wrap">
        <h1>Privacy Policy</h1>
        <p className="lede">Draft for review. Have a lawyer read and adapt this before launch.</p>
        <h2>What we store</h2>
        <p>Your email address, and the speeches and settings you save. Billing is handled by Stripe; we receive your plan status and a customer reference, not your card number.</p>
        <h2>Who can see your speeches</h2>
        <p>Only you, through your signed-in account. Our database enforces this per account. We do not read your speeches or use them to train models.</p>
        <h2>Service providers</h2>
        <p>Supabase (accounts and database), Stripe (payments), Resend (account emails), and Vercel (hosting) process data on our behalf. When you use an AI feature such as the pitch builder or rewrite suggestions, the text you submit is sent to Anthropic to generate the result. We do not use your speeches to train models.</p>
        <h2>Dictation</h2>
        <p>The Dictate button uses your browser's built-in speech recognition. Depending on your browser, the audio is processed by its maker (Google for Chrome and Edge, Apple for Safari). Talk Gooder does not record or store your audio, only the text you choose to keep.</p>
        <h2>Site analytics</h2>
        <p>We use Vercel Web Analytics to count visits and see which pages are used. It does not use cookies and does not follow you across other sites.</p>
        <h2>Your choices</h2>
        <p>You can delete speeches at any time. To delete your account and data, contact us at the address on the Terms page.</p>
      </main>
      <Disclaimer />
    </>
  );
}

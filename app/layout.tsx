import "./globals.css";
import type { Metadata, Viewport } from "next";
import { Analytics } from "@vercel/analytics/next";
import { SITE_URL } from "@/lib/env";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: "Talk Gooder: Speech Writing, Timing and Rehearsal", template: "%s | Talk Gooder" },
  description: "Write, time and rehearse speeches. Paste a script, mark the opening, body and close, punch it up, and print it. Built for club speakers and anyone who speaks in public.",
  alternates: { canonical: "./" },
  openGraph: { type: "website", siteName: "Talk Gooder", title: "Talk Gooder: Speech Writing, Timing and Rehearsal", description: "Write, time and rehearse speeches. Built for club speakers and anyone who speaks in public.", url: "/" },
  twitter: { card: "summary_large_image", title: "Talk Gooder", description: "Write, time and rehearse speeches." },
};
export const viewport: Viewport = { width: "device-width", initialScale: 1, viewportFit: "cover" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" />
      </head>
      <body>{children}<Analytics /></body>
    </html>
  );
}

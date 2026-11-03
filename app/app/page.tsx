import Header from "@/components/Header";
import EditorFrame from "@/components/EditorFrame";
import { getUserAndSub, isPaid } from "@/lib/subscription";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

export const metadata = { robots: { index: false, follow: false } };

export default async function AppPage({ searchParams }: { searchParams: Promise<{ open?: string; cmd?: string }> }) {
  const { open, cmd } = await searchParams;
  const { user, sub } = await getUserAndSub();
  if (!user) redirect("/login?next=/app");
  return (
    <div className="shell">
      <Header />
      <EditorFrame userId={user.id} email={user.email || ""} paid={isPaid(sub)} openId={open} cmd={cmd} />
    </div>
  );
}

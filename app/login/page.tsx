import { Suspense } from "react";
import Header from "@/components/Header";
import AuthForm from "@/components/AuthForm";

export const metadata = { robots: { index: false, follow: false } };

export default function Login() {
  return (<><Header /><main className="wrap narrow"><Suspense><AuthForm mode="login" /></Suspense></main></>);
}

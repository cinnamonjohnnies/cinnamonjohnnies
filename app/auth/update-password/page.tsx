import { Suspense } from "react";
import Header from "@/components/Header";
import PasswordForm from "@/components/PasswordForm";

export default function UpdatePassword() {
  return (<><Header /><main className="wrap narrow"><Suspense><PasswordForm /></Suspense></main></>);
}

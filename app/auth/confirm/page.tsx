import { Suspense } from "react";
import Header from "@/components/Header";
import ConfirmForm from "@/components/ConfirmForm";

export default function Confirm() {
  return (<><Header /><main className="wrap narrow"><Suspense><ConfirmForm /></Suspense></main></>);
}

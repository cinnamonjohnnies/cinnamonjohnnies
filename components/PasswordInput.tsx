"use client";
import { useState } from "react";

// A password box with a Show / Hide button, so a typo can be spotted before it causes a failed sign in.
export default function PasswordInput(props: { value: string; onChange: (v: string) => void; autoComplete: string; minLength?: number; required?: boolean }) {
  const [show, setShow] = useState(false);
  return (
    <span className="pw">
      <input type={show ? "text" : "password"} required={props.required ?? true} minLength={props.minLength ?? 8} autoComplete={props.autoComplete}
        autoCapitalize="none" autoCorrect="off" spellCheck={false} value={props.value} onChange={(e) => props.onChange(e.target.value)} />
      <button type="button" className="pw-toggle" aria-pressed={show} onClick={() => setShow(!show)}>{show ? "Hide" : "Show"}</button>
    </span>
  );
}

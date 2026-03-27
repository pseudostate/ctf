"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [id, setId] = useState("");
  const [pw, setPw] = useState("");
  const [msg, setMsg] = useState<string>("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setMsg("");
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ id, pw }),
      });
      const data = await res.json();
      if (!res.ok) {
        setMsg(data.error || "login failed");
        return;
      }
      router.push("/seats");
      router.refresh();
    } catch {
      setMsg("network error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container narrow">
      <section className="card panel">
        <h1 className="title">Login</h1>
        <br />
        <form className="stack" onSubmit={onSubmit}>
          <label className="field">
            <span>ID</span>
            <input value={id} onChange={(e) => setId(e.target.value)} placeholder="id" />
          </label>
          <label className="field">
            <span>Password</span>
            <input type="password" value={pw} onChange={(e) => setPw(e.target.value)} placeholder="password" />
          </label>
          <button className="btn" disabled={loading}>{loading ? "Signing in..." : "Sign in"}</button>
        </form>
        {msg ? <pre className="statusBox">{msg}</pre> : null}
      </section>
    </main>
  );
}

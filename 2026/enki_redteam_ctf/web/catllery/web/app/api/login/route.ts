import { NextResponse } from "next/server";
import { internalJson } from "@/lib/internal";

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}));
  const { res, data } = await internalJson("/internal/login", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });

  const out = NextResponse.json(data, { status: res.status });
  if (res.ok && data && typeof data === "object" && "ticket_no" in data && typeof (data as any).ticket_no === "string") {
    out.cookies.set("ticket_no", (data as any).ticket_no, { httpOnly: true, sameSite: "lax", path: "/" });
  }
  return out;
}

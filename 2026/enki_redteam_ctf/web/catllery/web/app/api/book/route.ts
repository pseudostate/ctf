import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { internalJson } from "@/lib/internal";

export async function POST(req: Request) {
  const ticketNo = (await cookies()).get("ticket_no")?.value;
  if (!ticketNo) return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });

  const body = (await req.json().catch(() => ({}))) as { seat?: string };
  if (!body.seat) {
    return NextResponse.json({ ok: false, error: "missing_params" }, { status: 400 });
  }

  const qs = new URLSearchParams({ seat: body.seat, ticket_no: ticketNo });

  const { res, data } = await internalJson(`/internal/book?${qs.toString()}`);
  return NextResponse.json(data, { status: res.status });
}

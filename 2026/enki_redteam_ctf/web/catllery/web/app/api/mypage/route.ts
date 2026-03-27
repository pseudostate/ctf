import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { internalJson } from "@/lib/internal";

export async function GET() {
  const ticketNo = (await cookies()).get("ticket_no")?.value;
  if (!ticketNo) return NextResponse.json({ ok: false, error: "unauthorized" }, { status: 401 });

  const qs = `ticket_no=${encodeURIComponent(ticketNo)}`;
  const [{ res: checkRes, data: checkData }, { res: seatsRes, data: seatsData }] = await Promise.all([
    internalJson(`/internal/check-reservation?${qs}`),
    internalJson(`/internal/all-seats?${qs}`),
  ]);
  if (!seatsRes.ok) return NextResponse.json(seatsData, { status: seatsRes.status });
  if (!checkRes.ok && checkRes.status !== 404) return NextResponse.json(checkData, { status: checkRes.status });

  const reservationsRaw =
    checkRes.ok && Array.isArray((checkData as any).reservations) ? (checkData as any).reservations : [];
  const allSeats = Array.isArray((seatsData as any).all_seats) ? (seatsData as any).all_seats : [];
  const reservations = reservationsRaw.map((s: any) => ({
    seat: s.seat ?? "",
    holder_name: s.holder_name ?? "",
    holder_ticket_no: s.holder_ticket_no ?? "",
    ttl: typeof s.ttl === "number" ? s.ttl : 0,
  }));

  return NextResponse.json(
    {
      ok: true,
      user: { ticket_no: ticketNo },
      all_seats: allSeats,
      reservations,
    },
    { status: 200 },
  );
}

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const INTERNAL_API_BASE = process.env.INTERNAL_API_BASE || "http://127.0.0.1:5000";

export async function middleware(req: NextRequest) {
  const ticketNo = req.cookies.get("ticket_no")?.value;
  if (!ticketNo) {
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("next", req.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  try {
    const res = await fetch(
      `${INTERNAL_API_BASE}/internal/all-seats?ticket_no=${encodeURIComponent(ticketNo)}`,
      { cache: "no-store" },
    );
    if (res.ok) return NextResponse.next();
  } catch {}

  const out = NextResponse.redirect(new URL("/login", req.url));
  out.cookies.delete("ticket_no");
  return out;
}

export const config = {
  matcher: ["/seats", "/mypage"],
};

"use client";

import { useEffect, useMemo, useState } from "react";

type Seat = {
  seat: string;
  status: "FREE" | "HELD";
  ttl: number;
  holder_name?: string;
  holder_ticket_no?: string;
};

type MypageResp = {
  ok: boolean;
  user?: { ticket_no: string };
  all_seats?: Seat[];
};

const VIP_SEAT = "VIP";

const FRONT_LEFT_ROWS = [
  ["1", "2", VIP_SEAT, "4"],
  ["9", "10", "11", "12"],
  ["17", "18", "19", "20"],
];

const FRONT_RIGHT_ROWS = [
  ["5", "6", "7", "8"],
  ["13", "14", "15", "16"],
  ["21", "22", "23", "24"],
];

const CENTER_ROWS = [
  ["31", "32", "33", "34", "35", "36", "37", "38", "39", "40"],
  ["41", "42", "43", "44", "45", "46", "47", "48"],
  ["49", "50", "51", "52", "53", "54", "55"],
  ["56", "57", "58", "59", "60", "61", "62"],
  ["63", "64", "25", "26", "27", "28", "29"],
];

const SIDE_LEFT = ["65", "66", "67", "68"];
const SIDE_RIGHT = ["69", "70", "71", "72"];

export default function SeatsPage() {
  const [seats, setSeats] = useState<Seat[]>([]);
  const [me, setMe] = useState<MypageResp["user"] | null>(null);
  const [selectedSeat, setSelectedSeat] = useState("25");
  const [status, setStatus] = useState("");

  async function refresh() {
    const res = await fetch("/api/mypage", { cache: "no-store" });
    const data = (await res.json()) as MypageResp;
    if (!res.ok) {
      setSeats([]);
      setMe(null);
      setStatus(typeof data === "object" ? JSON.stringify(data) : "failed");
      return;
    }
    setSeats(Array.isArray(data.all_seats) ? data.all_seats : []);
    setMe(data.user ?? null);
  }

  useEffect(() => {
    refresh().catch(() => setStatus("failed to load"));
    const timer = setInterval(() => {
      refresh().catch(() => {});
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const seatMap = useMemo(() => new Map(seats.map((s) => [s.seat, s])), [seats]);
  const selectedBackend = seatMap.get(selectedSeat);
  const activeHolds = seats.filter((s) => s.status === "HELD");
  const myReservations = me ? activeHolds.filter((s) => s.holder_ticket_no === me.ticket_no) : [];
  const myActiveSeat = myReservations[0]?.seat ?? null;
  const blockedByMyHold = Boolean(myActiveSeat && myActiveSeat !== selectedSeat);
  const meText = me ? `ticket_no=${me.ticket_no}` : "Not logged in";

  async function reserveSelected() {
    if (selectedSeat === VIP_SEAT) return;
    if (blockedByMyHold) return;
    if (!seatMap.has(selectedSeat)) return;

    setStatus(`booking ${selectedSeat}...`);
    const res = await fetch("/api/book", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ seat: selectedSeat }),
    });
    const data = await res.json();
    if (res.ok) setStatus(`Reserved ${selectedSeat} (${data.ttl}s)`);
    else setStatus(data.error || "booking failed");
    await refresh();
  }

  function renderSeat(label: string) {
    const backend = seatMap.get(label);
    const isVip = label === VIP_SEAT;
    const isHeld = backend?.status === "HELD";
    const isMine = Boolean(isHeld && me && backend?.holder_ticket_no === me.ticket_no);
    const isReserved = isVip || isHeld;
    const isSelected = selectedSeat === label;

    let className = "venueSeat";
    if (isReserved) className += " venueSeatReserved";
    if (isMine) className += " venueSeatMine";
    if (isVip) className += " venueSeatVipLocked";
    if (isSelected) className += " venueSeatSelected";

    let sub = isHeld ? `${backend?.ttl ?? 0}s` : "OPEN";
    if (isVip) sub = isHeld ? `RES ${backend?.ttl ?? 0}s` : "RESERVED";

    return (
      <button
        key={label}
        type="button"
        className={className}
        onClick={() => setSelectedSeat(label)}
        title={isVip ? "VIP reserved" : isReserved ? "Reserved" : "Available"}
      >
        <span className="venueSeatCode">{label}</span>
        <span className="venueSeatSub">{sub}</span>
      </button>
    );
  }

  return (
    <main className="container">
      <section className="card panel">
        <div className="header" style={{ marginBottom: 10 }}>
          <div>
            <h1 className="title">좌석 배치도</h1>
            <br />
          </div>
          <div className="badge">LIVE</div>
        </div>

        <pre className="statusBox">{meText}</pre>

        <div className="concertLayout">
          <div className="card concertMapCard">
            <div className="concertStage">STAGE</div>

            <div className="concertFloor">
              <div className="floorBlock">
                {FRONT_LEFT_ROWS.map((row, i) => (
                  <div className="floorRow" key={`l-${i}`}>
                    {row.map(renderSeat)}
                  </div>
                ))}
              </div>
              <div className="floorGap" />
              <div className="floorBlock">
                {FRONT_RIGHT_ROWS.map((row, i) => (
                  <div className="floorRow" key={`r-${i}`}>
                    {row.map(renderSeat)}
                  </div>
                ))}
              </div>
            </div>

            <div className="bowlWrap">
              <div className="wingCol leftWing">{SIDE_LEFT.map(renderSeat)}</div>
              <div className="bowlRows">
                {CENTER_ROWS.map((row, idx) => (
                  <div className={`bowlRow row-${idx}`} key={`b-${idx}`}>
                    {row.map(renderSeat)}
                  </div>
                ))}
              </div>
              <div className="wingCol rightWing">{SIDE_RIGHT.map(renderSeat)}</div>
            </div>
          </div>

          <div className="bookingSideStack">
            <aside className="card bookingSummary">
              <h2 className="panelTitle">예매 정보</h2>

              <div className="summarySection">
                <div className="summaryLabel">선택 좌석</div>
                <div className="summaryValue">{selectedSeat}</div>
                <div className="summarySub">
                  {selectedSeat === VIP_SEAT
                    ? "VIP / 예약됨"
                    : blockedByMyHold
                      ? `${myActiveSeat} 좌석 점유 중 (만료 후 재예약 가능)`
                    : !seatMap.has(selectedSeat)
                      ? "예약 불가"
                      : selectedBackend?.status === "HELD"
                        ? `예약됨 (${selectedBackend.ttl}s)`
                        : "예약 가능"}
                </div>
              </div>

              <button
                className="btn reserveAction"
                disabled={
                  !seatMap.has(selectedSeat) ||
                  selectedSeat === VIP_SEAT ||
                  blockedByMyHold ||
                  selectedBackend?.status === "HELD"
                }
                onClick={reserveSelected}
              >
                {blockedByMyHold
                  ? `${myActiveSeat} 좌석 점유 중`
                  : !seatMap.has(selectedSeat)
                  ? "예약 불가"
                  : selectedSeat === VIP_SEAT
                    ? "VIP 예약 불가"
                    : selectedBackend?.status === "HELD"
                      ? "이미 예약됨"
                      : `${selectedSeat} 좌석 예약`}
              </button>
            </aside>

            <aside className="card bookingSummary">
              <h2 className="panelTitle">내 예약 현황</h2>
              <div className="summarySection">
                {myReservations.length === 0 ? (
                  <div className="summarySub">현재 예약 없음</div>
                ) : (
                  myReservations.map((s) => (
                    <div className="summaryRow" key={`mine-${s.seat}`}>
                      <span>{s.seat}</span>
                      <span>{s.ttl}s</span>
                    </div>
                  ))
                )}
              </div>
            </aside>
          </div>
        </div>

        {status ? <pre className="statusBox">{status}</pre> : null}
      </section>
    </main>
  );
}

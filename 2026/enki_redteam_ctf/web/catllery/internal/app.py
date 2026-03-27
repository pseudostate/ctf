import os
import re
import secrets
import time
from functools import wraps
from pathlib import Path

import bcrypt

from flask import Flask, jsonify, request, send_file
import redis
from models import User

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"
REAL_FLAG_IMAGE = IMG_DIR / "real_flag.png"
FAKE_FLAG_IMAGE = IMG_DIR / "fake_flag.png"
FLAG_RE = re.compile(r"FLAG\{[^}]*\}")

VIP_ID = "FLAG{I_Th1nk_Th1s_15_N0t_R34l_F14G...XD}"
HOLD_TTL = 7
VIP_TICKET_NO = os.environ.get("VIP_TICKET_NO", "")

SEATS = tuple([str(n) for n in range(1, 73) if n != 3] + ["VIP"])

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

users_by_ticket: dict[str, User] = {}
users_by_login: dict[str, str] = {}

book_sha: str | None = None
lookup_sha: str | None = None

LUA_DIR = BASE_DIR / "lua"
BOOK_LUA = (LUA_DIR / "book.lua").read_text(encoding="utf-8")
LOOKUP_LUA = (LUA_DIR / "lookup.lua").read_text(encoding="utf-8")


def err(msg: str, code: int = 400):
    return jsonify({"ok": False, "error": msg}), code


def mask_flag_holder_name(holder_name: str) -> str:
    if not FLAG_RE.search(holder_name):
        return holder_name
    return FLAG_RE.sub(f"FLAG{{{secrets.token_hex(32)}}}", holder_name)


def new_ticket_no() -> str:
    while True:
        ticket_no = str(secrets.randbelow(900_000_000_000) + 100_000_000_000)
        if ticket_no != VIP_TICKET_NO and ticket_no not in users_by_ticket:
            return ticket_no


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ticket_no = request.args.get("ticket_no", "")
        user = users_by_ticket.get(ticket_no)
        if not user:
            return err("unauthorized", 401)
        return fn(user, *args, **kwargs)

    return wrapper


def reservation_by_ticket_no(seat: str, ticket_no: str) -> dict[str, str | int] | None:
    try:
        row = r.evalsha(lookup_sha, 1, f"seathold:{seat}", ticket_no, seat)
    except redis.exceptions.NoScriptError:
        return None
    if not isinstance(row, list) or len(row) != 4:
        return None
    return {
        "seat": str(row[0]),
        "holder_ticket_no": str(row[1]),
        "holder_name": str(row[2]),
        "ttl": int(row[3]),
    }


def reservations_for_ticket_no(ticket_no: str) -> list[dict[str, str | int]]:
    return [row for seat in SEATS if (row := reservation_by_ticket_no(seat, ticket_no))]


def init() -> None:
    global book_sha, lookup_sha, VIP_TICKET_NO
    for _ in range(10):
        try:
            r.ping()
            break
        except redis.RedisError:
            time.sleep(0.2)
    else:
        raise RuntimeError("redis not ready")

    if not VIP_TICKET_NO.isdigit():
        raise RuntimeError("VIP_TICKET_NO must be set to a decimal string")

    r.flushdb()
    vip_user = User(
        ticket_no=VIP_TICKET_NO,
        id="vip-curator",
        pw_hash=bcrypt.hashpw(b"disabled", bcrypt.gensalt()).decode(),
    )
    users_by_ticket[VIP_TICKET_NO] = vip_user
    users_by_login[vip_user.id] = vip_user.ticket_no

    r.hset(f"seathold:VIP", mapping={"holder_ticket_no": VIP_TICKET_NO, "holder_name": VIP_ID})
    r.expire(f"seathold:VIP", 365 * 24 * 60 * 60)
    book_sha = r.script_load(BOOK_LUA)
    lookup_sha = r.script_load(LOOKUP_LUA)


@app.post("/internal/signup")
def signup():
    data = request.get_json() or {}
    login_id = str(data.get("id", "")).strip()
    login_pw = str(data.get("pw", ""))

    if not login_id or not login_pw:
        return err("missing_credentials", 400)
    if login_id in users_by_login:
        return err("duplicate_login_id", 409)

    ticket_no = new_ticket_no()
    user = User(
        ticket_no=ticket_no,
        id=login_id,
        pw_hash=bcrypt.hashpw(login_pw.encode(), bcrypt.gensalt()).decode(),
    )

    users_by_ticket[ticket_no] = user
    users_by_login[login_id] = ticket_no

    return jsonify({"ok": True, "ticket_no": ticket_no, "user": user.public()})


@app.post("/internal/login")
def login():
    data = request.get_json() or {}
    login_id = str(data.get("id", "")).strip()
    login_pw = str(data.get("pw", ""))

    ticket_no = users_by_login.get(login_id)
    user = users_by_ticket.get(ticket_no) if ticket_no else None

    if not user or not bcrypt.checkpw(login_pw.encode(), user.pw_hash.encode()):
        return err("invalid_credentials", 401)

    return jsonify({"ok": True, "ticket_no": user.ticket_no, "user": user.public()})


@app.get("/internal/all-seats")
@login_required
def all_seats(_user: User):
    rows = []
    for seat in SEATS:
        hold_key = f"seathold:{seat}"
        ttl = r.ttl(hold_key)
        if ttl > 0:
            hold = r.hgetall(hold_key)
            row = {
                "seat": seat,
                "status": "HELD",
                "ttl": ttl,
                "holder_ticket_no": hold.get("holder_ticket_no", ""),
                "holder_name": hold.get("holder_name", ""),
            }
        else:
            row = {
                "seat": seat,
                "status": "FREE",
                "ttl": 0,
                "holder_ticket_no": "",
                "holder_name": "",
            }
        row["holder_name"] = mask_flag_holder_name(str(row["holder_name"]))
        rows.append(row)
    return jsonify({"ok": True, "all_seats": rows})


@app.get("/internal/book")
@login_required
def book(user: User):
    seat = request.args.get("seat", "")
    if seat not in SEATS:
        return err("seat_not_found", 404)
    if seat == "VIP":
        return err("vip_locked", 403)

    hold_key = f"seathold:{seat}"
    ticket_hold_key = f"tickethold:{user.ticket_no}"

    try:
        out = r.evalsha(
            book_sha,
            2,
            hold_key,
            ticket_hold_key,
            seat,
            user.ticket_no,
            user.id,
            str(HOLD_TTL),
        )
    except redis.exceptions.NoScriptError:
        return err("booking_script_missing", 500)

    if out != "ok":
        return err(out, 409 if out == "already_holding_seat" else 403)

    hold = r.hgetall(hold_key)
    return jsonify({"ok": True, "seat": seat, "ttl": r.ttl(hold_key), "holder_ticket_no": hold.get("holder_ticket_no", "")})

@app.get("/internal/check-reservation")
def check_reservation():
    ticket_no = request.args.get("ticket_no", "")
    reservations = reservations_for_ticket_no(ticket_no)

    if not reservations:
        return err("not_found", 200)
    return jsonify({"ok": True, "ticket_no": ticket_no, "reservations": reservations})


@app.get("/internal/get-image")
def get_image():
    ticket_no = request.args.get("ticket_no", "")
    if ticket_no == VIP_TICKET_NO:
        return err("forbidden", 403)

    reservations = reservations_for_ticket_no(ticket_no) if ticket_no else []

    is_vip = any(str(row.get("seat")) == "VIP" for row in reservations)

    path = REAL_FLAG_IMAGE if is_vip else FAKE_FLAG_IMAGE

    if not path.exists():
        return err("missing_image_asset", 500)

    return send_file(path, mimetype="image/png", max_age=0)

init()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

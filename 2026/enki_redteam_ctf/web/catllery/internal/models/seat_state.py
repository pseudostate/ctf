from dataclasses import dataclass


@dataclass(slots=True)
class SeatState:
    seat: str
    status: str
    ttl: int
    holder_ticket_no: str
    holder_name: str

    def to_dict(self) -> dict[str, str | int]:
        return {
            "seat": self.seat,
            "status": self.status,
            "ttl": self.ttl,
            "holder_ticket_no": self.holder_ticket_no,
            "holder_name": self.holder_name,
        }

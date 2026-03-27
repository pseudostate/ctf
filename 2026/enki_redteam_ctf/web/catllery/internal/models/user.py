from dataclasses import dataclass


@dataclass(slots=True)
class User:
    ticket_no: str
    id: str
    pw_hash: str

    def public(self) -> dict[str, str]:
        return {"ticket_no": self.ticket_no, "id": self.id}

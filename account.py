# account.py
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Account:
    account_number: int
    name: str
    age: int
    balance: float
    account_type: str  # "Savings" or "Current"
    status: str = "Active"  # "Active" or "Inactive"
    pin: Optional[int] = None

    def to_dict(self):
        # used for CSV persistence
        return {
            "account_number": str(self.account_number),
            "name": self.name,
            "age": str(self.age),
            "balance": f"{self.balance:.2f}",
            "type": self.account_type,
            "status": self.status,
            "pin": str(self.pin) if self.pin is not None else ""
        }

    @staticmethod
    def from_dict(d):
        return Account(
            account_number=int(d["account_number"]),
            name=d["name"],
            age=int(d["age"]),
            balance=float(d["balance"]),
            account_type=d.get("type", "Savings"),
            status=d.get("status", "Active"),
            pin=int(d["pin"]) if d.get("pin") not in (None, "", "None") else None
        )

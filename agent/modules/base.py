"""
Базовий клас для всіх модулів перевірки.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class CheckResult:
    """Результат однієї перевірки для відправки в моніторинг."""
    module: str
    status: str  # "ok" | "error" | "warning"
    message: str
    details: dict[str, Any] | None = None
    timestamp: str | None = None

    def to_payload(self) -> dict[str, Any]:
        ts = self.timestamp or datetime.utcnow().isoformat() + "Z"
        out = {
            "type": "check",
            "module": self.module,
            "status": self.status,
            "message": self.message,
            "timestamp": ts,
        }
        if self.details:
            out["details"] = self.details
        return out


class BaseModule:
    """Базовий модуль: один метод run (async) повертає CheckResult."""

    name: str = "base"

    async def run(self) -> CheckResult:
        raise NotImplementedError

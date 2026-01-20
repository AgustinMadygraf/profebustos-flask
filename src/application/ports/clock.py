"""
Path: src/application/ports/clock.py
"""

from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    "Provides current time for application use cases."
    def now(self) -> datetime:
        "Return the current datetime."
        raise NotImplementedError

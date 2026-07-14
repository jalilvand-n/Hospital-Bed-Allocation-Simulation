from dataclasses import dataclass, field
from typing import Optional

from enums import EventType
from patient import Patient


@dataclass(order=True)
class Event:

    time: float
    event_type: EventType = field(compare=False)
    priority: int = field(default=0)
    patient: Optional[Patient] = field(default=None, compare=False)

    def __repr__(self):

        return (
            f"{self.event_type.name}"
            f"(time={self.time:.2f})"
        )
from dataclasses import dataclass
from typing import Optional

from patient import Patient


@dataclass
class Bed:
    bed_id: int

    patient: Optional[Patient] = None

    occupied_since: Optional[float] = None

    @property
    def is_available(self):
        return self.patient is None

    def assign(self, patient: Patient, current_time: float):
        self.patient = patient
        self.occupied_since = current_time
        return self

    def release(self):
        self.patient = None
        self.occupied_since = None
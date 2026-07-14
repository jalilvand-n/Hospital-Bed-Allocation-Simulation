from dataclasses import dataclass
from typing import Optional

from enums import PatientStatus, PriorityLevel, RejectionReason

@dataclass
class Patient:

    # --------------------------
    # Basic Information
    # --------------------------

    patient_id: int
    arrival_time: float

    age_group: str
    age_priority: int

    disease: str
    subtype: str

    # --------------------------
    # Vital Signs
    # --------------------------

    blood_pressure: float = 0.0
    pulse: float = 0.0
    temperature: float = 0.0

    # --------------------------
    # Triage
    # --------------------------

    severity_score: float = 0.0   
    priority_score: float = 0.0
    priority_level: Optional[PriorityLevel] = None
    triage_duration: float = 0.0
    triage_finish_time: float = 0.0
    safe_wait_time: float = 0.0

    # --------------------------
    # Hospital Stay
    # --------------------------

    status: PatientStatus = PatientStatus.ARRIVED
    bed_number: Optional[int] = None
    queue_entry_time: Optional[float] = None
    queue_exit_time: Optional[float] = None
    admission_time: Optional[float] = None
    treatment_duration: float = 0.0
    discharge_time: Optional[float] = None
    rejection_time: Optional[float] = None
    rejection_reason: Optional[RejectionReason] = None

    # --------------------------
    # Calculated Outputs
    # --------------------------

    wait_to_bed: Optional[float] = None

    total_time_in_system: Optional[float] = None

    def calculate_output_metrics(self):
        if (
            self.admission_time is not None
            and self.queue_entry_time is not None
        ):
            self.wait_to_bed = (
                self.admission_time -
                self.queue_entry_time
            )
        else:
            self.wait_to_bed = 0.0

        if self.discharge_time is not None:
            self.total_time_in_system = (
                self.discharge_time -
                self.arrival_time
                )
        
    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "arrival_time": self.arrival_time,
            "age_group": self.age_group,
            "disease": self.disease,
            "subtype": self.subtype,
            "severity_score": self.severity_score,
            "priority_score": self.priority_score,
            "priority_level": (
                self.priority_level.name
                if self.priority_level
                else None
            ),
            "status": self.status.name,
            "bed_number": self.bed_number,
            "queue_entry_time": self.queue_entry_time,
            "admission_time": self.admission_time,
            "discharge_time": self.discharge_time,
            "wait_to_bed": self.wait_to_bed,
            "total_time_in_system": self.total_time_in_system,
            "rejection_time": self.rejection_time,
            "rejection_reason": (
                self.rejection_reason.name
                if self.rejection_reason
                else None
            )
        }

    @property
    def is_admitted(self):
        return self.status in (PatientStatus.UNDER_TREATMENT, PatientStatus.DISCHARGED, PatientStatus.CENSORED)
    @property
    def is_rejected(self):
        return self.status == PatientStatus.REJECTED
from enum import Enum, auto

class PatientStatus(Enum):
    ARRIVED = auto()
    UNDER_TRIAGE = auto()
    WAITING = auto()
    UNDER_TREATMENT = auto()
    DISCHARGED = auto()
    REJECTED = auto()
    CENSORED = auto()

class EventType(Enum):
    PATIENT_ARRIVAL = auto()
    TRIAGE_COMPLETE = auto()
    TREATMENT_COMPLETE = auto()
    QUEUE_TIMEOUT = auto()
    HOURLY_MONITOR = auto()

class PriorityLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class RejectionReason(Enum):
    QUEUE_FULL = auto()
    CAPACITY = auto()
    TIMEOUT = auto()
    LOW_PRIORITY = auto()
    NON_URGENT = auto()
    RESOURCE_CONSTRAINTS = auto()
    TRANSFER_RECOMMENDED = auto()
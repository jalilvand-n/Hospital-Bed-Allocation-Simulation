from collections import deque
from typing import Optional

from config import BED_CAPACITY, QUEUE_CAPACITY
from bed import Bed
from enums import PatientStatus
from patient import Patient


class Hospital:

    def __init__(self):

        # Create beds
        self.beds = [
            Bed(bed_id=i + 1)
            for i in range(BED_CAPACITY)
        ]

        # Waiting queue (FIFO)
        self.queue = deque()

    # ==================================================
    # Properties
    # ==================================================

    @property
    def occupied_beds(self):
        return sum(
            1
            for bed in self.beds
            if not bed.is_available
        )

    @property
    def available_beds(self):
        return BED_CAPACITY - self.occupied_beds

    @property
    def queue_length(self):
        return len(self.queue)

    @property
    def queue_full(self):
        return self.queue_length >= QUEUE_CAPACITY

    @property
    def bed_utilization(self):
        return self.occupied_beds / BED_CAPACITY

    @property
    def system_pressure(self):
        return self.occupied_beds + self.queue_length

    @property
    def over_capacity_pressure(self):
        return self.system_pressure > BED_CAPACITY

    # ==================================================
    # Bed Management
    # ==================================================

    def find_available_bed(self) -> Optional[Bed]:
        for bed in self.beds:
            if bed.is_available:
                return bed
        return None

    def assign_bed(self, patient: Patient, current_time: float) -> bool:
        bed = self.find_available_bed()
        if bed is None:
            return False
        bed.assign(patient, current_time)
        patient.bed_number = bed.bed_id
        patient.admission_time = current_time
        if patient.queue_entry_time is not None:
            patient.queue_exit_time = current_time
        return True

    def release_bed(self, bed_number: int):
        for bed in self.beds:
            if bed.bed_id == bed_number:
                bed.release()
                return True
        return False

    # ==================================================
    # Queue Management
    # ==================================================

    def enqueue_patient(self, patient: Patient, current_time: float) -> bool:
        if self.queue_full:
            return False
        patient.status = PatientStatus.WAITING
        patient.queue_entry_time = current_time
        self.queue.append(patient)
        return True

    def dequeue_patient(self):
        if self.queue:
            patient = self.queue.popleft()
            return patient
        return None

    def peek_queue(self):
        if self.queue:
            return self.queue[0]
        return None

    def remove_from_queue(self, patient: Patient):
        if patient in self.queue:
            self.queue.remove(patient)
            return True
        return False
    
    def has_available_bed(self):
        return self.available_beds > 0    
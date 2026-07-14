import random

from config import *
from hospital import Hospital
from event_queue import EventQueue
from patient import Patient
from event import Event
from enums import *

class Simulation:

    def __init__(self, seed=DEFAULT_SEED):

        self.clock = 0.0
        self.rng = random.Random(seed)
        self.seed = seed
        self.hospital = Hospital()
        self.event_queue = EventQueue()
        self.patients = []
        self.hourly_records = []
        self.patient_counter = 0

    def next_patient_id(self):
        self.patient_counter += 1
        return self.patient_counter
    
    def schedule_event(self, event):
        self.event_queue.add_event(event)

    def initialize(self):

        self.schedule_event(
            Event(
                time=0,
                priority=3,
                event_type=EventType.PATIENT_ARRIVAL
            )
        )

        self.schedule_event(
            Event(
                time=0,
                priority=4,
                event_type=EventType.HOURLY_MONITOR
            )
        )

    def run(self):

        self.initialize()

        handlers = {
            EventType.PATIENT_ARRIVAL:
                self.handle_arrival,
            EventType.TRIAGE_COMPLETE:
                self.handle_triage_complete,
            EventType.TREATMENT_COMPLETE:
                self.handle_treatment_complete,
            EventType.QUEUE_TIMEOUT:
                self.handle_queue_timeout,
            EventType.HOURLY_MONITOR:
                self.handle_hourly_monitor
        }

        while not self.event_queue.is_empty():
            event = self.event_queue.get_next_event()
            self.clock = event.time
            handlers[event.event_type](event)

        return self.patients
        
    def generate_age_group(self):
        age_groups = list(AGE_GROUPS.keys())
        probabilities = [
            AGE_GROUPS[group]["probability"]
            for group in age_groups
        ]
        selected = self.rng.choices(
            age_groups,
            weights=probabilities,
            k=1
        )[0]
        return (
            selected,
            AGE_GROUPS[selected]["priority"]
        )

    def generate_disease(self):
        disease = self.rng.choice(
            list(DISEASES.keys())
        )
        subtype = self.rng.choice(
            DISEASES[disease]["subtypes"]
        )
        return disease, subtype
    
    def generate_vital_signs(self):
        blood_pressure = self.rng.gauss(
            BLOOD_PRESSURE_MEAN,
            BLOOD_PRESSURE_STD
        )
        blood_pressure = max(70, min(200, blood_pressure))
        pulse = self.rng.gauss(
            PULSE_MEAN,
            PULSE_STD
        )
        pulse = max(40, min(180, pulse))
        temperature = self.rng.gauss(
            TEMPERATURE_MEAN,
            TEMPERATURE_STD
        )
        temperature = max(35, min(41.5, temperature))
        return (
            blood_pressure,
            pulse,
            temperature
        )
    
    def generate_triage_time(self):
        return self.rng.uniform(
            TRIAGE_TIME_MIN,
            TRIAGE_TIME_MAX
        )
    
    def generate_interarrival_time(self):
        return self.rng.uniform(
            INTERARRIVAL_MIN,
            INTERARRIVAL_MAX
        )
    
    def calculate_severity(self, patient):
        score = DISEASES[patient.disease]["base_severity"]
        subtypes = DISEASES[patient.disease]["subtypes"]
        subtype_index = subtypes.index(patient.subtype)
        score += subtype_index
        if patient.blood_pressure < 90 or patient.blood_pressure > 140:
            score += 1
        if patient.pulse < 60 or patient.pulse > 100:
            score += 1
        if patient.temperature >= 38:
            score += 1
        if patient.age_priority >= 4:
            score += 1
        return score
    
    def calculate_priority_score(self, patient):
        return (
            PRIORITY_WEIGHTS["severity"] *
            patient.severity_score
            +
            PRIORITY_WEIGHTS["age"] *
            patient.age_priority
        )

    def handle_arrival(self, event):
        patient_id = self.next_patient_id()
        age_group, age_priority = self.generate_age_group()
        disease, subtype = self.generate_disease()
        bp, pulse, temp = self.generate_vital_signs()
        triage_time = self.generate_triage_time()
        patient = Patient(
            patient_id=patient_id,
            arrival_time=self.clock,
            age_group=age_group,
            age_priority=age_priority,
            disease=disease,
            subtype=subtype,
            blood_pressure=bp,
            pulse=pulse,
            temperature=temp,
            triage_duration=triage_time
        )
        patient.status = PatientStatus.UNDER_TRIAGE
        self.patients.append(patient)
        patient.triage_finish_time = (
            self.clock +
            triage_time
        )
        self.schedule_event(
            Event(
                time=patient.triage_finish_time,
                priority=2,
                event_type=EventType.TRIAGE_COMPLETE,
                patient=patient
            )
        )
        next_arrival = (
            self.clock +
            self.generate_interarrival_time()
        )
        if next_arrival <= SIMULATION_HOURS:
            self.schedule_event(
                Event(
                    time=next_arrival,
                    priority=3,
                    event_type=EventType.PATIENT_ARRIVAL
                )
            )

    def determine_priority_level(self, score):

        if score >= PRIORITY_THRESHOLDS["HIGH"]:
            return PriorityLevel.HIGH

        elif score >= PRIORITY_THRESHOLDS["MEDIUM"]:
            return PriorityLevel.MEDIUM

        return PriorityLevel.LOW

    def calculate_safe_wait_time(self, patient):
        if patient.priority_level == PriorityLevel.HIGH:
            return SAFE_WAIT_TIME["HIGH"]
        elif patient.priority_level == PriorityLevel.MEDIUM:
            return SAFE_WAIT_TIME["MEDIUM"]
        return SAFE_WAIT_TIME["LOW"]
    
    def generate_treatment_duration(
        self,
        patient
    ):
        low, high = DISEASES[
            patient.disease
        ]["treatment"]
        duration = self.rng.uniform(
            low,
            high
        )
        duration += max(
            0,
            patient.severity_score - 3
        ) * 0.5
        duration = max(duration, low)
        return duration
    
    def handle_triage_complete(self, event):
        patient = event.patient
        patient.severity_score = (
            self.calculate_severity(patient)
        )
        patient.priority_score = (
            self.calculate_priority_score(patient)
        )
        patient.priority_level = (
            self.determine_priority_level(
                patient.priority_score
            )
        )
        patient.safe_wait_time = (
            self.calculate_safe_wait_time(patient)
        )
        if self.hospital.has_available_bed():
            self.hospital.assign_bed(
                patient,
                self.clock
            )
            patient.status = PatientStatus.UNDER_TREATMENT
            patient.treatment_duration = (
                self.generate_treatment_duration(
                    patient
                )
            )
            self.schedule_event(
                Event(
                    time=(
                        self.clock +
                        patient.treatment_duration
                    ),
                    priority=0,
                    event_type=EventType.TREATMENT_COMPLETE,
                    patient=patient
                )
            )
        else:
            success = self.hospital.enqueue_patient(
                patient,
                self.clock
            )
            if success:
                self.schedule_event(
                    Event(
                        time=(
                            self.clock +
                            patient.safe_wait_time
                        ),
                        priority=1,
                        event_type=EventType.QUEUE_TIMEOUT,
                        patient=patient
                    )
                )
            else:
                patient.status = PatientStatus.REJECTED
                patient.rejection_time = self.clock
                patient.rejection_reason = (
                    RejectionReason.QUEUE_FULL
                )

    def handle_treatment_complete(self, event):
        patient = event.patient
        patient.status = PatientStatus.DISCHARGED
        patient.discharge_time = self.clock
        patient.calculate_output_metrics()
        self.hospital.release_bed(
            patient.bed_number
        )
        if self.hospital.queue_length == 0:
            return
        next_patient = self.hospital.dequeue_patient()
        self.hospital.assign_bed(
            next_patient,
            self.clock
        )
        next_patient.status = PatientStatus.UNDER_TREATMENT
        next_patient.treatment_duration = (
            self.generate_treatment_duration(
                next_patient
            )
        )
        self.schedule_event(
            Event(
                time=(
                    self.clock +
                    next_patient.treatment_duration
                ),
                priority=0,
                event_type=EventType.TREATMENT_COMPLETE,
                patient=next_patient
            )
        )

    def handle_queue_timeout(self, event):
        patient = event.patient
        if patient.status != PatientStatus.WAITING:
            return
        removed = self.hospital.remove_from_queue(patient)
        if not removed:
            return
        patient.status = PatientStatus.REJECTED
        patient.rejection_time = self.clock
        patient.rejection_reason = (
            RejectionReason.TIMEOUT
        )

    def handle_hourly_monitor(self, event):
        record = {
            "time": self.clock,
            "beds_used":
                self.hospital.occupied_beds,
            "available_beds":
                self.hospital.available_beds,
            "queue_length":
                self.hospital.queue_length,
            "queue_full":
                self.hospital.queue_full,
            "bed_utilization":
                self.hospital.bed_utilization,
            "system_pressure":
                self.hospital.system_pressure,
            "over_capacity_pressure":
                self.hospital.over_capacity_pressure
        }
        self.hourly_records.append(
            record
        )
        next_hour = self.clock + 1
        if next_hour <= SIMULATION_HOURS:
            self.schedule_event(
                Event(
                    time=next_hour,
                    priority=4,
                    event_type=EventType.HOURLY_MONITOR
                )
            )
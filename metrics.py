"""
metrics.py

Performance metrics for Hospital Bed Allocation Simulation
"""

from collections import defaultdict
from statistics import mean

from enums import PatientStatus, PriorityLevel


class Metrics:

    def __init__(self, simulation):

        self.sim = simulation

    # =====================================================
    # Admission Rate
    # =====================================================

    def admission_rate(self):

        total = len(self.sim.patients)

        admitted = sum(

            p.status in (
                PatientStatus.UNDER_TREATMENT,
                PatientStatus.DISCHARGED,
                PatientStatus.CENSORED
            )

            for p in self.sim.patients

        )

        return admitted / total if total else 0

    # =====================================================
    # Rejection Rate
    # =====================================================

    def rejection_rate(self):

        total = len(self.sim.patients)

        rejected = sum(

            p.status == PatientStatus.REJECTED

            for p in self.sim.patients

        )

        return rejected / total if total else 0

    # =====================================================
    # Average Waiting Time
    # =====================================================

    def average_waiting_time(self):

        waits = [

            p.wait_to_bed

            for p in self.sim.patients

            if (
                p.wait_to_bed is not None
                and
                p.status != PatientStatus.REJECTED
            )

        ]

        return mean(waits) if waits else 0

    # =====================================================
    # Average Bed Utilization
    # =====================================================

    def average_bed_utilization(self):

        values = [

            row["bed_utilization"]

            for row in self.sim.hourly_records

        ]

        return mean(values) if values else 0

    # =====================================================
    # Peak Queue Length
    # =====================================================

    def peak_queue_length(self):

        values = [

            row["queue_length"]

            for row in self.sim.hourly_records

        ]

        return max(values) if values else 0

    # =====================================================
    # Percent Time Queue Full
    # =====================================================

    def percent_queue_full(self):

        if not self.sim.hourly_records:

            return 0

        full = sum(

            row["queue_full"]

            for row in self.sim.hourly_records

        )

        return full / len(self.sim.hourly_records)

    # =====================================================
    # Percent Time Under Pressure
    # =====================================================

    def percent_under_pressure(self):

        if not self.sim.hourly_records:

            return 0

        pressure = sum(

            row["over_capacity_pressure"]

            for row in self.sim.hourly_records

        )

        return pressure / len(self.sim.hourly_records)

    # =====================================================
    # Average Length Of Stay
    # =====================================================

    def average_length_of_stay(self):

        los = [

            p.total_time_in_system

            for p in self.sim.patients

            if (
                p.total_time_in_system is not None
                and
                p.status == PatientStatus.DISCHARGED
            )

        ]

        return mean(los) if los else 0

    # =====================================================
    # Rejection Rate By Priority
    # =====================================================

    def rejection_rate_by_priority(self):

        total = defaultdict(int)

        rejected = defaultdict(int)

        for patient in self.sim.patients:

            if patient.priority_level is None:
                continue

            key = patient.priority_level.name

            total[key] += 1

            if patient.status == PatientStatus.REJECTED:

                rejected[key] += 1

        rates = {}
        for key in total:
            rates[key] = (
                round(rejected[key] / total[key], 3)
                if total[key] > 0
                else 0
            )
        return rates

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        return {

            "admission_rate":
                self.admission_rate(),

            "rejection_rate":
                self.rejection_rate(),

            "average_waiting_time":
                self.average_waiting_time(),

            "average_bed_utilization":
                self.average_bed_utilization(),

            "peak_queue_length":
                self.peak_queue_length(),

            "percent_queue_full":
                self.percent_queue_full(),

            "percent_under_pressure":
                self.percent_under_pressure(),

            "average_length_of_stay":
                self.average_length_of_stay(),

            "rejection_rate_by_priority":
                self.rejection_rate_by_priority()

        }
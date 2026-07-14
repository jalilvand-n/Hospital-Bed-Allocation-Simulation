"""
verification.py

Verification checks for Hospital Bed Allocation Simulation

Implements the required verification checks listed in
Appendix B of the project description.
"""

from config import BED_CAPACITY, QUEUE_CAPACITY
from enums import PatientStatus


class Verification:

    def __init__(self, simulation):
        self.sim = simulation

    # ==========================================================
    # Check 1
    # Bed capacity never exceeded
    # ==========================================================

    def check_bed_capacity(self):
        return (
            all(
                row["beds_used"] <= BED_CAPACITY
                for row in self.sim.hourly_records
            )
        )

    # ==========================================================
    # Check 2
    # Queue capacity never exceeded
    # ==========================================================

    def check_queue_capacity(self):
        return all(
            row["queue_length"] <= QUEUE_CAPACITY
            for row in self.sim.hourly_records
        )

    # ==========================================================
    # Check 3
    # Admitted / Treated patients contain required information
    # ==========================================================

    def check_admitted_patients(self):

        for patient in self.sim.patients:

            if patient.status in (
                PatientStatus.UNDER_TREATMENT,
                PatientStatus.DISCHARGED,
                PatientStatus.CENSORED
            ):

                if patient.bed_number is None:
                    return False

                if patient.admission_time is None:
                    return False

                if (
                    patient.status != PatientStatus.CENSORED
                    and
                    patient.discharge_time is None
                ):
                    return False

        return True

    # ==========================================================
    # Check 4
    # Every rejected patient has rejection information
    # ==========================================================

    def check_rejected_patients(self):

        for patient in self.sim.patients:

            if patient.status == PatientStatus.REJECTED:

                if patient.rejection_reason is None:
                    return False

                if patient.rejection_time is None:
                    return False

        return True

    # ==========================================================
    # Check 5
    # Every bed has at most one patient
    # ==========================================================

    def check_bed_consistency(self):

        occupied = 0

        for bed in self.sim.hospital.beds:

            if bed.patient is not None:
                occupied += 1

        return occupied <= BED_CAPACITY

    # ==========================================================
    # Check 6
    # Seed exists
    # ==========================================================

    def check_seed(self):

        return hasattr(self.sim, "seed")

    # ==========================================================
    # Run all verification checks
    # ==========================================================

    def check_all(self):

        results = {

            "bed_capacity":
                self.check_bed_capacity(),

            "queue_capacity":
                self.check_queue_capacity(),

            "admitted_patients":
                self.check_admitted_patients(),

            "rejected_patients":
                self.check_rejected_patients(),

            "bed_consistency":
                self.check_bed_consistency(),

            "seed":
                self.check_seed()

        }

        return results

    # ==========================================================
    # Print verification report
    # ==========================================================

    def print_report(self):

        results = self.check_all()

        print("\nVerification Report")
        print("-" * 40)

        for name, passed in results.items():

            status = "PASS" if passed else "FAIL"

            print(f"{name:25} : {status}")

        print("-" * 40)

        if all(results.values()):
            print("All verification checks passed.")
        else:
            print("Some verification checks failed.")
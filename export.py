"""
export.py

Export simulation outputs to CSV files.
"""

from pathlib import Path
import pandas as pd
from metrics import Metrics

class Export:

    def __init__(self, simulation, output_dir="outputs"):

        self.sim = simulation

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            exist_ok=True
        )

    # =====================================================
    # Patient-Level Table
    # =====================================================

    def export_patient_table(self):

        rows = []

        for patient in self.sim.patients:

            rows.append({

                "patient_id":
                    patient.patient_id,

                "arrival_time":
                    patient.arrival_time,

                "age_group":
                    patient.age_group,

                "disease":
                    patient.disease,

                "subtype":
                    patient.subtype,

                "severity_score":
                    patient.severity_score,

                "priority_score":
                    patient.priority_score,

                "priority_level":
                    (
                        patient.priority_level.name
                        if patient.priority_level
                        else None
                    ),

                "status":
                    patient.status.name,

                "bed_number":
                    patient.bed_number,

                "queue_entry_time":
                    patient.queue_entry_time,

                "admission_time":
                    patient.admission_time,

                "discharge_time":
                    patient.discharge_time,

                "wait_to_bed":
                    patient.wait_to_bed,

                "total_time_in_system":
                    patient.total_time_in_system,

                "rejection_time":
                    patient.rejection_time,

                "rejection_reason":
                    (
                        patient.rejection_reason.name
                        if patient.rejection_reason
                        else None
                    )

            })

        df = pd.DataFrame(rows)

        df.to_csv(
            self.output_dir / "patients.csv",
            index=False
        )

        return df

    # =====================================================
    # Hourly Monitoring Table
    # =====================================================

    def export_hourly_table(self):

        df = pd.DataFrame(
            self.sim.hourly_records
        )

        df.to_csv(

            self.output_dir / "hourly_monitoring.csv",

            index=False

        )

        return df

    # =====================================================
    # Replication Summary (Future use)
    # =====================================================

    def export_summary(self):
        metrics = Metrics(self.sim)
        summary = metrics.summary()
        df = pd.DataFrame([summary])
        df.to_csv(
            self.output_dir / "summary.csv",
            index=False
        )

        return df

    # =====================================================
    # Export Everything
    # =====================================================

    def export_all(self):

        self.export_patient_table()

        self.export_hourly_table()

        self.export_summary()

        print(
            f"\nOutput files saved to: {self.output_dir}"
        )
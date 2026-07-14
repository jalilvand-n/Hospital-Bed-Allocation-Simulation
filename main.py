"""
main.py

Hospital Bed Allocation Simulation
Project Entry Point
"""

from config import DEFAULT_SEED
from simulation import Simulation
from verification import Verification
from export import Export
from metrics import Metrics

def main():

    print("=" * 60)
    print("Hospital Bed Allocation Simulation")
    print("=" * 60)

    # -----------------------------------
    # Run Simulation
    # -----------------------------------

    sim = Simulation(seed=DEFAULT_SEED)
    sim.run()

    metrics = Metrics(sim)
    results = metrics.summary()

    # -----------------------------------
    # Verification
    # -----------------------------------

    verifier = Verification(sim)

    verifier.print_report()

    # -----------------------------------
    # Export Outputs
    # -----------------------------------

    exporter = Export(sim)

    exporter.export_all()

    # -----------------------------------
    # Quick Summary
    # -----------------------------------

    total_patients = len(sim.patients)

    admitted = sum(
        p.status.name in (
            "UNDER_TREATMENT",
            "DISCHARGED"
        )
        for p in sim.patients
    )

    rejected = sum(
        p.status.name == "REJECTED"
        for p in sim.patients
    )

    print("\nSimulation Summary")
    print("-" * 40)

    print(f"Patients Generated : {total_patients}")
    print(f"Admitted           : {admitted}")
    print(f"Rejected           : {rejected}")

    if total_patients > 0:

        print(
            f"Admission Rate     : {admitted / total_patients:.2%}"
        )

        print(
            f"Rejection Rate     : {rejected / total_patients:.2%}"
        )

    print("-" * 40)

    print("\nPerformance Metrics")
    print("-" * 40)

    for key, value in results.items():

        if isinstance(value, dict):
            print(f"{key:30} : {value}")

        elif isinstance(value, float):
            print(f"{key:30} : {value:.3f}")

        else:
            print(f"{key:30} : {value}")
        
    print("\nSimulation completed successfully.")


if __name__ == "__main__":
    main()
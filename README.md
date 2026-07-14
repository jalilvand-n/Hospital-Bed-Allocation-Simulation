# Hospital Bed Allocation Simulation

## Project Overview

This project implements a discrete-event simulation (DES) of a hospital bed allocation system. Patients arrive randomly, undergo triage, request hospital beds, wait in a queue if necessary, receive treatment, and are eventually discharged or rejected.

The simulation was developed as part of a Hospital Simulation course project and follows the project specifications provided by the instructor.

---

## Features

- Discrete-event simulation
- Random patient arrivals
- Disease and age generation
- Vital sign generation
- Severity and priority calculation
- FIFO waiting queue
- Bed allocation
- Disease-dependent treatment durations
- Queue timeout mechanism
- Hourly monitoring
- Performance metrics
- Verification checks
- CSV export

---

## Project Structure

## Project Structure

```text
Simulation/
│
├── main.py
├── simulation.py
├── hospital.py
├── patient.py
├── bed.py
├── event.py
├── event_queue.py
├── enums.py
├── config.py
├── metrics.py
├── verification.py
├── export.py
├── requirements.txt
├── README.md
│
└── outputs/
    ├── patients.csv
    ├── hourly_monitoring.csv
    └── summary.csv
```

---

## Requirements

- Python 3.11+
- pandas

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Outputs

Running the simulation generates the following CSV files:

- `patients.csv` — patient-level simulation results
- `hourly_monitoring.csv` — hourly hospital state
- `summary.csv` — overall performance metrics

---

## Verification

The model verifies

- Bed capacity
- Queue capacity
- Patient consistency
- Rejection information
- Random seed availability

---

## Simulation Assumptions

- 10 inpatient beds
- Queue capacity = 5
- Uniform interarrival time (1–3 hours)
- Simulation horizon = 30 days
- Arrivals stop after 30 days
- Existing patients continue until discharge

---

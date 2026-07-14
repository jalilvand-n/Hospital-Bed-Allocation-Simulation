"""
config.py
Global configuration for Hospital Bed Allocation Simulation
"""

# =============================
# Simulation Settings
# =============================

SIMULATION_DAYS = 30
HOURS_PER_DAY = 24
SIMULATION_HOURS = SIMULATION_DAYS * HOURS_PER_DAY

# =============================
# Hospital Settings
# =============================

BED_CAPACITY = 10
QUEUE_CAPACITY = 5

# =============================
# Arrival Process
# =============================

INTERARRIVAL_MIN = 1.0
INTERARRIVAL_MAX = 3.0

# =============================
# Random Seed
# =============================

DEFAULT_SEED = 42


AGE_GROUPS = {
    "0-18": {
        "probability": 0.15,
        "priority": 3
    },
    "19-35": {
        "probability": 0.25,
        "priority": 2
    },
    "36-55": {
        "probability": 0.35,
        "priority": 1
    },
    "56-75": {
        "probability": 0.15,
        "priority": 4
    },
    "76+": {
        "probability": 0.10,
        "priority": 5
    }
}

DISEASES = {
"Broken Arm":{
"base_severity":2,
"treatment":(12,24),
"subtypes":["Hairline Fracture","Simple Fracture","Compound Fracture"]
},
"Concussion":{
"base_severity":4,
"treatment":(18,24),
"subtypes":["Mild","Moderate","Severe"]
},
"Simple Fracture":{
"base_severity":3,
"treatment":(12,18),
"subtypes":["Non-displaced","Displaced","Comminuted"]
},
"Appendicitis":{
"base_severity":5,
"treatment":(12,24),
"subtypes":["Early Stage","Acute","Perforated"]
},
"Pneumonia":{
"base_severity":4,
"treatment":(18,24),
"subtypes":["Mild","Moderate","Severe"]
},
}

BLOOD_PRESSURE_MEAN = 120
BLOOD_PRESSURE_STD = 15

PULSE_MEAN = 80
PULSE_STD = 10

TEMPERATURE_MEAN = 37.0
TEMPERATURE_STD = 0.5

TRIAGE_TIME_MIN = 0.25
TRIAGE_TIME_MAX = 0.75

SEVERITY_WEIGHTS = {
    "disease": 1.0,
    "subtype": 1.0,
    "vitals": 1.0,
    "age": 1.0
}

PRIORITY_WEIGHTS = {
    "severity": 0.7,
    "age": 0.3
}

PRIORITY_THRESHOLDS = {
    "HIGH": 6.0,
    "MEDIUM": 3.5
}

SAFE_WAIT_TIME = {
    "HIGH": 2,
    "MEDIUM": 5,
    "LOW": 8
}
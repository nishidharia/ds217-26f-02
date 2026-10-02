"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Give systolic reading from every encounter"""
    readings = []
    for encounter in encounters: 
        readings.append(encounter[2])
    return readings 


def mean_systolic(readings):
    """give mean systolic reading or none if the list is empty"""
    if len(readings) == 0:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Give the number of different patients in the ecoutners"""
    patient_ids = set()
    for encounter in encounters:
        patient_ids.add(encounter[0])
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Give the IDs of patients whose systolic reading is at or above the cutoff."""
    patient_ids = set()
    for encounter in encounters:
        if encounter[2] >= cutoff:
            patient_ids.add(encounter[0])
    return patient_ids

#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from dataclasses import fields
from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """give usable encounters and the number of skilled data rows"""
    encounters = []
    skipped = 0
    with open(data_path, "r") as file:
        lines = file.readlines()
    for line in lines[1:]:
        line = line.strip()
        if line == '':
            print("Skipping blank row")
            skipped += 1
        fields = line.split(",")
        if len(fields) != 3:
            print("Skipping row:", line)
            skipped += 1
            continue
        patient_id = fields[0]
        visit_date = fields[1]
        try:
            systolic = int(fields[2])
        except ValueError:
            print("Skipping row:", line)
            skipped += 1
            continue
        if systolic < 60 or systolic > 250:
            print("Skipping row:", line)
            skipped += 1
            continue

        encounters.append((patient_id, visit_date, systolic))

    return encounters, skipped

def main():
    """write the vitals report and follow-up patientlist."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)

    usable_count = len(encounters)
    patients_seen = count_patients(encounters)
    mean = mean_systolic(readings)
    highest = max(readings)
    lowest = min(readings)

    OUTPUT_DIR.mkdir(exist_ok=True)

    report = (
        f"Usable encounters: {usable_count}\n"
        f"Skipped rows: {skipped}\n"
        f"Patients seen: {patients_seen}\n"
        f"Mean systolic: {mean:.1f} mmHg\n"
        f"Highest systolic: {highest} mmHg\n"
        f"Lowest systolic: {lowest} mmHg\n"
    )

    report_path = OUTPUT_DIR / "vitals_report.txt"

    with open(report_path, "w") as file:
        file.write(report)

    with open(report_path, "r") as file:
        print(file.read())

    cutoff = 140
    reason = "I chose 140 mmHg to prioritize patients with higher systolic readings for follow-up."

    followup_patients = patients_at_or_above(encounters, cutoff)

    followup_path = OUTPUT_DIR / "followup_list.txt"

    with open(followup_path, "w") as file:
        file.write(f"Cutoff: {cutoff} mmHg\n")
        file.write(f"Reason: {reason}\n")

        for patient_id in followup_patients:
            file.write(f"{patient_id}\n")


if __name__ == "__main__":
    main()

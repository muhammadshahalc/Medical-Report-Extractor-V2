#utils.py
def initialize_record():
    return {
        "patient": {"name": "", "age": "", "gender": "", "date_of_report": ""},
        "tests": [],
        "diagnosis": ""
    }


def merge_records(base_record, new_record):
    """Merge a new page record into the base record."""
    # Merge patient info
    for key in base_record["patient"]:
        if not base_record["patient"][key] and new_record["patient"].get(key):
            base_record["patient"][key] = new_record["patient"][key]

    # Merge tests
    base_record["tests"].extend(new_record.get("tests", []))

    # Merge diagnosis
    if new_record.get("diagnosis"):
        base_record["diagnosis"] += " " + new_record["diagnosis"]

    base_record["diagnosis"] = base_record["diagnosis"].strip()
    return base_record

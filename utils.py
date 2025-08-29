def initialize_record():
    """Initialize an empty medical record structure."""
    return {
        "patient": {
            "name": "",
            "age": "",
            "gender": "",
            "date_of_report": ""
        },
        "tests": [],
        "diagnosis": "Not Mentioned"
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
    new_diag = new_record.get("diagnosis", "").strip()
    if new_diag and new_diag != "Not Mentioned":
        if base_record["diagnosis"] and base_record["diagnosis"] != "Not Mentioned":
            base_record["diagnosis"] += "; " + new_diag
        else:
            base_record["diagnosis"] = new_diag

    # Ensure we always have a fallback diagnosis
    if not base_record["diagnosis"]:
        base_record["diagnosis"] = "Not Mentioned"

    return base_record

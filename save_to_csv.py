import pandas as pd

def save_to_csv(merged_data, file_name, output_path="data/extracted_reports.csv"):
    """
    Save extracted medical data into CSV format.
    Columns:
    File Name, Patient Name, Age, Gender, Report Date, Tests Names, Test Results, Diagnosis/Observations
    """

    # Prepare tests (combine value + unit)
    test_names = []
    test_results = []
    for test in merged_data.get("tests", []):
        test_names.append(test.get("test_name", ""))
        value = str(test.get("value", ""))
        unit = str(test.get("unit", ""))
        test_results.append(f"{value} {unit}".strip())

    # Create a single row of data
    row = {
        "File Name": file_name,
        "Patient Name": merged_data["patient"].get("name", ""),
        "Age": merged_data["patient"].get("age", ""),
        "Gender": merged_data["patient"].get("gender", ""),
        "Report Date": merged_data["patient"].get("date_of_report", ""),
        "Tests Names": "; ".join(test_names),
        "Test Results": "; ".join(test_results),
        "Diagnosis/Observations": merged_data.get("diagnosis", ""),
    }

    # Save/append to CSV
    try:
        df = pd.read_csv(output_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([row])

    df.to_csv(output_path, index=False)
    return output_path

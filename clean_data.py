import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


SOURCE_DIR = Path.home() / "Desktop" / "side_quest"
OUTPUT_DIR = Path(__file__).parent / "cleaned_data"
NULL_VALUES = {"", "na", "n/a", "nan", "none", "null"}


def clean_value(value):
    if value is None:
        return ""
    value = value.strip()
    return "" if value.casefold() in NULL_VALUES else value


def parse_date(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        for date_format in ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y", "%m/%d/%y"):
            try:
                return datetime.strptime(value, date_format).date()
            except ValueError:
                continue
    return None


def open_csv_reader(path):
    source = path.open(newline="", encoding="utf-8-sig")
    reader = csv.DictReader(source)
    if not reader.fieldnames:
        source.close()
        raise ValueError(f"{path} does not contain a CSV header")
    return source, reader


def validate_columns(path, headers, required_columns):
    missing = required_columns.difference(headers)
    if missing:
        raise ValueError(f"{path.name} is missing required columns: {', '.join(sorted(missing))}")


def clean_permit_csv(source_path, output_path):
    required = {
        "Permit_Number",
        "Work_Type",
        "Date_of_Submission",
        "Date_of_Permit_Issuance",
    }
    source, reader = open_csv_reader(source_path)
    try:
        validate_columns(source_path, reader.fieldnames, required)
        kept = 0
        dropped = 0
        with output_path.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                cleaned = {key: clean_value(value) for key, value in row.items() if key is not None}
                submission = parse_date(cleaned["Date_of_Submission"])
                issuance = parse_date(cleaned["Date_of_Permit_Issuance"])
                if (
                    not cleaned["Permit_Number"]
                    or not cleaned["Work_Type"]
                    or submission is None
                    or issuance is None
                ):
                    dropped += 1
                    continue
                cleaned["Date_of_Submission"] = submission.isoformat()
                cleaned["Date_of_Permit_Issuance"] = issuance.isoformat()
                writer.writerow(cleaned)
                kept += 1
    finally:
        source.close()
    return kept, dropped


def clean_timeline_csv(source_path, output_path):
    required = {"Permit_Number", "Issuance_Stage", "Total_Duration"}
    source, reader = open_csv_reader(source_path)
    try:
        validate_columns(source_path, reader.fieldnames, required)
        kept = 0
        dropped = 0
        with output_path.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                cleaned = {key: clean_value(value) for key, value in row.items() if key is not None}
                if not cleaned["Permit_Number"] or not cleaned["Issuance_Stage"]:
                    dropped += 1
                    continue
                try:
                    duration = Decimal(cleaned["Total_Duration"])
                except InvalidOperation:
                    dropped += 1
                    continue
                if not duration.is_finite() or duration < 0:
                    dropped += 1
                    continue
                writer.writerow(cleaned)
                kept += 1
    finally:
        source.close()
    return kept, dropped


def main():
    permit_source = SOURCE_DIR / "PLC_permit.csv"
    timeline_source = SOURCE_DIR / "PLC_permit_time.csv"
    for path in (permit_source, timeline_source):
        if not path.is_file():
            raise FileNotFoundError(f"Expected source CSV was not found: {path}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    permit_result = clean_permit_csv(
        permit_source, OUTPUT_DIR / "PLC_permit_cleaned.csv"
    )
    timeline_result = clean_timeline_csv(
        timeline_source, OUTPUT_DIR / "PLC_permit_time_cleaned.csv"
    )

    print(f"PLC_permit.csv: kept {permit_result[0]:,}; excluded {permit_result[1]:,}.")
    print(
        "PLC_permit_time.csv: "
        f"kept {timeline_result[0]:,}; excluded {timeline_result[1]:,}."
    )
    print(f"Cleaned copies saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

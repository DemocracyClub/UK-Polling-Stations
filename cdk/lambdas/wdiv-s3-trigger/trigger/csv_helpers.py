import csv
from csv import excel

import chardet


def detect_ems(header):
    first_col = header[0].lower()
    if first_col == "houseid" and "addressline1" in [h.lower() for h in header]:
        return "Idox Eros (Halarose) 2026 Update"
    if first_col == "houseid":
        return "Idox Eros (Halarose)"
    if first_col == "authoritycode":
        return "Xpress WebLookup"
    if first_col == "electiondate":
        return "Xpress DC"
    if "xordinate" in [h.lower() for h in header]:
        return "Democracy Counts"
    return "unknown"


def get_body_sample(body: bytes):
    if b"\r\n" in body:
        line_sep = b"\r\n"
    elif b"\n" in body:
        line_sep = b"\n"
    else:
        return body
    lines = body.split(line_sep)
    if len(lines) > 20:
        return line_sep.join(lines[:20])
    return line_sep.join(lines)


def attempt_decode(body: bytes):
    sample = get_body_sample(body)
    detection = chardet.detect(sample)
    encoding = detection["encoding"]
    if encoding == "utf-16le":
        return body.decode(encoding), encoding
    encodings = ["utf-8", "windows-1252", "latin-1"]
    for encoding in encodings:
        try:
            return body.decode(encoding), encoding
        except UnicodeDecodeError as e:
            last_exception = e
            continue
    raise last_exception


def get_dialect(sample, key):
    # sometimes we get CSVs with a TSV extension or TSVs with a CSV extension,
    # so we'll try and use csv.Sniffer to work it out for us.
    try:
        return csv.Sniffer().sniff(sample, [",", "\t"])
    except csv.Error:
        # if that fails, make an assumption based on the file extension
        if key.lower().endswith(".tsv"):
            return "\t"
        return excel


def get_csv_report(response, key):
    report = {
        "csv_valid": False,
        "csv_rows": 0,
        "csv_encoding": "",
        "ems": "unknown",
        "errors": [],
    }
    body = response["Body"].read()
    if len(body) == 0:
        report["errors"].append("File is empty")
        return report

    try:
        decoded, csv_encoding = attempt_decode(body)
        report["csv_encoding"] = csv_encoding
    except UnicodeDecodeError:
        report["errors"].append("Failed to decode body using any expected encoding")
        return report

    dialect = get_dialect(decoded.splitlines()[0], key)
    records = csv.reader(
        decoded.splitlines(True),
        dialect=dialect,
        delimiter=dialect.delimiter,
        quotechar=dialect.quotechar,
    )
    try:
        header = next(records)
        expected_row_length = len(header)
        if expected_row_length < 3:
            report["errors"].append(
                f"File has only {expected_row_length} columns. We might have failed to detect the delimiter"
            )
            return report
        report["ems"] = detect_ems(header)
        total_rows = 1
        for record in records:
            length = len(record)
            total_rows += 1
            if length < expected_row_length:
                report["csv_valid"] = False
                report["errors"].append(
                    f"Incomplete file: Expected {expected_row_length} columns on row {total_rows} found {length}"
                )
                report["csv_rows"] = total_rows
                return report

        report["csv_valid"] = True
        report["csv_rows"] = total_rows
        return report
    except csv.Error as e:
        report["errors"].append(f"Failed to parse body -> line {records.line_num}: {e}")
        return report


def get_object_report(response, council_id):
    if response["ContentLength"] < 1024 and council_id != "IOS":
        return {"errors": ["Expected file to be at least 1KB"]}
    if response["ContentLength"] > 150_000_000:
        return {"errors": ["Expected file to be under 150MB"]}
    return {"errors": []}

import csv


def detect_ems(header):
    first_col = header[0].lower()
    if first_col == "houseid":
        return "Idox Eros (Halarose)"
    if first_col == "authoritycode":
        return "Xpress WebLookup"
    if first_col == "electiondate":
        return "Xpress DC"
    if "xordinate" in [h.lower() for h in header]:
        return "Democracy Counts"
    return "unknown"


def attempt_decode(body):
    encodings = ["utf-8", "windows-1252", "latin-1"]
    for encoding in encodings:
        try:
            return body.decode(encoding), encoding
        except UnicodeDecodeError as e:
            last_exception = e
            continue
    raise last_exception


def get_delimiter(sample, key):
    # sometimes we get CSVs with a TSV extension or TSVs with a CSV extension,
    # so we'll try and use csv.Sniffer to work it out for us.
    try:
        dialect = csv.Sniffer().sniff(sample, [",", "\t"])
        return dialect.delimiter
    except csv.Error:
        # if that fails, make an assumption based on the file extension
        if key.lower().endswith(".tsv"):
            return "\t"
        return ","


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

    delimiter = get_delimiter(decoded[0:10000], key)

    try:
        records = csv.reader(
            decoded.splitlines(True), delimiter=delimiter, quotechar='"'
        )
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
    except csv.Error:
        report["errors"].append("Failed to parse body")
        return report


def get_object_report(response):
    if response["ContentLength"] < 1024:
        return {"errors": ["Expected file to be at least 1KB"]}
    if response["ContentLength"] > 150_000_000:
        return {"errors": ["Expected file to be under 150MB"]}
    return {"errors": []}

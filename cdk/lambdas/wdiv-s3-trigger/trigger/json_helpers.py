import json
from json import JSONDecodeError

fcs_fields = [
    "id",
    "stationId",
    "name",
    "addressLine1",
    "addressLine2",
    "addressLine3",
    "addressLine4",
    "addressLine5",
    "addressPostCode",
    "addressUprn",
    "latitude",
    "longitude",
    "defaultStationId",
    "properties",
    "pollingDistricts",
]


def detect_ems(data):
    if isinstance(data, list) and len(data) > 0:
        if all(key in data[0] for key in fcs_fields):
            return "FCS"
    return "unknown"


def count_addresses(data, ems):
    if ems == "FCS":
        return sum(len(station["properties"]) for station in data)
    return 0


def get_json_report(response, key):
    report = {
        "csv_valid": False,
        "csv_rows": 0,
        "csv_encoding": "utf-8",  # always assume utf-8 for JSON
        "ems": "unknown",
        "errors": [],
    }
    body = response["Body"].read()
    if len(body) == 0:
        report["errors"].append("File is empty")
        return report

    try:
        data = json.loads(body)
        report["csv_valid"] = True
    except JSONDecodeError as e:
        report["errors"].append(str(e))
        return report

    report["ems"] = detect_ems(data)
    report["csv_rows"] = count_addresses(data, report["ems"])
    return report

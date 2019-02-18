from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from data_collection.addresshelpers import format_residential_address


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000001"
    addresses_name = "local.2019-05-02/Version 1/Polling Station Address Information 02 May 2019 Hartlepool.csv"
    stations_name = "local.2019-05-02/Version 1/Polling Station Address Information 02 May 2019 Hartlepool.csv"
    elections = ["local.2019-05-02"]

    # Hartlepool use Xpress, but they've provided a slightly trimmed down
    # version of the export. We need to customise a bit..
    station_uprn_field = None

    def address_record_to_dict(self, record):
        if record.post_code.strip() == "":
            return None
        address = format_residential_address(
            [
                record.addressline1,
                record.addressline2,
                record.addressline3,
                record.addressline4,
            ]
        )
        uprn = getattr(record, self.residential_uprn_field).strip().lstrip("0")
        postcode = record.post_code.strip()
        ret = {
            "address": address.strip(),
            "postcode": postcode,
            "polling_station_id": getattr(record, self.station_id_field).strip(),
            "uprn": uprn,
        }

        # corrections
        if postcode == "TS22 5QE":
            ret["postcode"] = "TS22 5FY"
        if postcode == "TS25 2HE":
            return None
        if uprn == "10090070423":
            ret["postcode"] = "TS25 2DY"
        if uprn == "10090070227":
            ret["postcode"] = "TS25 2BF"

        return ret

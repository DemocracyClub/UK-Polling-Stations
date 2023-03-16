from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "HAA"
    addresses_name = "2023-05-04/2023-03-16T14:48:52.200029/PropertyPostCodePollingStationWebLookup-2023-03-16.TSV"
    stations_name = "2023-05-04/2023-03-16T14:48:52.200029/PropertyPostCodePollingStationWebLookup-2023-03-16.TSV"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013683413",  # 47 WELLESLEY COURT, DARNEL ROAD, WATERLOOVILLE
        ]:
            return None
        if record.addressline6 in [
            "PO11 9LA",
        ]:
            return None

        return super().address_record_to_dict(record)

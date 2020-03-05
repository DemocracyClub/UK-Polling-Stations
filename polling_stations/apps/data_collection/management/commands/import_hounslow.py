from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000018"
    addresses_name = "2020-02-19T09:58:45.236148/Democracy_Club__7 May 2020.CSV"
    stations_name = "2020-02-19T09:58:45.236148/Democracy_Club__7 May 2020.CSV"
    elections = ["2020-05-07"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in [
            "TW4 6DH",
            "TW3 2PD",
        ]:
            return None

        if uprn in [
            "100021554382",  # SCHOOL HOUSE, 104 Martindale Road, Hounslow
            "100021514552",  # FLAT 1 36 HAMILTON ROAD, BRENTFORD
        ]:
            return None

        return rec

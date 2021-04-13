from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUG"
    addresses_name = "2021-03-25T13:16:40.725865/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T13:16:40.725865/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010525228",  # 46 STATION AVENUE, HOULTON, RUGBY
            "10010504659",  # FLAT, BELL & BARGE, BROWNSOVER ROAD, RUGBY
        ]:
            return None

        if record.addressline6 in [
            "CV21 2TE",
            "CV21 2EZ",
            "CV22 6NR",
            "CV23 1BP",
            "CV23 1BT",
        ]:
            return None

        return super().address_record_to_dict(record)

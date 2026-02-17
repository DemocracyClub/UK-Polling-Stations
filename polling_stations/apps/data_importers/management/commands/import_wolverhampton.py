from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLV"
    addresses_name = "2026-05-07/2026-01-22T16:58:37.246479/Update - Democracy_Club Wolverhampton 07May2026.tsv"
    stations_name = "2026-05-07/2026-01-22T16:58:37.246479/Update - Democracy_Club Wolverhampton 07May2026.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093324969",  #  24 WOOD STREET, HEATH TOWN, WOLVERHAMPTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "WV3 9AY",
            "WV2 2BF",
            "WV10 8BA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction from council for:
        # St Joseph`s Church Hall, Coalway Road, Wolverhampton WV3 7LF
        if record.polling_place_id == "32993":
            record = record._replace(polling_place_postcode="WV3 7NG")

        return super().station_record_to_dict(record)

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLV"
    addresses_name = "2024-07-04/2024-05-31T11:56:01.424909/Wolverhampton polling stations - Democracy Club.tsv"
    stations_name = "2024-07-04/2024-05-31T11:56:01.424909/Wolverhampton polling stations - Democracy Club.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "WV2 2BF",
            "WV3 9AY",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Joseph`s Church Hall, Coalway Road, Wolverhampton WV3 7LF
        if record.polling_place_id == "31519":
            record = record._replace(polling_place_postcode="")
        return super().station_record_to_dict(record)

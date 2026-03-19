from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BDG"
    addresses_name = (
        "2026-05-07/2026-03-05T15:43:47.815524/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-05T15:43:47.815524/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100092520",  # SHIP AND SHOVEL RIPPLE ROAD, BARKING
            "10023598442",  # 36A WHALEBONE LANE SOUTH, DAGENHAM
            "10023592360",  # 32A WHALEBONE LANE SOUTH, DAGENHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RM8 3PT",
            "IG11 0PP",
            # looks wrong
            "IG11 0SR",
            "IG11 7PD",
            "IG11 8TJ",
            "IG11 8TP",
            "RM10 8FA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Barley Hall, Ethelburga Way, Barking, IG11 7JG
        if record.polling_place_id == "8335":
            record = record._replace(polling_place_postcode="IG11 7EX")

        return super().station_record_to_dict(record)

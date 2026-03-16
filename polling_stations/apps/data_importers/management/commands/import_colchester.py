from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2026-05-07/2026-03-16T12:39:16.036477/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-16T12:39:16.036477/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10070229236",  # COLCHESTER FABRICATIONS, THE SWALLOWS, WORMINGFORD ROAD, FORDHAM, COLCHESTER, CO6 3NS
                "100091472547",  # SIMPLE VAN HIRE, 88A COGGESHALL ROAD, MARKS TEY, COLCHESTER, CO6 1LS
                "10034898298",  # MERVILLE BARRACKS, POST ROOM, CIRCULAR ROAD SOUTH, COLCHESTER, CO2 7UT
                "10095444509",  # 2A BELLE VUE ROAD, WIVENHOE, COLCHESTER, CO7 9LE
                "10095445911",  # 32D MAYPOLE GREEN ROAD, COLCHESTER, CO2 9NX
                "10095443897",  # RUNKINS FARM, LANGHAM LANE, BOXTED, COLCHESTER
            ]
        ):
            return None

        if record.post_code in [
            # splits
            "CO4 5LG",
            "CO2 8BU",
            "CO6 1HA",
            # looks wrong
            "CO4 3ZP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: St Cedd`s Church Hall, Iceni Way, Colchester, CO2 9BZ
        if record.polling_place_id == "14536":
            record = record._replace(polling_place_postcode="CO2 9EH")

        return super().station_record_to_dict(record)

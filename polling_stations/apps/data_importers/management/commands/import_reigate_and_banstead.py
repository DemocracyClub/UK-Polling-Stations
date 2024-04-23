from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "REI"
    addresses_name = (
        "2024-05-02/2024-03-05T11:26:20.067521/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-05T11:26:20.067521/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.lstrip("0")

        if uprn in [
            "68134095",  # CHIDWELL FARMING, NICOLA FARM, 37 WWOODMANSTERNE LANE, BANSTEAD
            "68137043",  # 170 DOVERS GREEN ROAD, REIGATE
            "68137147",  # 168 DOVERS GREEN ROAD, REIGATE
            "68183366",  # MYRTLE COTTAGE, HORLEY LODGE LANE, REDHILL
            "68115368",  # 1 DEAN LANE, MERSTHAM, REDHILL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RH6 8DU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station change requested by council:
        # OLD: Banstead Methodist Church, The Drive, Banstead, SM7 1DA
        # NEW: Nork Community Centre, Nork Way, Banstead SM7 1JB
        if record.polling_place_id == "4979":
            record = record._replace(
                polling_place_name="Nork Community Centre",
                polling_place_address_1="Nork Way",
                polling_place_address_2="Banstead",
                polling_place_address_3="",
                polling_place_address_4="",
                polling_place_postcode="SM7 1JB",
                polling_place_easting="523774",
                polling_place_northing="159336",
            )

        # more accurate point for: Woodmansterne Village Hall, Carshalton Road, Woodmansterne, Banstead, Surrey
        if record.polling_place_id == "5001":
            record = record._replace(
                polling_place_easting="527572", polling_place_northing="160117"
            )

        return super().station_record_to_dict(record)

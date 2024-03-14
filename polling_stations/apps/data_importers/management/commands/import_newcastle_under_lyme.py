from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEC"
    addresses_name = (
        "2024-05-02/2024-03-14T17:42:31.686074/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-14T17:42:31.686074/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Higherland Methodist Church Hall Higherland Newcastle Staffs ST5 2TF
        if record.polling_place_id == "3190":
            record = record._replace(polling_place_easting="384574")
            record = record._replace(polling_place_northing="345703")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002872601",  # 125A LIVERPOOL ROAD, NEWCASTLE
            "100032216255",  # CROSS HEATH NEWS, 121 LIVERPOOL ROAD, NEWCASTLE
            "10024252556",  # BRIERYHURST FARM HOUSE, MOW LANE, MOW COP, STOKE-ON-TRENT
            "10002238961",  # 2 BRIERYHURST FARM BUNGALOW THE HOLLOW, MOW COP
            "10094839598",  # BRIERY VIEW, MOW LANE, MOW COP, STOKE-ON-TRENT
            "10002237282",  # WILLOUGHBRIDGE WELLS LODGE, WILLOUGHBRIDGE, MARKET DRAYTON
            "100031723127",  # 7 DEANS LANE, NEWCASTLE
            "100031723126",  # 6 DEANS LANE, NEWCASTLE
            "100031723129",  # STARBOROUGH HOUSE, DEANS LANE, NEWCASTLE
            "100031723128",  # 8 DEANS LANE, NEWCASTLE
        ]:
            return None

        if record.addressline6 in [
            # split
            "ST5 4DU",
            "ST5 8QG",
            "ST7 1DY",
            "TF9 4PW",
            "TF9 4PN",
            # suspect
            "ST5 6BS",
        ]:
            return None

        return super().address_record_to_dict(record)

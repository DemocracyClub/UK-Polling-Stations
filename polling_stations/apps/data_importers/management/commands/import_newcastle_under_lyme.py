from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEC"
    addresses_name = (
        "2022-05-05/2022-03-23T13:32:11.842979/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T13:32:11.842979/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Higherland Methodist Church Hall Higherland Newcastle Staffs ST5 2TF
        if record.polling_place_id == "2633":
            record = record._replace(polling_place_easting="384574")
            record = record._replace(polling_place_northing="345703")

        # Salvation Army, Heathcote Street, Kidsgrove, Stoke on Trent
        if record.polling_place_id == "2752":
            record = record._replace(polling_place_postcode="ST7 4AA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100032219337",  # ARDENNE THE AVENUE, KIDSGROVE
            "10024255961",  # 4B WARWICK CLOSE, KIDSGROVE, STOKE-ON-TRENT
            "10024255960",  # 4A WARWICK CLOSE, KIDSGROVE, STOKE-ON-TRENT
            "200002872601",  # 125A LIVERPOOL ROAD, NEWCASTLE
            "100032216255",  # CROSS HEATH NEWS, 121 LIVERPOOL ROAD, NEWCASTLE
            "200004612280",  # CARAVAN RED STREET STABLES TALKE ROAD, BRADWELL, NEWCASTLE UNDER LYME
            "10024252556",  # BRIERYHURST FARM HOUSE, MOW LANE, MOW COP, STOKE-ON-TRENT
            "10002238961",  # 2 BRIERYHURST FARM BUNGALOW THE HOLLOW, MOW COP
        ]:
            return None

        if record.addressline6 in [
            "ST5 2TP",
            "ST5 4DU",
            "ST5 6JY",
            "ST5 8DS",
            "ST7 1DY",
        ]:
            return None

        return super().address_record_to_dict(record)

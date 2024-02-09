from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAI"
    addresses_name = (
        "2024-05-02/2024-02-09T08:21:20.078163/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-09T08:21:20.078163/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # The Nevendon Centre, Nevendon Road, Wickford, Essex
        if record.polling_place_id == "7191":
            record = record._replace(polling_place_easting="574486")
            record = record._replace(polling_place_northing="193177")

        # Laindon Library, 5-7 New Century Road, Laindon, Basildon, SS15 6AG
        if record.polling_place_id == "7098":
            record = record._replace(polling_place_easting="567896")
            record = record._replace(polling_place_northing="188830")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091212751",  # PROBATION OFFICE, 1 FELMORES, BASILDON
            "100090239089",  # 17 CHURCH ROAD, LAINDON, BASILDON
            "100090273531",  # 23 GREENS FARM LANE, BILLERICAY
            "10090682049",  # CEDAR COTTAGE, LOWER DUNTON ROAD, BULPHAN, UPMINSTER
        ]:
            return None

        if record.addressline6 in [
            # split
            "SS15 5GX",
            "CM11 2AD",
            "SS15 6PF",
            "CM11 2JX",
            "SS15 5NZ",
            "SS16 6PH",
            "CM11 2RU",
            # suspect
            "SS13 3RL",
        ]:
            return None

        return super().address_record_to_dict(record)

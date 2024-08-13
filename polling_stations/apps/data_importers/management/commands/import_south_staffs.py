from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2024-07-04/2024-05-31T15:57:56.112836/Democracy_Club__04July2024 SSDC.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T15:57:56.112836/Democracy_Club__04July2024 SSDC.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100031833008",  # CHILLINGTON LODGE, WHITEHOUSE LANE, CODSALL WOOD, WOLVERHAMPTON
                "100031799992",  # GREENSFORGE HOUSE, GREENSFORGE, KINGSWINFORD, DY6 0AH
                "200004524554",  # IVETSEY BANK FARM, IVETSEY BANK, WHEATON ASTON, STAFFORD
                "10094875300",  # POOL FARM BUNGALOW, GAILEY LEA LANE, GAILEY, STAFFORD ST19 5PT
                "100032282008",  # SHOOT LODGE, TEDDESLEY ROAD, PENKRIDGE, STAFFORD
                "10090093164",  # 3 HAY HOUSE COURT, DUNSTON HEATH, STAFFORD
                "10090091050",  # 2 HAY HOUSE COURT, DUNSTON HEATH, STAFFORD
                "10090091049",  # 1 HAY HOUSE COURT, DUNSTON HEATH, STAFFORD
                "200004526134",  # 135 RODBASTON, PENKRIDGE, STAFFORD
                "200004528062",  # AMBLESIDE, WOLVERHAMPTON ROAD, PENKRIDGE, STAFFORD
                "10003692787",  # 7B SANDYFIELDS ROAD, DUDLEY
                "10003693861",  # WILD WOOD, COUNTY LANE, ALBRIGHTON, WOLVERHAMPTON
                "10003693386",  # M S J HEALTHCARE, KARTER FARM, NEW ROAD, SWINDON, DUDLEY
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "ST19 9AB",
            "WV11 2DN",
            "ST19 9AG",
            "WV9 5BW",
            # suspect
            "WV5 8EX",
            "WV11 2RD",
            "ST19 9LX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Bartholomew's Church Hall, Vicarage Road, Penn, Wolverhampton
        if record.polling_place_id == "5468":
            record = record._replace(
                polling_place_easting="389364", polling_place_northing="295314"
            )

        return super().station_record_to_dict(record)

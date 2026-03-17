from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2026-05-07/2026-02-23T09:23:31.641167/Democracy_Club__07May2026 (1).tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-23T09:23:31.641167/Democracy_Club__07May2026 (1).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10094904420",  # 35 FLEMINGS FARM CLOSE, RUNWELL, WICKFORD, SS11 7PJ
                "10094904422",  # 12 FLEMINGS FARM CLOSE, RUNWELL, WICKFORD, SS11 7PL
                "10094904409",  # 23 FLEMINGS FARM CLOSE, RUNWELL, WICKFORD, SS11 7PJ
                "100091430917",  # CORNER COTTAGE, MARGARETTING ROAD, WRITTLE, CHELMSFORD, CM1 3PJ
                "10093928574",  # MONTPELIERS FARMHOUSE, MARGARETTING ROAD, WRITTLE, CHELMSFORD, CM1 3PJ
                "100091440884",  # 1 BARRACK SQUARE, CHELMSFORD, CM2 0UU
                "10093928503",  # HONEYSTONE, SOUTHEND ROAD, HOWE GREEN, CHELMSFORD, CM2 7TD
                "100091430409",  # BASSMENT NIGHTCLUB, 16-18 WELLS STREET, CHELMSFORD, CM1 1HZ
            ]
        ):
            return None

        if record.post_code in [
            # splits
            "CM1 7AR",
            "CM1 1FU",
            "CM3 1ER",
            "CM4 9JL",
            "CM4 0LT",
            # looks wrong
            "CM2 0UU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Postcode correction for: Rettendon Memorial Hall, Main Road, Rettendon, Chelmsford, CM3 8DR
        if record.polling_place_id == "14871":
            record = record._replace(polling_place_postcode="CM3 8DP")
        return super().station_record_to_dict(record)

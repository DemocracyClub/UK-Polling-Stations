from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2024-12-12/2024-11-20T15:03:43.866922/Democracy_Club__12December2024.tsv"
    )
    stations_name = (
        "2024-12-12/2024-11-20T15:03:43.866922/Democracy_Club__12December2024.tsv"
    )
    elections = ["2024-12-12"]
    csv_delimiter = "\t"

    # Ignoring the warnings RE the following stations
    # (Council has confirmed the current postcodes are correct):
    # 'East Hanningfield Village Hall, The Tye, East Hanningfield, Chelmsford, CM3 8AE' (id: 13209)
    # 'Civic Centre - Chelmsford City Council, Duke Street, Chelmsford, CM1 1JE' (id: 13420)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100091430409",  # BASSMENT NIGHTCLUB, 16-18 WELLS STREET, CHELMSFORD
                "200004630041",  # NEW BUNGALOW, TURKEY FARM, WINDSOR ROAD, DOWNHAM, BILLERICAY
                "10093928503",  # HONEYSTONE, SOUTHEND ROAD, HOWE GREEN, CHELMSFORD
            ]
        ):
            return None

        # removing addresses for NPR
        if record.polling_place_id in [
            "14153",  # Danbury Chapel
            "14039",  # Danbury Leisure Centre
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # removing stations for NPR
        if record.polling_place_id in [
            "14153",  # Danbury Chapel
            "14039",  # Danbury Leisure Centre
        ]:
            return None

        return super().station_record_to_dict(record)

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAS"
    addresses_name = (
        "2024-07-04/2024-06-18T10:36:29.124832/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-18T10:36:29.124832/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100090360367",  # 210 KENTS HILL ROAD, BENFLEET
                "100091599588",  # 115 DOWNER ROAD, BENFLEET
                "10004941351",  # 420 DAWS HEATH ROAD, BENFLEET
                "10004941352",  # 422 DAWS HEATH ROAD, BENFLEET
                "10094905546",  # BIRD OF PARADISE SMALL GAINS MARINA POINT ROAD, CANVEY ISLAND
            ]
        ):
            return None
        if record.addressline6 in [
            # split
            "SS8 8HN",
            "SS8 9SL",
            "SS8 7PJ",
            "SS7 1HH",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Fixing missing postcode:
        # Runnymede Hall Foyer, Rear of Council Offices, Kiln Road, Thundersley, Benfleet
        if record.polling_place_id in ["2853", "2855"]:
            record = record._replace(polling_place_postcode="SS7 1TF")

        return super().station_record_to_dict(record)

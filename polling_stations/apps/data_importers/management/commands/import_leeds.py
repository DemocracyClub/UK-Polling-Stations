from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LDS"
    addresses_name = (
        "2023-05-04/2023-03-09T13:54:42.945922/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T13:54:42.945922/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "72132919",  # EBOR COTTAGE, MIDDLETON ROAD, LEEDS
            "72721195",  # FLAT PENDAS ARMS NABURN APPROACH, WHINMOOR, LEEDS
        ]:
            return None

        if record.addressline6 in [
            # SPLIT
            "LS10 4BD",
            "LS25 1AX",
            "WF3 2GL",
            "WF3 2GN",
            "WF3 1TB",
            "LS9 6LP",
            "WF3 1GQ",
            "LS12 2BN",
            "LS15 0LG",
            "LS10 4AZ",
            "LS17 9ED",
            "LS8 2QG",
            "WF3 1FX",
            "LS10 4ET",
            "LS16 7SU",
            "LS18 5HN",
            # WRONG
            "LS2 7DJ",
            "LS19 7RZ",
            "LS9 8DU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Haigh Road Community Centre
        if record.polling_place_id == "14987":
            record = record._replace(
                polling_place_easting="434066", polling_place_northing="428893"
            )
        return super().station_record_to_dict(record)

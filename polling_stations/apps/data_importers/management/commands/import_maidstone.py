from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAI"
    addresses_name = (
        "2022-05-05/2022-03-23T15:47:49.310266/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T15:47:49.310266/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Ulcombe Village Hall, Headcorn Road, Ulcombe, Maidstone
        if record.polling_place_id == "3183":
            record = record._replace(polling_place_postcode="ME17 1EB")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "ME15 9RA",
            "ME18 6AT",
        ]:
            return None  #  split
        return super().address_record_to_dict(record)

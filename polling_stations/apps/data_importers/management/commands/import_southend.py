from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = (
        "2024-05-02/2024-03-18T12:13:52.746718/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-18T12:13:52.746718/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Booth 2, Earls Hall Primary School, (Colemans Avenue Entrance), Westcliff-on-Sea
        if record.polling_place_id == "9382":
            record = record._replace(
                polling_place_easting="586595", polling_place_northing="187653"
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SS9 1RP",
            "SS9 1QY",
            "SS9 1NH",
            "SS9 1LN",
            "SS9 4RP",
            "SS3 9QH",
            "SS9 5EW",
        ]:
            return None

        return super().address_record_to_dict(record)

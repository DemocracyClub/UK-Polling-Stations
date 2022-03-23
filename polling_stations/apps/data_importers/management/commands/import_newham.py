from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = (
        "2022-05-05/2022-03-23T16:02:55.134381/LBNewham_Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T16:02:55.134381/LBNewham_Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Winsor Primary School, East Ham Manor Way, Beckton, London
        if record.polling_place_id == "7284":
            record = record._replace(polling_place_postcode="E6 5NA")  # was E6 4NA

        # Checked The Hall, 2-4 Victory Parade, as it's out of district.
        # Its postcode (E20 1FS) is correct.

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["E6 3JE"]:
            return None  # split

        return super().address_record_to_dict(record)

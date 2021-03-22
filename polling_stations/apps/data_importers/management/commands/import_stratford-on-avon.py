from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STR"
    addresses_name = (
        "2021-03-08T19:57:06.704590/Stratford DC Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-08T19:57:06.704590/Stratford DC Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "9600",  # Eric Payne Community Centre
            "9594",  # Alcester Methodist Church
        ]:
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "CV35 0AE",
            "CV36 4JA",
            "CV36 4PJ",
            "CV36 5LR",
            "OX17 1DH",
            "CV37 8FH",
            "CV37 7JS",
        ]:
            return None

        return super().address_record_to_dict(record)

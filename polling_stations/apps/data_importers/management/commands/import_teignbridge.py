from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEI"
    addresses_name = (
        "2021-03-30T13:07:24.373977/Teignbridge Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-30T13:07:24.373977/Teignbridge Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Alice Cross Day Centre
        if record.polling_place_id == "7926":
            record = record._replace(polling_place_easting="293930")
            record = record._replace(polling_place_northing="73047")

        return super().station_record_to_dict(record)

    #
    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "EX7 9PL",
            "TQ12 1EW",
            "TQ12 1HR",
            "TQ12 2JA",
            "TQ12 4AH",
            "TQ12 5HU",
            "TQ12 6NX",
            "TQ13 7BU",
            "TQ13 9TR",
            "TQ14 8NL",
            "TQ14 8NX",
            "TQ14 8SR",
            "TQ14 9AA",
            "TQ14 9AZ",
            "TQ14 9EN",
            "TQ14 9LD",
            "TQ14 9LZ",
        ]:
            return None

            if record.addressline6.strip() == "TQ13 8JG":
                record._replace(addressline6="TQ13 9JG")

        if (
            record.addressline1.strip() == "Little Park Farm"
            and record.addressline2.strip() == "Doddiscombsleigh"
            and record.addressline3.strip() == "Exeter"
            and record.addressline6.strip() == "EX6 8PA"
        ):
            record = record._replace(addressline6="EX6 7PZ")

        if (
            record.addressline1.strip() == "Flat 3 Old Globe Hotel"
            and record.addressline2.strip() == "15 North Street"
            and record.addressline3.strip() == "Ashburton"
            and record.addressline6.strip() == "TQ13 9HD"
        ):
            record = record._replace(addressline6="TQ13 7QH")

        return super().address_record_to_dict(record)

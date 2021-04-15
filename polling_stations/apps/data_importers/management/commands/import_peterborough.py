from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PTE"
    addresses_name = "2021-03-30T10:49:55.510017/Democracy_Club__06May2021 - Peterborough City Council.tsv"
    stations_name = "2021-03-30T10:49:55.510017/Democracy_Club__06May2021 - Peterborough City Council.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        # Hampton Leisure Centre Clayburn Road Hampton Vale Peterborough PE7 8HQ
        if record.polling_place_id == "8846":
            record = record._replace(polling_place_postcode="PE7 8HG")

        # St Andrews Church Russell Hill Thornhaugh Peterborough PE6 6NW
        if record.polling_place_id == "8986":
            record = record._replace(polling_place_postcode="")

        # Copeland Community Centre 37 Copeland Bretton Peterborough PE3 9YJ
        if record.polling_place_id == "8978":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008072993",  # 271 CLARENCE ROAD, PETERBOROUGH
            "10094542529",  # 64 GREENFIELD WAY, HAMPTON WATER, PETERBOROUGH
        ]:
            return None

        if record.addressline6 in [
            "PE6 7EN",
            "PE2 9HZ",
            "PE1 5ET",
            "PE7 8NQ",
            "PE7 0LE",
            "PE1 2JF",
            "PE1 2PW",
            "PE1 2EQ",
            "PE1 2NQ",
            "PE1 4AR",
            "PE7 3BW",
            "PE2 8FY",
            "PE3 6HP",
        ]:
            return None

        return super().address_record_to_dict(record)

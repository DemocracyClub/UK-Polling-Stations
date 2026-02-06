from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ISL"
    addresses_name = (
        "2026-05-07/2026-02-06T10:31:08.966210/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-06T10:31:08.966210/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
    # Ignore postcode mismatches for:
    # 'N4 Library, 26 Blackstock Road, London, N4 2JF'
    # 'St Joan of Arc Community Centre, Kelross Road, London, N5 2QN'
    # 'Harry Rice Hall, 72-74 Hargrave Park, London, N19 5JN'
    # 'Cornwallis Adventure Playground, Cornwallis Road, London, N19 4LP'
    # 'Vernon Hall, Vernon Square, King's Cross Road, WC1X 9EP' (id: 3152)
    # 'New Life Centre, 8-10 Lennox Road, London, N4 3NW' (id: 3064)
    # 'Whittington Community Centre, Yerbury Road, London, N19 4RS' (id: 3085)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10093113062",  #  103C SEVEN SISTERS ROAD, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)

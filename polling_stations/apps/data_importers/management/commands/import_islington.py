from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ISL"
    addresses_name = (
        "2024-05-02/2024-03-15T12:44:49.222514/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-15T12:44:49.222514/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # The following stations generate mismatched postcode warnings but have been verified
    # with the council as correct:
    # 'St Joan of Arc Community Centre, Kelross Road, London, N5 2QN' (id: 2689)
    # 'N4 Library, 26 Blackstock Road, London, N4 2JF' (id: 2692)
    # 'Harry Rice Hall, 72-74 Hargrave Park, London, N19 5JN' (id: 2571)
    # 'Cornwallis Adventure Playground, Cornwallis Road, London, N19 4LP' (id: 2583)
    # 'Vernon Hall, Vernon Square, King's Cross Road, WC1X 9EP' (id: 2636)
    # 'Williamson Street Community Centre, Trefil Walk, Parkhurst Road, London, N7 0SX' (id: 2662)
    # 'Aubert Court Community Centre, Avenell Road, N5 1BT' (id: 2700)

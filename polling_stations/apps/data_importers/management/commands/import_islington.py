from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ISL"
    addresses_name = (
        "2024-07-04/2024-05-31T13:32:36.325253/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T13:32:36.325253/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    # The following stations generate mismatched postcode warnings but have been verified
    # with the council as correct:
    # 'St Joan of Arc Community Centre, Kelross Road, London, N5 2QN' (id: 2904)
    # 'N4 Library, 26 Blackstock Road, London, N4 2JF' (id: 2926)
    # 'Harry Rice Hall, 72-74 Hargrave Park, London, N19 5JN' (id: 2870)
    # 'Cornwallis Adventure Playground, Cornwallis Road, London, N19 4LP' (id: 2882)
    # 'Vernon Hall, Vernon Square, King's Cross Road, WC1X 9EP' (id: 2966)
    # 'Williamson Street Community Centre, Trefil Walk, Parkhurst Road, London, N7 0SX' (id: 2987)
    # 'Aubert Court Community Centre, Avenell Road, N5 1BT' (id: 2895)

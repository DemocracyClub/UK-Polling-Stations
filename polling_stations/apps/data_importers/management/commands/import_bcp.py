from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = (
        "2022-10-06/2022-09-13T16:21:27.820706/Democracy_Club__06October2022.CSV"
    )
    stations_name = (
        "2022-10-06/2022-09-13T16:21:27.820706/Democracy_Club__06October2022.CSV"
    )
    elections = ["2022-10-06"]

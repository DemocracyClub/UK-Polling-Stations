from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    """
    Imports the Polling Station data from Ceredigion
    """

    council_id = "CGN"
    addresses_name = (
        "2021-04-07T14:45:08.852408/DEMOCRACY CLUB - POLLING DISTRICTS 30235.csv"
    )
    stations_name = (
        "2021-04-07T14:45:08.852408/DEMOCRACY CLUB - POLLING STATIONS (2).csv"
    )
    csv_encoding = "latin-1"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip(" 0")

        if uprn in [
            "49061701",
            "49049138",
            "49069702",
            "49047840",
            "49041491",
        ]:
            return None  # significantly overlaps other polling areas

        return super().address_record_to_dict(record)

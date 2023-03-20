from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BAS"
    addresses_name = "2023-05-04/2023-03-20T14:03:01.811295/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-03-20T14:03:01.811295/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    # Note: these warning has been checked and all looks fine.
    # > WARNING: Polling stations 'Welton Vale Community Room 9 Welton Vale' and
    # > 'The Salvation Army Radstock Road / Stones Cross' are at approximately the same
    # > location
    #
    # The centroid is outside, but the polling place is within.
    # > WARNING: Polling station Prattens Westfield Amateur Sports Club is in Mendip
    # > District Council (MEN) but target council is Bath & North East Somerset Council
    # > (BAS) - manual check recommended

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "BA2 2RZ",
            "BA2 6DR",
            "BA2 5AD",
            "BS31 2GF",
        ]:
            return None

        return super().address_record_to_dict(record)

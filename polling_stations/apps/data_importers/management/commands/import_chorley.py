from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHO"
    addresses_name = "2025-05-01/2025-02-28T08:34:33.193115/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-02-28T08:34:33.193115/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]

    def station_record_to_dict(self, record):
        # The following station's postcode has been confirmed by the council:
        # BUCKSHAW ROF SCOUT GROUP, MILE STONE MEADOW, EUXTON, CHORLEY, PR7 6FX (id: 97)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100010387618",  # MILLSTONE HOUSE, THE GREEN, ECCLESTON, CHORLEY
        ]:
            return None

        if record.housepostcode in [
            # split
            "PR7 2QL",
            "PR6 0HT",
            # suspect
            "PR26 9HE",
        ]:
            return None

        return super().address_record_to_dict(record)

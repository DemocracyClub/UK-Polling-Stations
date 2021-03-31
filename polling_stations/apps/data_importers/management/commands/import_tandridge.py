from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TAN"
    addresses_name = "2021-03-16T13:46:43.742650/polling_station_export-2021-03-16.csv"
    stations_name = "2021-03-16T13:46:43.742650/polling_station_export-2021-03-16.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062498517",  # SWEET BRIAR BARN, NEWCHAPEL ROAD, LINGFIELD
            "100062499148",  # SCHOOL HOUSE, TANDRIDGE LANE, TANDRIDGE, OXTED
            "200000141065",  # OLD MOAT BARN, ARDENRUN, LINGFIELD
            "200000146196",  # DERHILL, STATION ROAD, WOLDINGHAM, CATERHAM
        ]:
            return None

        if record.housepostcode in ["CR3 6HG", "RH7 6JH", "CR6 9LB", "TN16 2EX"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St. Peter's Hall High Street Limpsfield Oxted RH8 ODG
        if (record.pollingstationnumber, record.pollingstationpostcode) == (
            "32",
            "RH8 ODG",
        ):
            record = record._replace(pollingstationpostcode="RH8 0DG")

        return super().station_record_to_dict(record)

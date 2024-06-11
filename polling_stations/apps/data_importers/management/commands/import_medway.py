from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MDW"
    addresses_name = "2024-07-04/2024-06-05T18:33:15.401473/Eros_SQL_Output012.csv"
    stations_name = "2024-07-04/2024-06-05T18:33:15.401473/Eros_SQL_Output012.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062394561",  # WESTBANK FARM, CAPSTONE ROAD, GILLINGHAM
        ]:
            return None

        if record.housepostcode in [
            # split
            "ME8 8DB",
            # suspect
            "ME1 2EZ",
            "ME1 2FD",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Main Hall, Gillingham Baptist Church, Green Street, MR7 5TJ
        if self.get_station_hash(record) == "27-main-hall-gillingham-baptist-church":
            record = record._replace(pollingstationpostcode="ME7 5TJ")

        return super().station_record_to_dict(record)

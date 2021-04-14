from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WLN"
    addresses_name = "2021-04-14T09:51:22.820489/edinburgh_lothians_polling_station_export-2021-04-13.csv"
    stations_name = "2021-04-14T09:51:22.820489/edinburgh_lothians_polling_station_export-2021-04-13.csv"
    elections = ["2021-05-06"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)

        if record.adminarea.lower().strip() != "west lothian":
            return None
        if station_hash in (
            "142-kirknewton-village-hall",
            "147-centenary-hall",
            "80-craig-inn-centre",
            "0-echline-primary-school",
            "343-echline-primary-school",
            "0-kirkliston-community-centre",
            "352-kirkliston-community-centre",
        ):
            return None
        if record.housepostcode in (
            "EH47 0EY",
            "EH48 2GT",
            "EH48 3HL",
            "EH47 7NL",
            "EH54 8FF",
            "EH53 0GJ",
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if record.adminarea.lower().strip() != "west lothian":
            return None

        if station_hash in [
            "142-kirknewton-village-hall",
            "147-centenary-hall",
            "80-craig-inn-centre",
            "0-echline-primary-school",
            "343-echline-primary-school",
            "0-kirkliston-community-centre",
            "352-kirkliston-community-centre",
        ]:
            print(station_hash)
            return None

        return super().station_record_to_dict(record)

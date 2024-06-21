from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "GOS"
    addresses_name = "2024-07-04/2024-05-31T12:38:18.136820/2024 PGE - Democracy Club Polling Districts v1 (31 05 2024).csv"
    stations_name = "2024-07-04/2024-05-31T12:38:18.136820/2024 PGE - Democracy Club Polling Stations v1 (31 05 2024).csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # Fareham stations
        if record.stationcode in (
            "48ST1",  # Crofton Community Centre
            "47HH4",  # Crofton Community Centre
            "46HH3",  # Crofton Community Centre
            "44HH1",  # Crofton Community Centre
            "45HH2",  # Crofton Community Centre
            "49ST2",  # Stubbington Methodist Church Hall
            "50ST3",  # Stubbington Methodist Church Hall
            "51ST4",  # Stubbington Baptist Church
        ):
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # suspect
            "PO12 1SE",
            "PO12 4AW",
            "PO12 4QE",
            "PO12 4JP",
        ]:
            return None

        return super().address_record_to_dict(record)

from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CMD"
    addresses_name = "2026-10-08/2026-09-21T12:02:48.533067/Polling Districts.csv"
    stations_name = "2026-10-08/2026-09-21T12:02:48.533067/Polling Stations.csv"
    elections = ["2026-10-08"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # correction from council on 25/09/2026
        if rec["internal_council_id"] == "PD":
            rec["address"] = "Abacus Belsize Primary School\n105 Camley Street\nLondon"
            rec["postcode"] = "N1C 4PF"
            rec["location"] = None

        return rec

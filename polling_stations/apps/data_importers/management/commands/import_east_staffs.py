from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "EST"
    addresses_name = "2021-02-23T13:27:13.045364/Democracy Club - Polling Districts.csv"
    stations_name = "2021-02-23T13:27:13.045364/Democracy Club - Polling Stations.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if rec and rec["postcode"] in ["ST14 8SG"]:
            # Spurious polling place for one property
            return None

        return rec

    def station_record_to_dict(self, record):
        # Shobnall Primary School
        if record.stationcode == "BP_21":
            record = record._replace(
                xordinate="422735", yordinate="323640", postcode="DE14 2BB"
            )

        # St Giles Church, Croxden Lane
        if record.stationcode == "AA_63":
            record = record._replace(
                xordinate="406486", yordinate="339871", postcode="ST14 5JG"
            )

        return super().station_record_to_dict(record)

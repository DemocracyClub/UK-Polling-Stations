from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GLG"
    addresses_name = "2022-05-05/2022-03-30T10:30:41.528184/Glasgow_polling_station_export-2022-03-28.csv"
    stations_name = "2022-05-05/2022-03-30T10:30:41.528184/Glasgow_polling_station_export-2022-03-28.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "G14 9HQ",
            "G21 2LN",
            "G21 4UH",
            "G22 6RL",
            "G33 3SU",
            "G52 1RZ",
            "G53 6UW",
            "G61 1QE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if "LINTHAUGH NURSERY" in record.pollingstationname:
            record = record._replace(
                pollingstationpostcode=record.pollingstationaddress_5
            )
            record = record._replace(pollingstationaddress_5="")

        if "ST MARGARETS PARISH CHURCH HALL" in record.pollingstationname:
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)

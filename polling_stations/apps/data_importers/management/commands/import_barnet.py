from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = "2022-05-05/2022-03-10T12:42:22.195442/Barnet_PDs_Data_220505.csv"
    stations_name = (
        "2022-05-05/2022-03-10T12:42:22.195442/Barnet_PollStations_Data_220505.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.postcode.strip() in [
            "NW11 7ND",
        ]:
            return None
        return super().address_record_to_dict(record)

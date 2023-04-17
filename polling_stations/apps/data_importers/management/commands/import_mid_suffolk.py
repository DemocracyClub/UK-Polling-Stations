from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "MSU"
    addresses_name = (
        "2023-05-04/2023-04-17T14:43:48.331284/DC Polling Districts - Mid Suffolk.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-17T14:43:48.331284/DC Polling Stations - Mid Suffolk.csv"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # correction from council
        if record.stationcode in [
            "M49",  # Wetheringsett Village Hall
            "M84",  # All Saints Church Beyton
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "IP14 5PE",
            "IP14 1LU",
            "IP14 5LN",
            "IP14 6ET",
            # look wrong
            "IP14 4FW",
        ]:
            return None
        if record.uprn in [
            "10095542589",  # THE PIGGERY, BROAD VIEW FARM, LOWER FARM ROAD, RINGSHALL, STOWMARKET
        ]:
            return None
        return super().address_record_to_dict(record)

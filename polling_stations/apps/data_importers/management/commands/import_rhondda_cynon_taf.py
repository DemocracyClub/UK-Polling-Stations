from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = (
        "2022-11-17/2022-11-03T10:02:02.538154/polling_station_export-2022-11-03.csv"
    )
    stations_name = (
        "2022-11-17/2022-11-03T10:02:02.538154/polling_station_export-2022-11-03.csv"
    )
    elections = ["2022-11-17"]

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "124":
            # ST DAVIDS CHURCH, LLANTRISANT ROAD, GROESFAEN, PONTYCLUN
            # "CF72 8NU" → "CF72 8NS"
            # Source: https://www.churchinwales.org.uk/en/structure/church/4123/
            record = record._replace(pollingstationpostcode="CF72 8NS")

        if record.pollingstationnumber == "97":
            #     # CILFYNYDD & NORTON BRIDGE COMMUNITY CENTRE, CILFYNYDD ROAD, …
            #     # Was "CF37 3NR", but that's not on Cilfyndd Road
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CF37 3BS",
            "CF37 1TG",
            "CF39 8FA",
            "CF38 1DR",
            "CF37 1LD",
            "CF44 9DT",
            "CF38 2HH",
            "CF37 4DX",
            "CF38 2JF",
            "CF37 3EW",
            "CF42 6LX",
            "CF42 6BH",
            "CF40 2SN",
            "CF38 2JZ",
            "CF40 2ER",
            "CF38 2SA",
            "CF44 0PD",
            "CF39 8AT",
            "CF44 9TB",
            "CF72 9JZ",
            "CF37 1UA",
        ]:
            return None

        if record.uprn in [
            "10001300469",
            "10094101040",
        ]:
            return None

        return super().address_record_to_dict(record)

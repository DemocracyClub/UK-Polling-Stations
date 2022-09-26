from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = (
        "2022-09-29/2022-09-26T11:41:22.544794/polling_station_export-2022-09-26.csv"
    )
    stations_name = (
        "2022-09-29/2022-09-26T11:41:22.544794/polling_station_export-2022-09-26.csv"
    )
    elections = ["2022-09-29"]

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
            "CF37 1LD",
            "CF44 9TB",
            "CF37 3BS",
            "CF44 0PD",
            "CF38 1DR",
            "CF37 3EW",
            "CF38 2SA",
            "CF38 2HH",
            "CF39 8FA",
            "CF40 2SN",
            "CF40 2ER",
            "CF38 2JF",
            "CF37 1TG",
            "CF42 6BH",
            "CF44 9BP",
            "CF72 9JZ",
            "CF39 8AT",
            "CF38 2JZ",
            "CF37 1UA",
            "CF37 4DX",
            "CF42 6LX",
            "CF44 9DT",
        ]:
            return None

        return super().address_record_to_dict(record)

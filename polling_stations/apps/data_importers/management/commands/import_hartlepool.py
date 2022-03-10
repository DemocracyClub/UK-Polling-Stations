from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HPL"
    addresses_name = "2022-05-05/2022-03-31T11:14:18.050665/Polling Station Finder 05 May 2022 NEW.tsv"
    stations_name = "2022-05-05/2022-03-31T11:14:18.050665/Polling Station Finder 05 May 2022 NEW.tsv"
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100110020667",
            "10090069600",
            "10090070990",
            "100110786581",
            "100110673984",
            "10090073016",
        ]:
            return None

        if record.addressline6 in [
            "TS24 9BD",
            "TS24 8DD",
            "TS25 5BF",
            "TS24 9SF",
            "TS25 4PE",
            "TS26 0LA",
            "TS25 5QB",
            "TS25 5DY",
            "TS24 8PR",
            "TS26 0EE",
        ]:
            return None

        return super().address_record_to_dict(record)

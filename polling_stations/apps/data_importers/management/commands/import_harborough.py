from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAO"
    addresses_name = "2021-04-22T15:54:24.242348/Harborough.tsv"
    stations_name = "2021-04-22T15:54:24.242348/Harborough.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "5849":
            # Billesdon Coplow Centre
            # https://www.thecoplowcentre.com/contact-us/
            record = record._replace(polling_place_postcode="LE7 9FL")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["200001042689", "200001043348", "10093551160"]:
            return None

        if record.addressline6 in [
            "LE17 4BN",
            "LE16 9HY",
            "LE16 9HD",
            "LE17 5LE",
            "LE9 6PU",
            "LE16 9FG",
            "LE7 9WB",
            "LE17 5EA",
            "LE16 7AX",
            "LE17 6AX",
        ]:
            return None  # split

        if record.addressline6 in ["LE7 9EL"]:
            return None  # suspect

        return super().address_record_to_dict(record)

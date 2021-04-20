from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHS"
    addresses_name = "2021-04-01T14:48:16.336851/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-01T14:48:16.336851/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["S43 1ER", "S40 3LA", "S41 9RL"]:
            return None

        if uprn in ["74085483"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Manor Centre Manor Road Brimington Chesterfield
        if record.polling_place_id == "6217":
            record = record._replace(polling_place_postcode="")
        return super().station_record_to_dict(record)

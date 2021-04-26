from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROH"
    addresses_name = "2021-04-16T13:52:31.124456/Rother Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-16T13:52:31.124456/Rother Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.addressline6 in ["TN31 6BG"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Georges Church Parish Room, Crowhurst
        if record.polling_place_id == "1416":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

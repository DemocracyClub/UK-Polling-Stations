from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHA"
    addresses_name = "2021-04-07T11:42:17.260342/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-07T11:42:17.260342/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # St Gregory's Social Centre
        if record.polling_place_id == "8532":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in ["10070073939"]:
            return None
        if record.addressline6 in ["LE11 1RZ", "LE11 2HH"]:
            return None
        return super().address_record_to_dict(record)

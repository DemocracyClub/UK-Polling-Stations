from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLV"
    addresses_name = (
        "2022-05-05/2022-03-24T13:26:30.475155/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T13:26:30.475155/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # St Joseph`s Church Hall, Coalway Road, Wolverhampton
        if record.polling_place_id == "29400":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100071373072",
            "10007123304",
            "10093323695",
            "10093323696",
            "10093325431",
            "10090013969",
            "10090642339",
            "10090643975",
            "100071556719",
        ]:
            return None

        if record.addressline6 in []:
            return None

        return super().address_record_to_dict(record)

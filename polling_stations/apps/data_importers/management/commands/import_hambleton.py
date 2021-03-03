from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAE"
    addresses_name = "2021-03-02T16:29:16.566032/Democracy_Club__06May2021 Hambleton District Council.tsv"
    stations_name = "2021-03-02T16:29:16.566032/Democracy_Club__06May2021 Hambleton District Council.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003295948",  # CHAPPEL VIEW PONY STUD, TUNSTALL LANE, NUNTHORPE, MIDDLESBROUGH
        ]:
            return None

        if record.addressline6 in ["YO7 3NG", "DL7 8DA"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "8653"
        ):  # Thirkleby Parish Hall Great Thirkleby Thirsk - https://trello.com/c/uAHT7T8d/330-hambleton
            record = record._replace(polling_place_postcode="YO7 2AT")

        return super().station_record_to_dict(record)

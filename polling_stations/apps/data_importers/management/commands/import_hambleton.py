from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAE"
    addresses_name = "2022-05-05/2022-04-08T13:47:40.261523/Hambleton District Council 3.3.22 Democracy_Club__05May2022.tsv"
    stations_name = "2022-05-05/2022-04-08T13:47:40.261523/Hambleton District Council 3.3.22 Democracy_Club__05May2022.tsv"
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200003295948",  # CHAPPEL VIEW PONY STUD, TUNSTALL LANE, NUNTHORPE, MIDDLESBROUGH
            ]
        ):
            return None

        if record.addressline6 in ["DL7 8DA", "YO7 2BR", "YO7 3NG", "YO61 3GT"]:
            return None

        return super().address_record_to_dict(record)

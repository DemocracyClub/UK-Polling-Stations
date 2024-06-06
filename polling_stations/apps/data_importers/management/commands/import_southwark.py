from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWK"
    addresses_name = (
        "2024-07-04/2024-06-06T12:15:04.024597/Democracy_Club__04July2024_Southwark.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T12:15:04.024597/Democracy_Club__04July2024_Southwark.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.addressline6 in [
            # split
            "SE16 6AZ",
            "SE5 0SY",
            "SE15 6BJ",
            "SE5 7HY",
            # suspect:
            "SE24 9JQ",
        ]:
            return None
        return super().address_record_to_dict(record)

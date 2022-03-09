from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWK"
    addresses_name = (
        "2022-05-05/2022-03-09T13:17:31.002506/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-09T13:17:31.002506/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003451291",  # ST. FAITHS VICARAGE, 62 RED POST HILL, LONDON
            "200003394858",  # 17 LYNDHURST WAY, LONDON
            "10090283768",  # KILIMANJARO LIVE LTD, SECOND FLOOR NORTH 15 BERMONDSEY SQUARE, LONDON
            "200003468937",  # GROUNDSMANS COTTAGE COLLEGE ROAD, LONDON
            "10091665680",  # 23 CAMBERWELL GROVE, LONDON
        ]:
            return None

        if record.addressline6 in [
            "SE1 3UL",
            "SE16 6AZ",
            "SE15 6BJ",
            "SE16 2QU",
            "SE1 2PS",
            "SE5 0SY",
            "SE15 3DN",
            "SE5 7HY",
            "SE1 2AD",
            "SE15 2ND",
            "SE1 0AA",
        ]:
            return None

        if record.addressline1 == "Excluding Third Floor and Fourth Floor":
            return None

        return super().address_record_to_dict(record)

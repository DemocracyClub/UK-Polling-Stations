from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLI"
    addresses_name = (
        "2021-04-16T11:36:59.020893/West Lindsay Democracy_Club__06May2021 (1).CSV"
    )
    stations_name = (
        "2021-04-16T11:36:59.020893/West Lindsay Democracy_Club__06May2021 (1).CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090698579",  # HORSESHOE BARN, LISSINGLEY LANE, LISSINGTON, LINCOLN
            "10090696854",  # HORIZON BARN, BULLY HILL TOP, TEALBY, MARKET RASEN
            "10013812180",  # 1 NETTLETON PARK MOORTOWN ROAD, NETTLETON, MARKET RASEN
        ]:
            return None

        if record.addressline6 in [
            "LN7 6JD",
            "LN1 2XG",
            "LN1 2PL",
            "LN2 2YX",
            "LN8 3SF",
            "LN2 3PD",
            "LN2 3RS",
            "DN21 2PL",
        ]:
            return None

        return super().address_record_to_dict(record)

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIL"
    addresses_name = "2024-07-04/2024-06-26T11:51:48.005266/WIL_combined.tsv"
    stations_name = "2024-07-04/2024-06-26T11:51:48.005266/WIL_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10094306546",  # MAREEBA, CARISBROOKE STUD, WEST SOLEY, CHILTON FOLIAT, HUNGERFORD
                "100121330656",  # 77 BOURNE AVENUE, SALISBURY
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "SP5 1RN",
            "SP3 6DY",
            "SN10 4AD",
            "SP5 2NL",
            "SN10 2PA",
            "SN8 1HG",
            "SN8 1QB",
            "BA12 7JH",
            "SN14 6HT",
            # suspect
            "BA14 8RA",
            "SN15 4EU",
            "SN15 4EX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: King Georges Hall, West Dean, Salisbury, SP5 1JA
        # slight correction to remove warning: Polling station King Georges Hall (87349) is in Test Valley Borough Council (TES)
        if record.polling_place_id == "87349":
            record = record._replace(polling_place_easting="425660")
            record = record._replace(polling_place_northing="127118")

        return super().station_record_to_dict(record)

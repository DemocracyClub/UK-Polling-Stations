from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = "2024-07-04/2024-05-30T15:37:51.177065/BCPCouncil_Democracy_Club__04July2024.tsv"
    stations_name = "2024-07-04/2024-05-30T15:37:51.177065/BCPCouncil_Democracy_Club__04July2024.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "BH1 1NF",
            "BH1 3EB",
            "BH11 8BA",
            "BH7 6LL",
            "BH1 1NF",
            "BH5 1DL",
            "BH14 9HF",
            "BH6 3NH",
            "BH23 3JJ",
            "BH6 3LF",
            "BH10 5JF",
            "BH14 0RD",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # removing postcodes until council responds for Station A and B at:
        # St. George`s Church Hall (Oakdale), Darby`s Lane, (entrance at junction with Johnston Road), Oakdale, Poole
        if record.polling_place_id in [
            "17399",
            "17425",
        ]:
            record = record._replace(polling_place_postcode="BH15 3EU")

        # coord correction from council for:
        # Station C - Immanuel Church, 120 Southbourne Road, Bournemouth
        if record.polling_place_id == "17445":
            record = record._replace(
                polling_place_easting="413613", polling_place_northing="91759"
            )

        # bug report 672: removing station map until council responds for:
        # Station B - The Annexe at St John`s Church, Dunyeats Road, Broadstone BH18 8AQ
        # suggested coords:
        # northing: 95825.15,
        # easting: 400560.37
        if record.polling_place_id in [
            "17528",
            "17526",
        ]:
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
                polling_place_uprn="",
            )

        return super().station_record_to_dict(record)

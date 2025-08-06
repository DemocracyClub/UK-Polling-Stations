from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = (
        "2024-10-24/2024-09-23T11:24:09.822906/Democracy_Club__24October2024.tsv"
    )
    stations_name = (
        "2024-10-24/2024-09-23T11:24:09.822906/Democracy_Club__24October2024.tsv"
    )
    elections = ["2024-10-24"]
    csv_delimiter = "\t"

    # These exclusions aren't relevant for the by-election but I'm maintaining them as a comment for future reference
    # comment to deploy

    # def address_record_to_dict(self, record):
    #     if record.addressline6 in [
    #         # split
    #         "BH1 1NF",
    #         "BH1 3EB",
    #         "BH11 8BA",
    #         "BH7 6LL",
    #         "BH1 1NF",
    #         "BH5 1DL",
    #         "BH14 9HF",
    #         "BH6 3NH",
    #         "BH23 3JJ",
    #         "BH6 3LF",
    #         "BH10 5JF",
    #         "BH14 0RD",
    #     ]:
    #         return None
    #     return super().address_record_to_dict(record)

    # def station_record_to_dict(self, record):
    #     # postcode correction from council for:
    #     # St. George`s Church Hall (Oakdale), Darby`s Lane, (entrance at junction with Johnston Road), Oakdale, Poole
    #     if record.polling_place_id in [
    #         "17399",
    #         "17425",
    #     ]:
    #         record = record._replace(polling_place_postcode="BH15 3EU")

    #     # coord correction from council for:
    #     # Station C - Immanuel Church, 120 Southbourne Road, Bournemouth
    #     if record.polling_place_id == "17445":
    #         record = record._replace(
    #             polling_place_easting="413613", polling_place_northing="91759"
    #         )

    #     # bug report 672:
    #     # coord correction from council for stations A and B at:
    #     # The Annexe at St John`s Church, Dunyeats Road, Broadstone BH18 8AQ
    #     if record.polling_place_id in [
    #         "17528",
    #         "17526",
    #     ]:
    #         record = record._replace(
    #             polling_place_easting="400556",
    #             polling_place_northing="95824",
    #         )

    #     return super().station_record_to_dict(record)

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIL"
    addresses_name = "2026-10-15/2026-09-21T12:49:38.409661/EC_&_Democracy_Club_PollingPlace_Lookup__15October2026.tsv"
    stations_name = "2026-10-15/2026-09-21T12:49:38.409661/EC_&_Democracy_Club_PollingPlace_Lookup__15October2026.tsv"
    elections = ["2026-10-15"]
    csv_delimiter = "\t"

    # maintaining tweaks as comments through by-election

    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if uprn in [
    #         # "100121330656",  # 77 BOURNE AVENUE, SALISBURY
    #     ]:
    #         return None

    #     if record.addressline6 in [
    #         # split
    #         # "SN10 4AD",
    #         # "SP3 6DY",
    #         # "SP5 2NL",
    #         # "SN10 2PA",
    #         # "SP11 9UX",
    #         # "SN14 6HT",
    #         # "SN8 1HG",
    #         # suspect
    #         # "BA14 8RA",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)

    # def station_record_to_dict(self, record):
    #     # more accurate point for: King Georges Hall, West Dean, Salisbury, SP5 1JA
    #     # slight correction to remove warning: Polling station King Georges Hall (87349) is in Test Valley Borough Council (TES)
    #     if record.polling_place_id == "92351":
    #         record = record._replace(polling_place_easting="425660")
    #         record = record._replace(polling_place_northing="127118")

    #     return super().station_record_to_dict(record)

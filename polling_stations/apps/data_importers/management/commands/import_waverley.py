from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WAE"
    addresses_name = (
        "2026-07-07/2026-06-08T15:28:11.723541/Democracy_Club__07July2026.tsv"
    )
    stations_name = (
        "2026-07-07/2026-06-08T15:28:11.723541/Democracy_Club__07July2026.tsv"
    )
    elections = ["2026-07-07"]
    csv_delimiter = "\t"

    # Maintaining exclusions as comments through a by-election
    # def station_record_to_dict(self, record):
    #     # UPRN from council for:
    #     # Busbridge Village Hall Brighton Road Godalming, GU7 1XA
    #     if record.polling_place_id == "7358":
    #         record = record._replace(polling_place_uprn="100062609703")

    #     return super().station_record_to_dict(record)

    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if uprn in [
    #         "100061602142",  # 3 FARNBOROUGH ROAD, FARNHAM
    #         "10096746074",  # FLAT 1, GAINSBOROUGH HOUSE, 204 HIGH STREET, CRANLEIGH
    #         "10096746075",  # FLAT 2, GAINSBOROUGH HOUSE, 204 HIGH STREET, CRANLEIGH
    #         "100061616831",  # KENNELS COTTAGE, HASLEMERE ROAD, WITLEY, GODALMING
    #     ]:
    #         return None

    #     if record.addressline6 in [
    #         "GU9 0NZ",  # split
    #         "RH12 3BQ",  # looks wrong
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)

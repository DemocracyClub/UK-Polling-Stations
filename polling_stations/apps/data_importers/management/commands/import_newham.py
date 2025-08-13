from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = (
        "2025-09-18/2025-08-13T15:03:02.928157/Democracy_Club__18September2025.tsv"
    )
    stations_name = (
        "2025-09-18/2025-08-13T15:03:02.928157/Democracy_Club__18September2025.tsv"
    )
    elections = ["2025-09-18"]
    csv_delimiter = "\t"

    # by-election so maintaining previous exclusions as comments

    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "10023995039",  # FLAT AT THE DOCKLANDS EQUESTRIAN CENTRE 2 CLAPS GATE LANE, BECKTON, LONDON
    #             "10094880629",  # FLAT 1 200 THE GROVE, STRATFORD, LONDON
    #             "10009003474",  # FLAT 2 200 THE GROVE, STRATFORD, LONDON
    #             "10009003475",  # FLAT 3 200 THE GROVE, STRATFORD, LONDON
    #             "46001049",  # 96 ALDERSBROOK ROAD, LONDON
    #             "10012838007",  # FLAT ABOVE 24 STEPHENSON STREET, CANNING TOWN, LONDON
    #             "10012838012",  # FLAT, 162 BIDDER STREET, LONDON
    #             "10093472922",  # ALAIN CODY DOCK 11C SOUTH CRESCENT, CANNING TOWN, LONDON
    #             "10093472923",  # MADORCHA CODY DOCK 11C SOUTH CRESCENT, CANNING TOWN, LONDON
    #         ]
    #     ):
    #         return None

    #     if record.addressline6 in [
    #         # split
    #         "E13 0DZ",
    #         # looks wrong
    #         "E15 1BQ",
    #         "E15 1BG",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)

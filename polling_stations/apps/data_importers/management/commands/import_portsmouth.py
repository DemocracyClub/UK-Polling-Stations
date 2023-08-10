from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "POR"
    addresses_name = (
        "2023-05-04/2023-03-13T12:41:54.727276/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T12:41:54.727276/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "1775074578",  # FLAT 1 SOUTHAMPTON ROAD, PORTSMOUTH
            "1775023088",  # FLAT GREAT SALTERNS MANSION EASTERN ROAD, PORTSMOUTH
            "1775078355",  # 264 TANGIER ROAD, PORTSMOUTH
            "1775097409",  # FLAT LAWNSWOOD 245 FRATTON ROAD, PORTSMOUTH
            "1775064482",  # 40 PERONNE ROAD, PORTSMOUTH
            "1775081845",  # 115 VICTORIA ROAD SOUTH, SOUTHSEA
            "1775129057",  # ADMIRAL JELLICOE HOUSE, LOCKSWAY ROAD, SOUTHSEA
        ]:
            return None

        if record.addressline6 in [
            "PO6 4SB",  # SOUTHAMPTON ROAD, PORTSMOUTH
            "PO6 3LX",  # POLICE RESIDENCES, SOUTHWICK ROAD, COSHAM, PORTSMOUTH
            "PO3 5NB",  # FLAT 1-3, BUILDBASE, BURRFIELDS ROAD, PORTSMOUTH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Import warnings, but no correction needed:

        # Church of the Ascension, Stubbington Avenue, Portsmouth, PO2 0JG
        # Howard Road Community Centre, Howard Road, Portsmouth, PO2 9PS
        # Portacabin on north side of green, Fairfield Square/Hythe Road, Portsmouth, PO6 3JS
        # St Peter & St Paul Hall, Old Wymering Lane, Wymering, PO6 3NH

        return super().station_record_to_dict(record)

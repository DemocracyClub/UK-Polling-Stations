from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "POR"
    addresses_name = (
        "2024-05-02/2024-02-23T14:57:35.343217/DemocracyClub__02May2024.tsv"
    )
    stations_name = "2024-05-02/2024-02-23T14:57:35.343217/DemocracyClub__02May2024.tsv"
    elections = ["2024-05-02"]
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
            "1775044838",  # 153 KIRBY ROAD, PORTSMOUTH
            "1775030023",  # ST, MARYS VICARAGE, FRATTON ROAD, PORTSMOUTH
            "1775016273",  # FLAT, 146 COMMERCIAL ROAD, PORTSMOUTH
            "1775020413",  # 37 DELAMERE ROAD, SOUTHSEA
            "1775117109",  # MANOR HOUSE, MANNERS ROAD, SOUTHSEA
            "1775122433",  # 1A MANNERS ROAD, SOUTHSEA
            "1775122434",  # 1B MANNERS ROAD, SOUTHSEA
            "1775091957",  # 2A ST, EDWARDS ROAD, SOUTHSEA
            "1775068980",  # MILL COTTAGE, RICHMOND ROAD, SOUTHSEA
            "1775082102",  # 21 VILLIERS ROAD, SOUTHSEA
            "1775094668",  # 8 HAMILTON ROAD, SOUTHSEA
            "1775034486",  # 20 HAMILTON ROAD, SOUTHSEA
            "1775034488",  # 22 HAMILTON ROAD, SOUTHSEA
            "1775034484",  # 18 HAMILTON ROAD, SOUTHSEA
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "PO6 4SB",
            "PO6 3LX",
            "PO3 5NB",
            "PO4 9JF",
            "PO5 2HH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Import warnings, but no correction needed (checked with the council):
        # Portsmouth Methodist Church (Eastney), Highland Road, Southsea, PO4 9NJ
        # John Pounds Centre, Queen Street, Portsmouth, PO1 3HN
        # Highslopes Community Centre (6235) is in Fareham Borough Council (FAR) but target council is Portsmouth City Council (POR)
        # St Peter & St Paul Hall, Old Wymering Lane, Wymering, PO6 3NH
        # Portacabin on north side of green, Fairfield Square/Hythe Road, Portsmouth, PO6 3JS

        # postcode correction for: Church of the Ascension, Stubbington Avenue, Portsmouth, PO2 0JG
        if record.polling_place_id == "6210":
            record = record._replace(polling_place_postcode="PO2 0JW")

        return super().station_record_to_dict(record)

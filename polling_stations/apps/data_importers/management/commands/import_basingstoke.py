from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAN"
    addresses_name = (
        "2024-05-02/2024-03-20T17:06:06.547142/Democracy_Club__02May2024.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-20T17:06:06.547142/Democracy_Club__02May2024.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000454945",  # THE FIRS, ALTON ROAD, WINSLADE, BASINGSTOKE
            "10008484054",  # 4A CUMBERLAND AVENUE, BASINGSTOKE
            "10008483447",  # ANNEXE 47 HANDEL CLOSE, BASINGSTOKE
            "10002922516",  # TWIGGYS FARM, PRIORY LANE, FREEFOLK, WHITCHURCH
            "10002234155",  # VITACRESS LTD, LOWER LINK FARM, LOWER LINK, ST. MARY BOURNE, ANDOVER
            "10001320643",  # KEEPERS COTTAGE, CRUX EASTON, NEWBURY
            "10002235910",  # DALESWOOD, OLD CHAPEL LANE, CHARTER ALLEY, TADLEY
            "10008497900",  # 5A WOOLFORD WAY, BASINGSTOKE
            "10008488752",  # 5A BALLARD CLOSE, BASINGSTOKE
            "10008507412",  # 57 HACKWOOD ROAD, BASINGSTOKE
            "10002464346",  # 28 PYOTTS HILL, OLD BASING, BASINGSTOKE
            "10008508107",  # 18 DORIC AVENUE, CHINEHAM, BASINGSTOKE
            "10002463446",  # BRADLEY WOOD FARMHOUSE, DUNLEY, WHITCHURCH
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "RG22 6TD",
            "RG24 8BF",
        ]:
            return None

        return super().address_record_to_dict(record)

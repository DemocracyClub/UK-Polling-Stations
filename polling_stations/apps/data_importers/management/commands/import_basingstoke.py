from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAN"
    addresses_name = (
        "2024-07-04/2024-06-11T16:47:36.897190/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-11T16:47:36.897190/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
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
                "100062459154",  # 24 LYTTON ROAD, BASINGSTOKE
                "100062459180",  # 22 LYTTON ROAD, BASINGSTOKE
            ]
        ):
            return None

        if record.addressline6 in [
            # looks wrong
            "RG22 6TD",
            "RG24 8BF",
        ]:
            return None

        return super().address_record_to_dict(record)

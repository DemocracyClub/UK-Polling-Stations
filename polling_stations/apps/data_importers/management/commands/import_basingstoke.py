from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAN"
    addresses_name = (
        "2026-05-07/2026-02-23T16:00:35.540853/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-23T16:00:35.540853/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100060227884",  # 51 HACKWOOD ROAD, BASINGSTOKE, RG21 3AE
                "100060240556",  # 4 RECTORY ROAD, OAKLEY, BASINGSTOKE, RG23 7LJ
                "100060223134",  # HARROWSIDE, THE HARROW WAY, BASINGSTOKE, RG22 4BE
                "10000453008",  # CHOLMLEY LODGE, THE HARROW WAY, BASINGSTOKE, RG22 4BE
                "10000454945",  # THE FIRS, ALTON ROAD, WINSLADE, BASINGSTOKE
                "10002922516",  # TWIGGYS FARM, PRIORY LANE, FREEFOLK, WHITCHURCH
                "10002234155",  # VITACRESS LTD, LOWER LINK FARM, LOWER LINK, ST. MARY BOURNE, ANDOVER
                "10001320643",  # KEEPERS COTTAGE, CRUX EASTON, NEWBURY
                "10002235910",  # DALESWOOD, OLD CHAPEL LANE, CHARTER ALLEY, TADLEY
                "10008507412",  # 57 HACKWOOD ROAD, BASINGSTOKE
                "10002464346",  # 28 PYOTTS HILL, OLD BASING, BASINGSTOKE
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
            "RG20 5PS",
            "RG22 5EJ",
        ]:
            return None

        return super().address_record_to_dict(record)

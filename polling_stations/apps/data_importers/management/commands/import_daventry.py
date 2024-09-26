from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAV"
    addresses_name = "2021-03-15T10:49:02.246508/Daventry Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-15T10:49:02.246508/Daventry Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "28061582",  # NEW LEAF FARM, CHURCH STREET, BYFIELD, DAVENTRY
                "28048536",  # WESTCOMBE FARM, FAWSLEY, DAVENTRY
                "28047695",  # WESTCOMBE HOUSE, FAWSLEY, DAVENTRY
                "28042479",  # CARAVAN CHARWELTON LODGE GRANTS HILL WAY, WOODFORD HALSE
                "28056692",  # KINGSTON LODGE, WHILTON LOCKS, WHILTON, DAVENTRY
                "28032128",  # CARETAKERS FLAT LANDMARK HOTEL AND CONFERENCE CENTRE LONDON ROAD, DAVENTRY
                "28022982",  # 3 NEWBOLD FARM CLIPSTON ROAD, CLIPSTON
                "28060573",  # 2 NEWBOLD FARM CLIPSTON ROAD, CLIPSTON
                "28057900",  # ROSE COTTAGE MOULTON GRANGE FARM GRANGE LANE, PITSFORD
                "28044367",  # THE PORTACABIN NORTHAMPTON ROAD, COLD ASHBY
                "28044366",  # SEDGEBROOK HOUSE, PITSFORD ROAD, CHAPEL BRAMPTON, NORTHAMPTON
                "28028615",  # DERWENT, KELMARSH ROAD, CLIPSTON, MARKET HARBOROUGH
            ]
        ):
            return None

        if record.addressline6 in [
            "NN11 6XA",
            "NN6 6DG",
            "NN11 0GL",
            "NN6 6HY",
            "NN11 2ND",
            "NN3 7DW",
            "NN3 7AU",
        ]:
            return None

        return super().address_record_to_dict(record)

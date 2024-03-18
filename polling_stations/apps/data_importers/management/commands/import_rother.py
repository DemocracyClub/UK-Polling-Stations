from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROH"
    addresses_name = (
        "2024-05-02/2024-03-18T15:59:53.401843/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-18T15:59:53.401843/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002667898",  # MEAD COTTAGE, CROWHURST ROAD, CATSFIELD, BATTLE
            "10002656457",  # THE CARAVAN, THREE GATES FARM, PASHLEY ROAD, TICEHURST, WADHURST
            "10002651849",  # THREE GATES FARM, PASHLEY ROAD, TICEHURST, WADHURST
            "10002668563",  # HOME FARM BARN, ETCHINGHAM
            "100060097122",  # BOARZWOOD, LONDON ROAD, HURST GREEN, ETCHINGHAM
            "100062553811",  # BOARSDEN, LONDON ROAD, HURST GREEN, ETCHINGHAM
            "100061937222",  # BOUNDARY FARM, LONDON ROAD, HURST GREEN, ETCHINGHAM
            "10002651836",  # LUDPIT COTTAGE, LUDPIT LANE, ETCHINGHAM
            "10002668412",  # COWFIELD COTTAGE, BODIAM, ROBERTSBRIDGE
            "10090508857",  # 2 OCKHAM MEWS, BODIAM, ROBERTSBRIDGE
            "10090507447",  # 1 OCKHAM MEWS, BODIAM, ROBERTSBRIDGE
            "10002662323",  # DYKES FARM, EWHURST GREEN, ROBERTSBRIDGE
            "100060089232",  # 49 ELLERSLIE LANE, BEXHILL-ON-SEA
            "100062584403",  # HIGHWOODS GOLF CLUB LTD, 47 ELLERSLIE LANE, BEXHILL-ON-SEA
        ]:
            return None

        return super().address_record_to_dict(record)

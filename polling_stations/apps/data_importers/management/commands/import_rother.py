from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROH"
    addresses_name = (
        "2023-05-04/2023-03-15T15:43:21.335525/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-15T15:43:21.335525/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002667898",  # MEAD COTTAGE, CROWHURST ROAD, CATSFIELD, BATTLE
            "10002656457",  # THE CARAVAN, THREE GATES FARM, PASHLEY ROAD, TICEHURST, WADHURST
            "10002651849",  # THREE GATES FARM, PASHLEY ROAD, TICEHURST, WADHURST
            "10002668563",  # HOME FARM BARN, ETCHINGHAM
            "10002660230",  # THE PUMP HOUSE, BREADSELL LANE, ST. LEONARDS-ON-SEA
            "100060097122",  # BOARZWOOD, LONDON ROAD, HURST GREEN, ETCHINGHAM
            "100062553811",  # BOARSDEN, LONDON ROAD, HURST GREEN, ETCHINGHAM
            "100061937222",  # BOUNDARY FARM, LONDON ROAD, HURST GREEN, ETCHINGHAM
            "10002651836",  # LUDPIT COTTAGE, LUDPIT LANE, ETCHINGHAM
            "100062569487",  # KEEPERS COTTAGE, BRIGHTLING ROAD, ROBERTSBRIDGE
        ]:
            return None

        if record.addressline6 in [
            "TN32 5RA",  # BODIAM, ROBERTSBRIDGE
        ]:
            return None

        return super().address_record_to_dict(record)

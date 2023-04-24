from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KWL"
    addresses_name = (
        "2023-05-04/2023-04-12T12:21:05.053431/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-12T12:21:05.053431/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "40035578",  # 182 RIBBLERS LANE, LIVERPOOL
            "40035577",  # 180 RIBBLERS LANE, LIVERPOOL
            "40003719",  # 121 BEWLEY DRIVE, SOUTHDENE, KIRKBY
            "40036487",  # 134 ROUGHWOOD DRIVE, LIVERPOOL
            "40025501",  # FOREST HOUSE, LIVERPOOL ROAD, PRESCOT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L34 1LP",
            "L36 5YR",
            "L35 1QN",
            "L35 5AW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Stockbridge Village Neighbourhood Centre, The Withens, Stockbridge Village, Knowsley, Merseyside, L28 1SU
        # Proposed postcode correction: L28 1AB
        if record.polling_place_id == "5142":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KWL"
    addresses_name = (
        "2024-05-02/2024-03-04T15:30:34.030306/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-04T15:30:34.030306/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "40035578",  # 182 RIBBLERS LANE, LIVERPOOL
            "40035577",  # 180 RIBBLERS LANE, LIVERPOOL
            "40003719",  # 121 BEWLEY DRIVE, SOUTHDENE, KIRKBY
            "40036487",  # 134 ROUGHWOOD DRIVE, LIVERPOOL
            "40025501",  # FOREST HOUSE, LIVERPOOL ROAD, PRESCOT
            "40048270",  # 10 CHURCH STREET, PRESCOT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L36 5YR",
            "L34 1LP",
            "L35 1QN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Stockbridge Village Neighbourhood Centre, The Withens, Stockbridge Village, Knowsley, Merseyside, L28 1SU
        if record.polling_place_id == "5789":
            record = record._replace(polling_place_postcode="L28 1AB")

        return super().station_record_to_dict(record)

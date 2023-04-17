from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAB"
    addresses_name = (
        "2023-05-04/2023-04-17T14:44:03.233285/DC Polling Districts Babergh.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-17T14:44:03.233285/DC Polling Stations Babergh.csv"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # correction from council
        if record.stationcode in [
            "B13",  # Polstead Village Hall
            "B17",  #  Nayland Village Hall
            "B70",  # Pinewood - Belstead Brook Muthu Hotel
            "B31",  # Fields Farmshop and Cafe
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "CO10 9LN",
            "CO10 9AQ",
            # look wrong
            "CO10 2PQ",
        ]:
            return None
        if record.uprn in [
            "10094142009",  # GREYCOTE RODBRIDGE HILL, LONG MELFORD
            "10093344109",  # 25 WAKELIN CLOSE, GREAT CORNARD, SUDBURY
            "10033308582",  # 37B WALNUT TREE LANE, SUDBURY
            "100091457209",  # KINGSBURY HOUSE, UPPER ROAD, LITTLE CORNARD, SUDBURY
            "10094140064",  # ELM VIEW, STONE STREET, HADLEIGH, IPSWICH
        ]:
            return None
        return super().address_record_to_dict(record)

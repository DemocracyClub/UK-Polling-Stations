from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNO"
    addresses_name = "2021-03-25T13:58:54.180597/Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-25T13:58:54.180597/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034791449",  # THE CEDARS, GRESHAM, NORWICH
            "10023665747",  # CHALET 4 MILL FARM AYLSHAM ROAD, FELMINGHAM
            "10034812867",  # BURROW COTTAGE AT WARREN BARN BREWERY ROAD, TRUNCH
            "10034807115",  # 6 SEAWARD CREST, LINKS ROAD, MUNDESLEY, NORWICH
            "10034818211",  # GARDEN COTTAGE, HOVETON HALL ESTATE, HOVETON, NORWICH
            "10034819670",  # THE OLD GATEHOUSE, WALSINGHAM ROAD, EAST BARSHAM, FAKENHAM
            "100091325096",  # FLAT 6 7 NORWICH ROAD, CROMER
        ]:
            return None

        if record.addressline6 in ["NR12 0RX", "NR11 7PE", "NR12 8AH", "NR12 0UD"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "17025",  # Walsingham Village Hall Wells Road Walsingham NR23 1RX
            "17003",  # Great Snoring Social Club Walsingham Road Great Snoring Fakenham NR21 0AP
            "16607",  # The Preston Room Neatishead Road Ashmanhaugh Wroxham NR12 8LB
        ]:
            record = record._replace(polling_place_postcode="")

        # Walcott Village Hall Coast Road Walcott NR12 ONG - O => 0
        if record.polling_place_id == "16728":
            record = record._replace(polling_place_postcode="NR12 0NG")

        return super().station_record_to_dict(record)

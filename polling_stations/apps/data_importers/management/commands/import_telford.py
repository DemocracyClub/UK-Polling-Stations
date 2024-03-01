from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TFW"
    addresses_name = (
        "2024-05-02/2024-03-01T11:51:31.642592/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-01T11:51:31.642592/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "452098161",  # AQUALATE MANOR, STAFFORD ROAD, NEWPORT
            "200001754669",  # CHARTLEY, CHURCH ASTON, NEWPORT
            "452098134",  # CARAVAN 3 GREENFIELDS COUNTRY STORE STATION ROAD, DONNINGTON, TELFORD
            "452063031",  # HOMECROFT, ADMASTON, TELFORD
            "452084193",  # MEESE COTTAGE, HOWLE, NEWPORT
            "452063475",  # 10 RUSHMOOR LANE, BRATTON, TELFORD
            "452094687",  # THE RIDGEWAYS, THE HEM, SHIFNAL
            "452044353",  # 12 WATERLOO ROAD, EDGMOND, NEWPORT
            "10090446309",  # LAKE VIEW RESIDENTIAL CARE HOME, BROOKSIDE AVENUE, TELFORD
            "452005400",  # 2 POOL HILL, DAWLEY, TELFORD
            "452005403",  # 5 POOL HILL, DAWLEY, TELFORD
            "452043117",  # INGLESIDE, EDGMOND ROAD, NEWPORT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TF10 7ZN",
            "TF10 7RG",
            "TF4 3JZ",
            "TF2 8SF",
            "TF4 3AZ",
            "TF2 9HF",
            "TF8 7NN",
            # looks wrong
            "TF3 4LY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Donnington Community Hub, St Matthews Road, Donnington Wood, Telford, Shropshire, TF2 7RB
        if record.polling_place_id == "8782":
            record = record._replace(polling_place_easting="370966")
            record = record._replace(polling_place_northing="312997")

        # more accurate point for: Horsehay Village Golf Club, Wellington Road, Horsehay, Telford, TF4 3BT
        if record.polling_place_id == "8933":
            record = record._replace(polling_place_easting="366836")
            record = record._replace(polling_place_northing="307950")

        return super().station_record_to_dict(record)

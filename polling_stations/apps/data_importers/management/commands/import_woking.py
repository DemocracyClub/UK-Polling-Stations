from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOI"
    addresses_name = (
        "2024-07-04/2024-05-28T18:55:42.997031/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-28T18:55:42.997031/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000218826",  # THE BUNGALOW DAWNEY HILL, PIRBRIGHT
            "10002428855",  # FLAT 7, THE OLD BREW HOUSE 130-132, HIGH STREET, OLD WOKING, WOKING
            "200000216418",  # THORLEY COTTAGE, PYRFORD ROAD, WOKING
            "100061656800",  # HEDGE COTTAGE, SAUNDERS LANE, WOKING
        ]:
            return None

        if record.addressline6 in [
            # splits
            "KT14 6LT",
            "GU22 8AF",
            "GU21 2NJ",
            # looks wrong
            "KT15 3QA",
            "KT15 3QD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Horsell Evangelical Church High Street Horsell Woking GU21 3SZ
        if record.polling_place_id == "5531":
            record = record._replace(polling_place_postcode="GU21 4SZ")

        return super().station_record_to_dict(record)
